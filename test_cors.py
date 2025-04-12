"""
Test script to verify API connectivity and CORS configuration.
This script simulates requests similar to those made by the browser.
"""

import requests
import json

def test_health_check():
    """Test the health check endpoint with CORS headers."""
    try:
        # Simulate a preflight OPTIONS request
        options_headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        options_response = requests.options(
            'http://localhost:5000/api/health',
            headers=options_headers
        )
        
        print(f"OPTIONS Response Status: {options_response.status_code}")
        print(f"OPTIONS Response Headers: {dict(options_response.headers)}")
        
        # Now make the actual GET request
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        response = requests.get(
            'http://localhost:5000/api/health',
            headers=headers
        )
        
        print(f"GET Response Status: {response.status_code}")
        print(f"GET Response Headers: {dict(response.headers)}")
        print(f"GET Response Body: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error in health check: {e}")
        return False

def test_chat_api():
    """Test the chat API endpoint with CORS headers."""
    try:
        # Simulate a preflight OPTIONS request
        options_headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        options_response = requests.options(
            'http://localhost:5000/api/chat',
            headers=options_headers
        )
        
        print(f"OPTIONS Response Status: {options_response.status_code}")
        print(f"OPTIONS Response Headers: {dict(options_response.headers)}")
        
        # Now make the actual POST request
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        data = {"message": "Hello, are you working?"}
        print(f"Sending test message: {data}")
        
        response = requests.post(
            'http://localhost:5000/api/chat',
            json=data,
            headers=headers
        )
        
        print(f"POST Response Status: {response.status_code}")
        print(f"POST Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"POST Response Body (truncated): {str(response.json())[:100]}...")
        else:
            print(f"POST Response Body: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error in chat API test: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing API Connectivity and CORS Configuration ===")
    
    print("\n--- Health Check Test ---")
    if test_health_check():
        print("✅ Health check passed!")
    else:
        print("❌ Health check failed!")
    
    print("\n--- Chat API Test ---")
    if test_chat_api():
        print("✅ Chat API test passed!")
    else:
        print("❌ Chat API test failed!")
    
    print("\n=== Testing Complete ===") 