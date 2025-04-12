#!/bin/bash

echo "Stopping servers..."

# Stop Flask backend
echo "Stopping Flask backend..."
pkill -f "python3 flask_api.py" || {
  echo "No Flask server running."
}

# Stop React frontend
echo "Stopping React frontend..."
pkill -f "node.*start" || {
  echo "No React server running."
}

echo "All servers stopped!" 