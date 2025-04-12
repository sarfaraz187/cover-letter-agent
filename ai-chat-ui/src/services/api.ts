// Set the API base URL based on environment
// Try to use the variable from the root .env file if available
<<<<<<< HEAD
import { ICvDataResponse } from "../types/index";
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5001/api";
=======
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5001/api";

>>>>>>> b143ec9 (commented out the API to fetch cv_data and moved it to be stored in the vector DB)
/**
 * Fetch CV data from the server
 *
 * @returns The CV data as text
 */

export const fetchCvData = async (): Promise<ICvDataResponse> => {
  try {
    console.log(`API Request - Fetching CV data`);

    const response = await fetch(`${API_BASE_URL}/get-cv`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    console.log("API Response - Status:", response.status);

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `Error: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error("API Error:", error);
    const errorMessage = error instanceof Error ? error.message : "Failed to fetch CV data. Please try again later.";
    throw new Error(errorMessage);
  }
};

/**
 * Generate a cover letter using the AI based on CV and job description
 *
 * @param jobDescription The job description or position
 * @param cvData The user's CV/resume data
 * @returns The generated cover letter
 */
<<<<<<< HEAD
export const generateCoverLetter = async (jobDescription: string): Promise<string> => {
=======
export const generateCoverLetter = async (jobDescription: string, cvData: string): Promise<string> => {
>>>>>>> b143ec9 (commented out the API to fetch cv_data and moved it to be stored in the vector DB)
  try {
    console.log(`API Request - Generating cover letter...`);

    // Check if the backend is reachable first
    try {
      const healthCheck = await fetch(`${API_BASE_URL}/health`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (!healthCheck.ok) {
        console.error("Health check failed:", await healthCheck.text());
        throw new Error("Backend API is not accessible. Please check if the server is running.");
      }
    } catch (healthError) {
      console.error("Health check error:", healthError);
      throw new Error("Failed to connect to the backend. Please check if the server is running and accessible.");
    }

    // Proceed with the cover letter generation API call
    const response = await fetch(`${API_BASE_URL}/cover-letter`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
<<<<<<< HEAD
      body: JSON.stringify({ message: jobDescription }),
=======
      body: JSON.stringify({ message: jobDescription, cv_data: cvData }),
>>>>>>> b143ec9 (commented out the API to fetch cv_data and moved it to be stored in the vector DB)
    });

    console.log("API Response - Status:", response.status);

    const data = await response.json();
    console.log("API Response - Data (truncated):", {
      ...data,
      response: data.response?.substring(0, 100) + "...",
    });

    if (!response.ok) throw new Error(data.error || `Error: ${response.status}`);

    return data.response;
  } catch (error) {
    console.error("API Error:", error);
    const errorMessage = error instanceof Error ? error.message : "Failed to generate cover letter. Please try again later.";
    throw new Error(errorMessage);
  }
};
