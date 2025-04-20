from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client
import os

app = Flask(__name__)
CORS(app)

# فقط اكتب اسم المساحة بدون src=
client = Client("https://alim9hamed-medical-chatbot.hf.space")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"error": "Missing question"}), 400

        result = client.predict(
            question,
            api_name="/predict"
        )

        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
