import chainlit as cl
import os
from typing import List
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from flask import request
from chainlit import user_session as session
import requests  # Add this import to make HTTP requests

# Flask server URL
#FLASK_SERVER_URL = "http://127.0.0.1:7000"
from flask_server import server_url
FLASK_SERVER_URL = server_url


# Load LaMini model and tokenizer
checkpoint = "../LaMini-T5-738M"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# Create a text generation pipeline using the LaMini model
generator = pipeline(
    'text2text-generation', 
    model=base_model, 
    tokenizer=tokenizer, 
    max_length=256,
    do_sample=True,
    temperature=0.3,
    top_p=0.95
)

def build_prompt(query: str, context: List[str]) -> str:
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

    # Combine the prompts to output a single prompt string
    system = f"{base_prompt['content']} {user_prompt['content']}"
    return system

def get_lamini_response(query: str, context: List[str]) -> str:
    # Generate a response using the LaMini model pipeline
    prompt = build_prompt(query, context)
    response = generator(prompt)[0]['generated_text']
    return response

def fetch_user_id_from_flask() -> str:
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/")
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        #global hi
        #hi = str(data.get('user_id', 'default_user'))
        return data.get('user_id', 'default_user')
    except requests.RequestException as e:
        print(f"Error fetching user_id from Flask: {e}")
        return 'default_user'

@cl.on_chat_start
async def on_chat_start():
    # Fetch user_id from Flask
    user_id = fetch_user_id_from_flask()
    
    # Continue with your logic using the user_id
    print(f"User ID: {user_id}")

    # Initialize other session values
    cl.user_session.set("history", [])
    cl.user_session.set("context", [])

    await cl.Message(content="Hello, I am OpenGPT. How can I assist you today?").send()


@cl.on_message
async def handle_message(message: cl.Message):
    #print(hi)
    message_content = message.content  # Extract content from the message

    # Instantiate a persistent chroma client
    client = chromadb.PersistentClient(path="chroma_storage")

    # Create embedding function
    embedding_function = embedding_functions.HuggingFaceEmbeddingFunction(
        api_key="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",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
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
        [f"{result['filename']}: line {result['line_number']}" for result in results["metadatas"][0]]
    ) if results["metadatas"] else ""

    # Get the response from LaMini
    response = get_lamini_response(message_content, context)

    # Get history and context from the session
    history = cl.user_session.get("history", [])
    current_context = cl.user_session.get("context", [])

    # Update history and context
    history.append({"message": message_content, "response": response})
    current_context = context

    # Save the updated history and context back to the session
    cl.user_session.set("history", history)
    cl.user_session.set("context", current_context)

    # Send the response
    await cl.Message(content=response).send()

# Entry point for Chainlit
if __name__ == "__main__":
    cl.run()
