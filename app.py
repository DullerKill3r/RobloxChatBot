import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Access the environment variable
API_KEY = os.getenv('API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Check if the API key matches (if you need to validate it)
    if request.headers.get('Authorization') != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 403
    
    if user_message:
        # Process the message and return a response
        return jsonify({"reply": f"Bot received: {user_message}"})
    return jsonify({"error": "No message provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
