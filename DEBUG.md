# Debugging AI Chat Application

This guide will help you verify that your frontend is properly connecting to your backend, and your backend is connecting to the Gemini AI API.

## 1. Starting the Backend and Frontend

Make sure both your backend and frontend are running:

```bash
# From the project root:
npm run dev
```

This should start your Flask backend on port 5000 and your React frontend on port 3000.

## 2. Testing the Backend Directly

Use the included test script to check if your backend is working correctly:

```bash
# From the project root:
python3 test_backend.py
```

You should see output indicating whether the health check and chat API tests passed.

## 3. Troubleshooting "Failed to fetch" Errors

If you see "Failed to fetch" errors in the frontend, this typically indicates CORS or network connectivity issues between the frontend and backend. Here's how to troubleshoot:

1. **Test CORS Configuration**:
   Run the CORS test script to simulate browser requests:
   ```bash
   python3 test_cors.py
   ```
   This script will check if CORS is properly configured.

2. **Verify Backend is Running**:
   Check that the Flask backend is running and accessible:
   ```bash
   curl http://localhost:5000/api/health
   ```
   You should get a JSON response with `"status": "ok"`.

3. **Check API Port and Host**:
   Make sure the backend is running on `0.0.0.0` to accept connections from any IP:
   ```bash
   # In flask_api.py
   app.run(debug=True, port=5000, host='0.0.0.0')
   ```

4. **Verify Frontend API URL**:
   Check that the frontend is using the correct API URL:
   ```bash
   # In ai-chat-ui/.env
   REACT_APP_API_URL=http://localhost:5000/api
   ```

5. **Check for Network/Firewall Issues**:
   - Ensure no firewall is blocking port 5000
   - Try accessing the backend API from a different browser
   - Check if localhost resolves correctly

## 4. Checking Browser Network Requests

1. Open your browser to http://localhost:3000
2. Open the developer tools (F12 or right-click > Inspect)
3. Go to the Network tab
4. Type a message in the chat interface and send it
5. Look for a request to `http://localhost:5000/api/chat`
6. Examine the request and response:
   - Request should include your message
   - Response should include the AI's response

## 5. Checking Console Logs

1. In the browser developer tools, go to the Console tab
2. Send a message in the chat interface
3. You should see logs indicating:
   - API Request being sent
   - API Response status and data received

## 6. Checking Backend Logs

In the terminal where your Flask backend is running, you should see logs including:
- Received request details
- Processing message
- AI response information
- Any errors that might occur

## Common Issues and Solutions

### CORS Errors
If you see CORS-related errors in the browser console:
- Ensure the Flask app has CORS properly configured
- Check that the frontend is using the correct API URL
- Try adding explicit CORS headers in the response:
  ```python
  @app.after_request
  def add_cors_headers(response):
      response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      return response
  ```

### Connection Refused
If you see "Connection refused" errors:
- Ensure the Flask backend is running
- Check that it's running on port 5000 and host 0.0.0.0
- Verify your frontend is using `http://localhost:5000/api` as the base URL

### API Key Issues
If you see authentication errors from the Gemini API:
- Verify your API key is correct
- Check that the key has the necessary permissions
- Ensure the environment variables are being loaded properly

### Data Format Issues
If responses are not appearing correctly:
- Check the response format from the Gemini API
- Ensure the parsing logic in the Flask backend is correct

## Testing a Simple Request with cURL

You can test your backend API directly using cURL:

```bash
curl -X POST \
  http://localhost:5000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Hello, are you working?"}'
```

This should return a JSON response containing the AI's reply. 