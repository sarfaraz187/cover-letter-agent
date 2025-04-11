from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from google import generativeai as genai
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Enable CORS with more explicit configuration
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logger.error("No API key found. Please set the GOOGLE_API_KEY environment variable.")
    raise ValueError("No API key found. Please set the GOOGLE_API_KEY environment variable.")

# Initialize Gemini AI with your API key
logger.info("Configuring Gemini AI...")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# In-memory storage for chat sessions
chat_sessions = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    logger.info(f"Received request: {request.method} {request.path}")
    logger.info(f"Request headers: {request.headers}")
    
    data = request.json
    logger.info(f"Request data: {data}")
    
    message = data.get('message', '')
    session_id = data.get('session_id', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        logger.info(f"Processing message: {message}")
        
        # Set up the model configuration
        generation_config = {
            "max_output_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.95
        }
        
        # Get a response from Gemini
        response = model.generate_content(
            contents=message,
            generation_config=generation_config
        )
        
        # Handle different response formats
        response_text = ""
        if hasattr(response, 'text'):
            response_text = response.text
        elif hasattr(response, 'parts'):
            response_text = ' '.join([part.text for part in response.parts if hasattr(part, 'text')])
        else:
            response_text = str(response)
            
        logger.info(f"AI response (truncated): {response_text[:100]}...")
        
        return jsonify({'response': response_text})
    except Exception as e:
        logger.exception(f"Error generating response: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    chat_sessions[session_id] = []
    logger.info(f"Created new session: {session_id}")
    return jsonify({'sessionId': session_id})

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        logger.info(f"Deleted session: {session_id}")
        return jsonify({'success': True})
    logger.warning(f"Session not found: {session_id}")
    return jsonify({'error': 'Session not found'}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'api_key_configured': bool(api_key)})

if __name__ == '__main__':
    logger.info("Starting Flask API server...")
    app.run(debug=True, port=5000)