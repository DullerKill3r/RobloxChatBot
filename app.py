import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HUGGING_FACE_API_KEY = os.getenv('HF_API_KEY')  # Store your Hugging Face key as an env variable

headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # If you require your own API key check:
    if request.headers.get('Authorization') != f"Bearer {os.getenv('API_KEY')}":
        return jsonify({"error": "Unauthorized"}), 403

    # Make sure the user provided a message
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Prepare the payload for Hugging Face
    payload = {"inputs": user_message}

    # Send request to Hugging Face
    response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        # Parse the model's output
        model_output = response.json()
        # The exact structure of `model_output` depends on the model. 
        # GPT-2 typically returns a list with 'generated_text'.
        # For example:
        generated_text = model_output[0].get("generated_text", "")

        return jsonify({"reply": generated_text})
    else:
        return jsonify({"error": "Hugging Face API error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
