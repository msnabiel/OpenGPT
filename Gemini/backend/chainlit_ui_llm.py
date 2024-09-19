import chainlit as cl
import os
from typing import List
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
import requests

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask server URL
from flask_server import server_url
FLASK_SERVER_URL = server_url

def build_prompt(query: str, context: List[str]) -> str:
    """
    Builds a prompt for the LLM in Gemini's format.

    Args:
    query (str): The original query.
    context (List[str]): The context of the query, returned by embedding search.

    Returns:
    A prompt for the LLM (str).
    """
    base_prompt = {
        "content": "I am going to ask you a question, which I would like you to answer"
                   " based only on the provided context, and not any other information."
                   " If there is not enough information in the context to answer the question,"
                   ' say "I am not sure", then try to make a guess.'
                   " Break your answer up into nicely readable paragraphs.",
    }
    user_prompt = {
        "content": f" The question is '{query}'. Here is all the context you have:"
                   f'{(" ").join(context)}',
    }

    return f"{base_prompt['content']} {user_prompt['content']}"

def get_gemini_response(query: str, context: List[str]) -> str:
    """
    Queries the Gemini API to get a response to the question.

    Args:
    query (str): The original query.
    context (List[str]): The context of the query, returned by embedding search.

    Returns:
    A response to the question.
    """
    response = model.generate_content(build_prompt(query, context))
    return response.text

@cl.on_chat_start
async def on_chat_start():
    # Fetch user_id from Flask
    user_id = fetch_user_id_from_flask()
    print(f"User ID: {user_id}")

    # Initialize other session values
    cl.user_session.set("history", [])
    cl.user_session.set("context", [])

    await cl.Message(content="Hello, I am OpenGPT, Powered by Gemini. How can I assist you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    message_content = message.content  # Extract content from the message

    # Instantiate a persistent chroma client
    client = chromadb.PersistentClient(path="chroma_storage")

    # Create embedding function
    google_api_key = os.getenv("GOOGLE_API_KEY")  # Ensure your Google API key is set in the environment variables
    embedding_function = embedding_functions.GoogleGenerativeAIEmbeddingFunction(
        api_key=google_api_key, task_type="RETRIEVAL_QUERY"
    )

    # Get the collection
    collection = client.get_collection(
        name="documents_collection", embedding_function=embedding_function
    )

    # Query the collection to get the most relevant results
    results = collection.query(
        query_texts=[message_content], n_results=5, include=["documents", "metadatas"]
    )

    # Extract context and sources
    context = results["documents"][0] if results["documents"] else []  # Handle empty results
    sources = "\n".join(
        [f"{metadata['filename']}: line {metadata['line_number']}" for metadata in results["metadatas"][0]]
    ) if results["metadatas"] else "No sources found"

    # Get the response from Gemini
    response = get_gemini_response(message_content, context)

    # Get history and context from the session
    history = cl.user_session.get("history", [])
    current_context = cl.user_session.get("context", [])

    # Update history and context
    history.append({"message": message_content, "response": response})
    current_context = context

    # Save the updated history and context back to the session
    cl.user_session.set("history", history)
    cl.user_session.set("context", current_context)

    # Combine the response and sources for the final message
    full_response = f"{response}\n\n**Sources:**\n{sources}"

    # Send the combined response
    await cl.Message(content=full_response).send()

def fetch_user_id_from_flask() -> str:
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/")
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json().get('user_id', 'default_user')
    except requests.RequestException as e:
        print(f"Error fetching user_id from Flask: {e}")
        return 'default_user'

# Entry point for Chainlit
if __name__ == "__main__":
    cl.run()
