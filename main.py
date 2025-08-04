from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompt import AGENT_INSTRUCTIONS, AGENT_RESPONSE
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Load environment variables from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

# Gemini AI wrapper function
def run_neo2_ai(user_message):
    full_prompt = f"{AGENT_INSTRUCTIONS}\n\nUser: {user_message}\nNeo 2:{AGENT_RESPONSE}"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(full_prompt)
    return response.text

# Root route (optional)
@app.route("/")
def home():
    return """
    <h2>🚀 Neo 2 Server is Running</h2>
    <p>Send POST requests to <code>/neo2</code> with a JSON body like:</p>
    <pre>{
      "message": "Hello Neo 2"
    }</pre>
    """

# API endpoint for your WebUI or any frontend
@app.route("/neo2", methods=["POST"])
def neo2_reply():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"reply": "⚠️ No message received, Beastie."})

        reply = run_neo2_ai(user_message)
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Internal error: {str(e)}"})

# Run locally
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
