# Chatbot Project 🤖

This chatbot helps users with queries related to Google tools. Built with Flask and Python.

## Setup  
1️⃣ **Get an API Key:**  
   - Visit Google Cloud Console (or OpenAI API, if used).  
   - Create a project and enable the required APIs.  
   - Generate an API key and replace `"GEMINI_API_KEY"` in the env file in the code.  

2️⃣ **Generate a Flask Secret Key:**  
   Run this command in the terminal:  
   ```sh
   python -c "import secrets; print(secrets.token_hex(16))"
```

  -add this secret key to the "FLASK_SECRET_KEY" in the env file in the code


  
