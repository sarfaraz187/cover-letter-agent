#!/bin/bash

echo "Stopping AI Cover Letter Generator servers..."

# Check if the PID files exist and kill the processes
if [ -f ".pids.backend" ]; then
  BACKEND_PID=$(cat .pids.backend)
  if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Stopping backend server (PID: $BACKEND_PID)..."
    kill $BACKEND_PID
  else
    echo "Backend server is not running."
  fi
  rm .pids.backend
else
  # Fallback method: use pkill
  echo "No PID file found for backend. Attempting to stop with pkill..."
  pkill -f "python flask_api.py" || true
fi

if [ -f ".pids.frontend" ]; then
  FRONTEND_PID=$(cat .pids.frontend)
  if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "Stopping frontend server (PID: $FRONTEND_PID)..."
    kill $FRONTEND_PID
  else
    echo "Frontend server is not running."
  fi
  rm .pids.frontend
else
  # Fallback method: use pkill
  echo "No PID file found for frontend. Attempting to stop with pkill..."
  pkill -f "node.*start" || true
fi

echo "Servers stopped." 