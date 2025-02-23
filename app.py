from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face GPT-2 Large model endpoint and your API key
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/gpt2-large"
HUGGING_FACE_API_KEY = "YOUR_HUGGING_FACE_API_KEY"  # Replace with your Hugging Face API key

headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

@app.route('/chat', methods=['POST'])
def chat():
    # Get user input from Roblox request
    user_input = request.json.get("input", "")
    
    # Create the payload for Hugging Face's GPT-2 model
    payload = {"inputs": user_input}
    
    # Make the API request to Hugging Face
    response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        # Get the model's output
        model_output = response.json()
        
        # Return the model's generated text (adjust as needed for your use case)
        return jsonify(model_output)
    else:
        return jsonify({"error": "Error with Hugging Face API"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
