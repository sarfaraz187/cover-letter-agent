# AI Chat Application

A ChatGPT-like interface built with React and connected to a Flask backend that uses the Gemini AI API.

## Project Structure

- `ai-chat-ui`: React frontend with a ChatGPT-like interface
- `flask_api.py`: Flask backend API that connects to Gemini AI
- `requirements.txt`: Python dependencies for the Flask backend

## Setup Instructions

### Prerequisites

- Node.js and npm (for React frontend)
- Python 3.7+ (for Flask backend)

### Environment Setup

1. Create environment files:
   - For the backend: Copy `.env.example` to `.env` and add your Gemini API key
   - For the frontend (optional): Create `ai-chat-ui/.env` for custom API URL

```bash
# Backend environment setup
cp .env.example .env
# Edit .env and add your actual Gemini API key
```

### Frontend Setup

1. Navigate to the React app directory:
   ```bash
   cd ai-chat-ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   This will run the app on [http://localhost:3000](http://localhost:3000)

### Backend Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask API:
   ```bash
   python flask_api.py
   ```
   This will run the API on [http://localhost:5000](http://localhost:5000)

### Running Both Frontend and Backend

You can start both services with a single command:
```bash
npm run dev
```

## API Endpoints

- `POST /api/chat`: Send a message to the AI and get a response
  - Request body: `{ "message": "Your message here" }`
  - Response: `{ "response": "AI response here" }`

- `POST /api/sessions`: Create a new chat session
  - Response: `{ "sessionId": "session-uuid" }`

- `DELETE /api/sessions/<session_id>`: Delete a chat session
  - Response: `{ "success": true }`

- `GET /api/health`: Health check endpoint
  - Response: `{ "status": "ok", "api_key_configured": true }`

## Debugging

If you encounter issues with the application, refer to the `DEBUG.md` file for troubleshooting steps.

## Notes

- The UI is designed to mimic the ChatGPT interface
- The backend connects to the Gemini AI API from Google
- API keys are stored in environment variables for security 