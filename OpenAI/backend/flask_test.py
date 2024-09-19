from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import time
import psutil
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Allow CORS for the specific frontend URL

# Global variable to store the user_id temporarily
stored_user_id = None
chainlit_process = None

def is_chainlit_running() -> bool:
    """Check if Chainlit is running."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        cmdline = proc.info.get('cmdline')
        if cmdline and 'frontend_test.py' in cmdline:
            return True
    return False

def start_chainlit():
    """Start the Chainlit application."""
    global chainlit_process
    if not is_chainlit_running():
        print("Starting Chainlit application...")
        chainlit_process = subprocess.Popen(
            ["chainlit", "run", "frontend_test.py", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensure the output is in text format for Python 3.5+
        )

        # Print Chainlit output to the terminal
        for line in iter(chainlit_process.stdout.readline, b''):
            print(line, end='')

def wait_for_chainlit_ready():
    """Wait for Chainlit to be fully ready by pinging the Chainlit server."""
    chainlit_url = 'http://localhost:8000'  # Chainlit's URL
    timeout = 30  # Wait up to 30 seconds for Chainlit to be ready
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Send a request to Chainlit to check if it's ready
            response = requests.get(chainlit_url)
            if response.status_code == 200:
                print("Chainlit is ready!")
                return True
        except requests.ConnectionError:
            # Chainlit is not ready yet, wait a bit and retry
            time.sleep(1)

    print("Chainlit failed to start within the timeout period.")
    return False

@app.route('/', methods=['POST', 'GET'])
def index():
    global stored_user_id

    if request.method == 'POST':
        # Handle POST request from React
        data = request.get_json()
        user_id = data.get('user_id')

        if user_id:
            # Store the user_id
            stored_user_id = user_id
            print(f"Stored user_id: {user_id}")

            # Start the Chainlit application
            if not is_chainlit_running():
                try:
                    start_chainlit()

                    # Wait for Chainlit to be ready
                    if wait_for_chainlit_ready():
                        chainlit_url = 'http://localhost:8000'  # Chainlit URL

                        # Respond to React POST request after Chainlit is ready
                        return jsonify({
                            'user_id': user_id,
                            'redirect_url': chainlit_url
                        }), 200
                    else:
                        # Chainlit didn't start within the timeout period
                        return jsonify({'error': 'Chainlit failed to start'}), 500

                except RuntimeError as e:
                    print(f"Error: {e}")
                    return jsonify({'error': 'Failed to start Chainlit application'}), 500
            else:
                # If Chainlit is already running, respond immediately
                return jsonify({
                    'user_id': user_id,
                    'redirect_url': 'http://localhost:8000'  # Chainlit URL
                }), 200

        else:
            # Return error if no user_id is found in the request
            print("No user_id found in request")
            return jsonify({'error': 'user_id not found'}), 400

    elif request.method == 'GET':
        # Handle GET request from Chainlit
        if stored_user_id:
            chainlit_url = 'http://localhost:8000'  # Chainlit URL

            # Return the stored user_id and redirect_url, then clear stored_user_id
            response = jsonify({
                'user_id': stored_user_id,
                'redirect_url': chainlit_url
            })
            print(f"Returning stored user_id: {stored_user_id}")
            stored_user_id = None  # Clear the stored user_id after it has been fetched
            return response, 200
        else:
            # Return error if no user_id is found
            print("No user_id found in storage")
            return jsonify({'error': 'user_id not found'}), 400

if __name__ == '__main__':
    print("Starting Flask application on port 7000")
    app.run(port=7000)