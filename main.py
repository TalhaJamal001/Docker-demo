from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
import hmac

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve environment variables
VEEVA_VAULT_URL = os.getenv("VEEVA_VAULT_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
API_KEY = os.getenv("API_KEY")

print("Debugging the env values")
print("VEEVA_VAULT_URL:", VEEVA_VAULT_URL)
print("USERNAME:", USERNAME)
print("PASSWORD:", PASSWORD)
print("API_KEY:", API_KEY)

# Function to authenticate API key
def authenticate_api_key(api_key):
    if api_key is None:
        return False
    return hmac.compare_digest(api_key, API_KEY)

# Define the route to get session ID
@app.route('/get-session-id', methods=['POST'])
def get_session_id():
    # Retrieve API key from request headers
    api_key = request.headers.get('Authorization')

    # Authenticate API key
    if not authenticate_api_key(api_key):
        return jsonify({'error': 'Unauthorized access'}), 403

    # Prepare payload for Veeva Vault API request
    payload = {
        'username': "e0517016@sb-sanofi.com",
        'password': PASSWORD
    }

    try:
        # Make the POST request to Veeva Vault
        response = requests.post(VEEVA_VAULT_URL, data=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Extract session ID from response
        session_id = response.json().get('sessionId')
        if session_id is None:
            return jsonify({'error': 'Session ID not found'}), 500

        # Print the session ID to the terminal
        print("Session ID:", session_id)

        # Return the session ID in the API response
        return jsonify({'session_id': session_id})

    except requests.RequestException as e:
        # Handle request exceptions and return error message
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)