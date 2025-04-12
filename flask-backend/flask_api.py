from flask import Flask, request, jsonify
from flask_cors import CORS
from google import generativeai as genai
import logging
import os
import PyPDF2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS with explicit settings
cors_headers = {
    "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "https://cover-letter-generator-mu.vercel.app"],
    "methods": ["GET", "POST", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True,
    "max_age": 3600
}
CORS(app, resources={r"/api/*": cors_headers})

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logger.error("No API key found. Please set the GOOGLE_API_KEY environment variable.")
    raise ValueError("No API key found. Please set the GOOGLE_API_KEY environment variable.")

# Get CV filename from environment variable or use default
cv_filename = os.getenv('CV_FILENAME', 'cv.pdf')
logger.info(f"Using CV filename: {cv_filename}")

# Initialize Gemini AI with your API key
logger.info("Configuring Gemini AI...")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

<<<<<<< HEAD:flask_api.py
=======
# ======================= RAG Implementation ==================
# Define a helper to retry when per-minute quota is reached.
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries
    document_mode = True

    @retry.Retry(predicate=is_retriable)
    def __call__(self, input: Documents) -> Embeddings:
        embedding_task = "retrieval_document" if self.document_mode else "retrieval_query"

        results = []
        
        # Handle single string or list input
        texts = [input] if isinstance(input, str) else input
        
        for text in texts:
            response = genai.embed_content(
                model="text-embedding-004",
                content=text,
                task_type=embedding_task
            )
            # The response is a dictionary with an "embedding" key
            results.append(response["embedding"])
            
        return results

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


# Read the CV file
cv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cv_filename)
if not os.path.exists(cv_path):
    logger.error(f"CV file not found at {cv_path}")
    raise FileNotFoundError(f"CV file not found at {cv_path}")
cv_text = extract_text_from_pdf(cv_path)
logger.info(f"Successfully extracted {len(cv_text)} characters from CV")

# Combine CV and job description into a single document
documents = [cv_text]

# Embedding process
embed_fn = GeminiEmbeddingFunction()
embed_fn.document_mode = True

# PersistentClient and assign it
chroma_client = chromadb.PersistentClient(path=os.path.join('flask-backend', "chroma_db"))

# Optional: print the resolved absolute path
print("------ Path to my DB ----->", os.path.abspath(os.path.join('flask-backend', "chroma_db")))

db = chroma_client.get_or_create_collection(name="resumeDB", embedding_function=embed_fn)

db.add(documents=documents, ids=[str(i) for i in range(len(documents))])

print("Here is my collections in DB :", db.count())

# ============================= END ===========================

# Since there is no cache for example like a redis to store the CV data, we will read it from the file each time and pass it to the model
# There is no explicit context window being defined in the technical sense.
>>>>>>> b143ec9 (commented out the API to fetch cv_data and moved it to be stored in the vector DB):flask-backend/flask_api.py
@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def cover_letter():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 204
    
    logger.info(f"Received request: {request.method} {request.path}")
    logger.info(f"Request headers: {request.headers}")
    
    data = request.json
    logger.info(f"Request data: {data}")
    
    message = data.get('message', '')
    cv_data = data.get('cv_data', '')
    is_cover_letter = data.get('is_cover_letter', False)
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        logger.info(f"Processing cover letter request")
        
        # Set up the model configuration
        generation_config = {
<<<<<<< HEAD:flask_api.py
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_p": 0.95
=======
            "max_output_tokens": 1024, # 1024 tokens is approximately 800 words
            "temperature": 0.4,
            "top_p": 0.90
>>>>>>> b143ec9 (commented out the API to fetch cv_data and moved it to be stored in the vector DB):flask-backend/flask_api.py
        }
        
        # Prepare content based on request type
        if is_cover_letter and cv_data:
            # Create a structured prompt for cover letter generation
            prompt = f"""
            I need to write a cover letter for a job application. Here's information about me:
            
            My CV/Resume:
            {cv_data}
            
            Job Details:
            {message}
            
            """
            
            prompt += """
            Write a compelling cover letter that:
            1. Has an attention-grabbing opening
            2. Highlights my relevant experience from my resume
            3. Addresses key requirements mentioned in the job description
            4. Includes a specific example of how I overcame a challenge in a previous role
            5. Emphasizes my unique selling points 
            6. Explains why I'm passionate about joining this specific company
            8. Add a personal touch. 
            7. Mentions I am available to relocate with a valid work permit and have fluent English and intermediate German
            8. Limit to 350 words maximum
            
            Structure the letter professionally with proper greeting and closing.
            """
            
            contents = prompt
        else:
            contents = message
        
        # Get a response from Gemini
        response = model.generate_content(
            contents=contents,
            generation_config=generation_config
        )
        
        # Handle different response formats
        response_text = ""
        if hasattr(response, 'text'):
            response_text = response.text
        elif hasattr(response, 'parts'):
            response_text = ' '.join([part.text for part in response.parts if hasattr(part, 'text')])
        else:
            response_text = str(response)
            
        logger.info(f"AI response (truncated): {response_text[:100]}...")
        
        return jsonify({'response': response_text})
    except Exception as e:
        logger.exception(f"Error generating response: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    """Health check endpoint"""
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 204
        
    logger.info("Health check request received")
    return jsonify({
        'status': 'ok', 
        'api_key_configured': bool(api_key),
        'cors_configured': True,
        'origins_allowed': cors_headers['origins']
    })

# This has been commented out as now i am using a RAG to reference the CV data
# @app.route('/api/get-cv', methods=['GET', 'OPTIONS'])
# def get_cv():
#     """Endpoint to read CV from PDF file"""
#     if request.method == 'OPTIONS':
#         # Handle preflight request
#         return '', 204
    
#     logger.info("CV request received")
#     cv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cv_filename)
#     logger.info("~~~~~~~~~~~~", cv_path)
#     try:
#         if not os.path.exists(cv_path):
#             logger.error(f"CV file not found at {cv_path}")
#             return jsonify({'error': f'CV file not found. Please ensure {cv_filename} is in the root directory.'}), 404
        
#         # Extract text from PDF
#         cv_text = ""
#         with open(cv_path, 'rb') as file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             for page_num in range(len(pdf_reader.pages)):
#                 page = pdf_reader.pages[page_num]
#                 cv_text += page.extract_text()
        
#         logger.info(f"Successfully extracted {len(cv_text)} characters from CV")
#         return jsonify({'content': cv_text})
    
#     except Exception as e:
#         logger.exception(f"Error reading CV: {str(e)}")
#         return jsonify({'error': str(e)}), 500

@app.route('/api/cover-letter', methods=['POST', 'OPTIONS'])
def generate_cover_letter():
    """Dedicated endpoint for cover letter generation"""
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 204
    
    logger.info(f"Received cover letter request: {request.method} {request.path}")
    logger.info(f"Request headers: {request.headers}")
    
    data = request.json
    logger.info(f"Request data: {data}")
    
    message = data.get('message', '')
    cv_data = data.get('cv_data', '')
    
    if not message:
        return jsonify({'error': 'No job details provided'}), 400
    
    if not cv_data:
        return jsonify({'error': 'No CV data provided'}), 400
    
    try:
        logger.info(f"Processing cover letter request")
        
        # Set up the model configuration
        generation_config = {
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_p": 0.95
        }
        
        # Create a structured prompt for cover letter generation
        prompt = f"""
        I need to write a cover letter for a job application. Here's information about me:
        
        My CV/Resume:
        {cv_data}
        
        Job Details:
        {message}
        
        """
        
        prompt += """
        Write a compelling cover letter that:
        1. Has an attention-grabbing opening
        2. Highlights my relevant experience from my resume
        3. Addresses key requirements mentioned in the job description
        4. Includes a specific example of how I overcame a challenge in a previous role
        5. Emphasizes my unique selling points 
        6. Explains why I'm passionate about joining this specific company
        7. Mentions I am available to relocate with a valid work permit and have fluent English and intermediate German
        8. Limit to 350 words maximum
        
        Structure the letter professionally with proper greeting and closing.
        """
        
        # Get a response from Gemini
        response = model.generate_content(
            contents=prompt,
            generation_config=generation_config
        )
        
        # Handle different response formats
        response_text = ""
        if hasattr(response, 'text'):
            response_text = response.text
        elif hasattr(response, 'parts'):
            response_text = ' '.join([part.text for part in response.parts if hasattr(part, 'text')])
        else:
            response_text = str(response)
            
        logger.info(f"AI response (truncated): {response_text[:100]}...")
        
        return jsonify({'response': response_text})
    except Exception as e:
        logger.exception(f"Error generating cover letter: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.after_request
def after_request(response):
    """Log response details after each request"""
    logger.info(f"Response status: {response.status}")
    logger.info(f"Response headers: {response.headers}")
    return response

if __name__ == '__main__':
    logger.info("Starting Flask API server...")
    app.run(debug=True, port=5001, host='0.0.0.0')