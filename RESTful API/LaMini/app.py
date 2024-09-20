import argparse
import os
from typing import List
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from flask import Flask, request, jsonify

# Load LaMini model and tokenizer
checkpoint = "LaMini-T5-738M"
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

app = Flask(__name__)

def build_prompt(query: str, context: List[str]) -> str:
    """
    Builds a prompt for LaMini.
    """
    base_prompt = {
        "content": "I am going to ask you a question, which I would like you to answer"
        " based only on the provided context, and not any other information."
        " If there is not enough information in the context to answer the question,"
        ' say "I am not sure", then try to make a guess.'
        " Break your answer up into nicely readable paragraphs.",
    }
    user_prompt = {
        "content": f" The question is '{query}'. Here is all the context you have: "
        f'{(" ").join(context)}',
    }

    # Combine the prompts to output a single prompt string
    system = f"{base_prompt['content']} {user_prompt['content']}"

    return system

def get_lamini_response(query: str, context: List[str]) -> str:
    """
    Queries the LaMini model to get a response to the question.
    """
    # Generate a response using the LaMini model pipeline
    prompt = build_prompt(query, context)
    response = generator(prompt)[0]['generated_text']
    return response

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles incoming requests to chat with the bot.
    Expects a JSON body with 'query' key, and headers with 'x-user-id' and 'x-session-id'.
    """
    try:
        # Extract request data
        query = request.json.get('query')
        user_id = request.headers.get('x-user-id')
        session_id = request.headers.get('x-session-id')

        if not query or not user_id or not session_id:
            return jsonify({"error": "Missing required fields"}), 400

        # Instantiate a persistent chroma client (can be modified to use provided args)
        client = chromadb.PersistentClient(path="chroma_storage")

        # Create embedding function
        embedding_function = embedding_functions.HuggingFaceEmbeddingFunction(
            api_key="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",
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Get the collection (assuming collection_name is fixed for now)
        collection = client.get_collection(
            name="documents_collection", embedding_function=embedding_function
        )

        # Query the collection to get the 5 most relevant results
        results = collection.query(
            query_texts=[query], n_results=5, include=["documents", "metadatas"]
        )

        # Get the context from the first result (modify as needed to process multiple documents)
        context = results["documents"][0]

        # Get the response from LaMini model
        response_text = get_lamini_response(query, context)

        # Prepare response with source metadata
        sources = "\n".join(
            [f"{result['filename']}: line {result['line_number']}" for result in results["metadatas"][0]]
        )

        return jsonify({
            "bot_message": response_text,
            "sources": sources
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the chatbot API")

    parser.add_argument(
        "--port", type=int, default=3000, help="Port to run the API on"
    )

    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)
