#!/bin/bash

echo "Stopping any existing servers..."
pkill -f "python3 flask_api.py" || true
pkill -f "node.*start" || true

echo "Starting Flask backend..."
python3 flask_api.py > flask.log 2>&1 &
FLASK_PID=$!
echo "Flask server started with PID: $FLASK_PID"

echo "Waiting for Flask server to initialize (5 seconds)..."
sleep 5

echo "Testing Flask server..."
curl -s http://localhost:5001/api/health || {
  echo "Error: Flask server is not responding. Check flask.log for details."
  exit 1
}

echo "Starting React frontend..."
cd ai-chat-ui && npm start > ../react.log 2>&1 &
REACT_PID=$!
echo "React server started with PID: $REACT_PID"

echo "Servers successfully started!"
echo "- Backend: http://localhost:5001/api/health"
echo "- Frontend: http://localhost:3000"
echo ""
echo "To view logs:"
echo "- Backend: tail -f flask.log"
echo "- Frontend: tail -f react.log"
echo ""
echo "To stop servers: ./stop.sh" 