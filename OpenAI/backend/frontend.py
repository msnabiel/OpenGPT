import chainlit as cl
import os
from typing import List
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from flask import request
from chainlit import user_session as session

# Load LaMini model and tokenizer
checkpoint = "/Users/msnabiel/Desktop/name/LaMini-T5-738M"
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
    """
    Builds a prompt for LaMini.

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

    # Combine the prompts to output a single prompt string
    system = f"{base_prompt['content']} {user_prompt['content']}"
    return system

def get_lamini_response(query: str, context: List[str]) -> str:
    """
    Queries the LaMini model to get a response to the question.

    Args:
    query (str): The original query.
    context (List[str]): The context of the query, returned by embedding search.

    Returns:
    A response to the question.
    """
    # Generate a response using the LaMini model pipeline
    prompt = build_prompt(query, context)
    response = generator(prompt)[0]['generated_text']
    return response

# Chainlit chat handler
@cl.on_chat_start
def on_chat_start():
    # Instead of request.args.get, use session to retrieve user-specific data
    user_id = session.get('user_id')  # Replace 'user_id' with how you want to identify users
    if user_id is None:
        # Handle the case where user_id is not found
        session.set('user_id', 'default_user')  # Set some default or get from frontend
        user_id = 'default_user'
    
    # Continue with your logic using the user_id
    print(f"User ID: {user_id}")

    # Initialize other session values
    cl.user_session.set("history", [])
    cl.user_session.set("context", [])


@cl.on_message
async def handle_message(message: cl.Message):
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