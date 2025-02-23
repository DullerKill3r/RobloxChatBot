import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1) Hugging Face API Key
HUGGING_FACE_API_KEY = os.getenv('HF_API_KEY')  # For calls to Hugging Face
HF_HEADERS = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

# 2) Flask App Key
FLASK_APP_KEY = os.getenv('API_KEY')  # For checking incoming requests

@app.route('/chat', methods=['POST'])
def chat():
    # Check that the request includes the correct Authorization header
    if request.headers.get('Authorization') != f"Bearer {FLASK_APP_KEY}":
        return jsonify({"error": "Unauthorized"}), 403

    # Get user message from JSON
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Forward the message to Hugging Face GPT-2 Large
    payload = {"inputs": user_message}
    response = requests.post(
        "https://api-inference.huggingface.co/models/gpt2-large",
        headers=HF_HEADERS,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        # GPT-2 returns an array with a "generated_text" key
        generated_text = data[0].get("generated_text", "No text generated")
        return jsonify({"reply": generated_text})
    else:
        return jsonify({"error": "Hugging Face API error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
