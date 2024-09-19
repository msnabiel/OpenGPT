import chainlit as cl
import os
from typing import List
import chromadb
from chromadb.utils import embedding_functions
import openai
from flask import request
from chainlit import user_session as session
import requests

# Flask server URL
from flask_server import server_url
FLASK_SERVER_URL = server_url

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your OpenAI API key is set in the environment variables
#model_name = "gpt-3.5-turbo"  # Change to "gpt-4" if preferred
model_name = "gpt-4o-mini" # Change to "gpt-4o" if preferred

def build_prompt(query: str, context: List[str]) -> List[dict]:
    """
    Builds a prompt for the LLM in OpenAI's format.

    Args:
    query (str): The original query.
    context (List[str]): The context of the query, returned by embedding search.

    Returns:
    A list of messages for the LLM.
    """
    return [
        {"role": "system", "content": (
            "I am going to ask you a question, which I would like you to answer"
            " based only on the provided context, and not any other information."
            " If there is not enough information in the context to answer the question,"
            ' say "I am not sure", then try to make a guess.'
            " Break your answer up into nicely readable paragraphs."
        )},
        {"role": "user", "content": f"The question is '{query}'. Here is all the context you have:"
        f'{(" ").join(context)}'}
    ]

def get_openai_response(query: str, context: List[str], model_name: str) -> str:
    """
    Queries the OpenAI API to get a response to the question.

    Args:
    query (str): The original query.
    context (List[str]): The context of the query, returned by embedding search.
    model_name (str): The OpenAI model to use (e.g., "gpt-4o-mini" or "gpt-4o").

    Returns:
    A response to the question.
    """
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=build_prompt(query, context)
    )
    return response.choices[0].message['content']

@cl.on_chat_start
async def on_chat_start():
    # Fetch user_id from Flask
    user_id = fetch_user_id_from_flask()
    
    # Continue with your logic using the user_id
    print(f"User ID: {user_id}")

    # Initialize other session values
    cl.user_session.set("history", [])
    cl.user_session.set("context", [])

    await cl.Message(content="Hello, I am OpenGPT, Powered by OpenAI. How can I assist you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    message_content = message.content  # Extract content from the message

    # Instantiate a persistent chroma client
    client = chromadb.PersistentClient(path="chroma_storage")

    # Create embedding function
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai.api_key,
        model_name="text-embedding-3-small"
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

    # Get the response from OpenAI
    response = get_openai_response(message_content, context, model_name)

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
