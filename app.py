from flask import Flask, render_template, request, session, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import uuid
import markdown

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_key")

# Configure Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define chatbot system instruction
SYSTEM_INSTRUCTION = """You are an AI chatbot assistant specialized in helping users with queries related to Google tools. 
Provide clear, concise, and accurate responses about Google services like Gmail, Google Drive, Docs, Sheets, Meet, Calendar, 
Google Cloud, and other Google products. Keep responses relevant and avoid unnecessary repetition."""


model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Helper function to convert Markdown to HTML
def format_response(text):
    return markdown.markdown(text)

@app.route("/", methods=["GET"])
def home():
    if "chat_sessions" not in session:
        session["chat_sessions"] = {}

    if "default" not in session["chat_sessions"]:
        session["chat_sessions"]["default"] = [
            {"role": "system", "text": SYSTEM_INSTRUCTION},  # System instruction
            {"role": "bot", "text": "Hello! How can I assist you today?"}
        ]
    
    return render_template("index.html", chat_sessions=session["chat_sessions"])

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if "chat_sessions" not in session:
        session["chat_sessions"] = {}

    if session_id not in session["chat_sessions"]:
        session["chat_sessions"][session_id] = [
            {"role": "system", "text": SYSTEM_INSTRUCTION},
            {"role": "bot", "text": "Hello! How can I assist you today?"}
        ]
    
    if message:
        session["chat_sessions"][session_id].append({"role": "user", "text": message})

        # Send system instruction along with user input
        response = model.generate_content([SYSTEM_INSTRUCTION, message])
        bot_response = response.text if hasattr(response, "text") else "Sorry, I didn't understand."

        # Convert Markdown (like **bold**) to HTML
        bot_response = format_response(bot_response)

        session["chat_sessions"][session_id].append({"role": "bot", "text": bot_response})
        session.modified = True

    return jsonify(session["chat_sessions"][session_id])

@app.route("/new_chat", methods=["POST"])
def new_chat():
    session_id = str(uuid.uuid4())[:8]  # Generate new session ID
    
    # Ensure chat_sessions exists
    if "chat_sessions" not in session:
        session["chat_sessions"] = {}

    # Create new session without deleting old ones
    session["chat_sessions"][session_id] = [
        {"role": "system", "text": SYSTEM_INSTRUCTION},
        {"role": "bot", "text": "Hello! How can I assist you today?"}
    ]
    
    session.modified = True  # Save session changes

    return jsonify({"session_id": session_id, "chat_sessions": session["chat_sessions"]})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
