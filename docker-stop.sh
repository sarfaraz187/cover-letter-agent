#!/bin/bash

echo "Stopping AI Cover Letter Generator Docker containers..."
docker-compose down

if [ $? -eq 0 ]; then
    echo "✅ All containers have been stopped successfully."
else
    echo "❌ There was an issue stopping the containers."
    echo "Please check with 'docker ps' to see if any containers are still running."
fi 