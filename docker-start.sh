#!/bin/bash

echo "Starting AI Cover Letter Generator with Docker..."

# Check if docker and docker-compose are installed
if ! command -v docker &> /dev/null; then
    echo "Error: docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Make sure CV file exists
CV_FILENAME=$(grep CV_FILENAME .env.docker | cut -d '=' -f2)
if [ ! -f "$CV_FILENAME" ]; then
    echo "Warning: CV file '$CV_FILENAME' not found!"
    echo "Make sure to add your CV file as specified in the .env.docker file."
    read -p "Continue anyway? (y/n): " continue_anyway
    if [ "$continue_anyway" != "y" ]; then
        exit 1
    fi
fi

# Build and start containers
echo "Building and starting containers..."
docker-compose up --build -d

# Check if containers are running
echo "Checking if services are running..."
sleep 5

if docker-compose ps | grep -q "Up"; then
    echo "✅ Docker containers are running successfully!"
    echo ""
    echo "Your application is now available at:"
    echo "- Frontend: http://localhost:3000"
    echo "- Backend API: http://localhost:5001/api/health"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop the application: docker-compose down"
else
    echo "❌ Something went wrong. Containers are not running properly."
    echo "Check logs with: docker-compose logs -f"
fi 