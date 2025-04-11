"""
Test script to verify backend connectivity.
Run this script to check if your Flask backend is running and accessible.
"""

import requests
import json

API_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Health check status code: {response.status_code}")
        print(f"Health check response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def test_chat_api():
    """Test the chat API endpoint."""
    try:
        data = {"message": "Hello, are you working?"}
        print(f"Sending test message: {data}")
        
        response = requests.post(
            f"{API_URL}/chat", 
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Chat API status code: {response.status_code}")
        if response.status_code == 200:
            print(f"Chat API response (truncated): {response.json().get('response', '')[:100]}...")
        else:
            print(f"Chat API error response: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Chat API error: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend connectivity...")
    
    if test_health_check():
        print("✅ Health check passed!")
    else:
        print("❌ Health check failed!")
    
    if test_chat_api():
        print("✅ Chat API test passed!")
    else:
        print("❌ Chat API test failed!") 