from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import psutil
import threading
import socket

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to store the user_id temporarily
stored_user_id = None
chainlit_process = None
server_url = None

def is_chainlit_running() -> bool:
    """Check if Chainlit is running."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        cmdline = proc.info.get('cmdline')
        if cmdline and 'chainlit_ui_llm.py' in cmdline:
            return True
    return False

def start_chainlit():
    """Start the Chainlit application."""
    global chainlit_process
    if not is_chainlit_running():
        print("Starting Chainlit application...")
        # Start Chainlit in a non-blocking way without reading output
        chainlit_process = subprocess.Popen(
            ["chainlit", "run", "chainlit_ui_llm.py", "-h"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

def monitor_chainlit_output():
    """Monitor Chainlit output in a separate thread."""
    global chainlit_process
    # Print Chainlit output to the terminal
    for line in iter(chainlit_process.stdout.readline, b''):
        print(line.decode(), end='')

@app.route('/', methods=['POST', 'GET'])
def index():
    global stored_user_id

    if request.method == 'POST':
        # Handle POST request
        data = request.get_json()
        user_id = data.get('user_id')

        if user_id:
            # Store the user_id
            stored_user_id = user_id
            print(f"Stored user_id: {user_id}")

            # Start the Chainlit application and check if it's running
            try:
                start_chainlit()
                threading.Thread(target=monitor_chainlit_output, daemon=True).start()
                chainlit_url = 'http://localhost:8000'  # Adjust this URL to your Chainlit application URL

                # Return the URL for redirection immediately
                return jsonify({
                    'user_id': user_id,
                    'redirect_url': chainlit_url
                }), 200
            except RuntimeError as e:
                print(f"Error: {e}")
                return jsonify({'error': 'Failed to start Chainlit application'}), 500
        else:
            # Return error if no user_id is found in the request
            print("No user_id found in request")
            return jsonify({'error': 'user_id not found'}), 400

    elif request.method == 'GET':
        # Handle GET request with both stored_user_id and query parameters
        query_user_id = request.args.get('user_id')

        if stored_user_id:
            # Return the stored user_id and clear it
            response = jsonify({'user_id': stored_user_id})
            print(f"Returning stored_user_id: {stored_user_id}")
            stored_user_id = None  # Clear the stored user_id after it has been fetched
            return response, 200
        elif query_user_id:
            # If user_id is passed via query params
            print(f"Received user_id from query params: {query_user_id}")
            return jsonify({'user_id': query_user_id}), 200
        else:
            # Return error if no user_id is found
            print("No user_id found in storage or query parameters")
            return jsonify({'error': 'user_id not found'}), 400

if __name__ == '__main__':
    # Default host and port settings
    port = 7000

    # Resolve the default host to get the IP address
    default_host = '127.0.0.1'
    addr_info = socket.getaddrinfo(default_host, port, socket.AF_INET, socket.SOCK_STREAM)
    ip_address = addr_info[0][4][0]

    # Create the server URL
    server_url = f"http://{ip_address}:{port}"

    print(f"Starting Flask application on {server_url}")
    app.run(port=port)
