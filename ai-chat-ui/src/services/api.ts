// Set the API base URL based on environment
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Send a message to the AI and get a response
 * 
 * @param message The user's message
 * @returns The AI's response
 */
export const sendMessage = async (message: string): Promise<string> => {
  try {
    console.log(`API Request - Sending message to ${API_BASE_URL}/chat:`, message);
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    console.log('API Response - Status:', response.status);
    
    const data = await response.json();
    console.log('API Response - Data:', data);
    
    if (!response.ok) {
      throw new Error(data.error || `Error: ${response.status}`);
    }

    return data.response;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Initialize a new chat session
 * 
 * @returns The session ID
 */
export const createChatSession = async (): Promise<string> => {
  try {
    console.log(`API Request - Creating session at ${API_BASE_URL}/sessions`);
    const response = await fetch(`${API_BASE_URL}/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('API Response - Status:', response.status);
    
    const data = await response.json();
    console.log('API Response - Data:', data);
    
    if (!response.ok) {
      throw new Error(data.error || `Error: ${response.status}`);
    }

    return data.sessionId;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}; 