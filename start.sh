#!/bin/bash

# Start the Flask backend
echo "Starting Flask backend..."
cd api
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
python app.py &
BACKEND_PID=$!

# Start the React frontend
echo "Starting React frontend..."
cd ../frontend
npm install
npm start &
FRONTEND_PID=$!

# Function to handle script termination
function cleanup {
    echo "Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Register the cleanup function for when script receives SIGINT
trap cleanup SIGINT

echo "Servers running. Press Ctrl+C to stop."
wait 