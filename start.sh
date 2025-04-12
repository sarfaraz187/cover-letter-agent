#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Check if the CV file exists
if [ -f "$CV_FILENAME" ]; then
    echo "Found CV file: $CV_FILENAME"
else
    echo "Warning: CV file '$CV_FILENAME' not found in root directory." 
    echo "Make sure to add your CV file as specified in the .env file."
fi

# Start the Flask backend
echo "Starting Flask backend..."
cd api
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
python ../flask_api.py &
BACKEND_PID=$!

# Start the React frontend
echo "Starting React frontend..."
cd ../ai-chat-ui
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