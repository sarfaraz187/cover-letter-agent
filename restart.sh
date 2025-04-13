#!/bin/bash

echo "Stopping any existing servers..."
./stop.sh

# Make sure environment variables are available
if [ ! -f ".env" ]; then
  echo "Error: .env file missing in the root directory"
  echo "Please create a .env file with the necessary environment variables"
  exit 1
fi

# Start the Flask backend
echo "Starting Flask backend..."
python flask_api.py &
BACKEND_PID=$!

# Wait for Flask to initialize
echo "Waiting for Flask server to initialize (5 seconds)..."
sleep 5

# Test if the Flask server is running
echo "Testing Flask server..."
RESPONSE=$(curl -s http://localhost:5001/api/health)
echo $RESPONSE

# Start the React frontend
echo "Starting React frontend..."
cd ai-chat-ui
npm start > ../react.log 2>&1 &
FRONTEND_PID=$!

# Save the PIDs to our PID file for the stop script
echo "$BACKEND_PID" > ../.pids.backend
echo "$FRONTEND_PID" > ../.pids.frontend

echo "Servers successfully started!"
echo "- Backend: http://localhost:5001/api/health"
echo "- Frontend: http://localhost:3000"
echo ""
echo "To view logs:"
echo "- Backend: tail -f flask.log"
echo "- Frontend: tail -f react.log"
echo ""
echo "To stop servers: ./stop.sh" 