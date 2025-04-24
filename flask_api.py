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

# Since there is no cache for example like a redis to store the CV data, we will read it from the file each time and pass it to the model
# There is no explicit context window being defined in the technical sense.
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
            "max_output_tokens": 1024, # 1024 tokens is approximately 800 words
            "temperature": 0.2,
            "top_p": 0.90
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
            8. Limit to 380 words maximum
            
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
            
        # logger.info(f"AI response (truncated): {response_text[:100]}...")
        
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

@app.route('/api/get-cv', methods=['GET', 'OPTIONS'])
def get_cv():
    """Endpoint to read CV from PDF file"""
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 204
    
    logger.info("CV request received")
    cv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cv_filename)
    logger.info("~~~~~~~~~~~~", cv_path)
    try:
        if not os.path.exists(cv_path):
            logger.error(f"CV file not found at {cv_path}")
            return jsonify({'error': f'CV file not found. Please ensure {cv_filename} is in the root directory.'}), 404
        
        # Extract text from PDF
        cv_text = ""
        with open(cv_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                cv_text += page.extract_text()
        
        logger.info(f"Successfully extracted {len(cv_text)} characters from CV")
        return jsonify({'content': cv_text})
    
    except Exception as e:
        logger.exception(f"Error reading CV: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
        
        Example Cover Letter:

        Dear Hiring Team,
        When I reduced customer onboarding time by 45% through an intuitive internal application at
        Onestoptransformation, I witnessed firsthand how thoughtful frontend engineering directly impacts user
        experience. This powerful connection between code and human wellbeing aligns perfectly with
        Gymondo's mission of helping people lead healthier lives through accessible digital fitness solutions.

        My frontend development journey includes:
        ● Professional experience with React, Vue.js, TypeScript and JavaScript
        ● Designing UI components and establishing TypeScript-based npm libraries at SevenCs
        ● Implementing robust validation and testing mechanisms for reliable application performance
        ● Integrating and consuming REST APIs across multiple production applications
        ● Collaborating with cross-functional teams to translate user needs into technical solutions

        At SevenCs, I developed MyRA Web, a digital routing service enhancing maritime navigation, where I
        created robust UI components while maintaining a keen focus on user experience. This project
        demanded clean, maintainable code that could reliably display complex real-time data—skills directly
        transferable to developing engaging fitness interfaces at Gymondo.

        During my time at Learnship GmbH, I contributed to feature development for multiple platforms while
        modernizing legacy systems. This experience taught me to balance innovation with
        maintainability—creating code that not only works but scales efficiently. I became adept at refactoring
        existing codebases while adding new functionality, a valuable skill for evolving applications.
        My internship at Onestoptransformation provided hands-on experience setting up CI/CD pipelines and
        writing comprehensive test cases, demonstrating my commitment to code quality and standardized
        practices. I embraced peer code reviews as opportunities for growth, refining my ability to both give and
        receive constructive feedback—an essential aspect of Gymondo's collaborative development culture.

        I'm particularly excited about Gymondo's commitment to continuous learning and growth, as I
        consistently seek out opportunities to expand my technical knowledge and stay current with frontend
        innovations. Your collaborative approach to development, including code reviews and team
        problem-solving, resonates with my own development philosophy of learning through shared expertise.
        
        I am available to relocate as needed, hold a valid work permit, and am fluent in English with intermediate
        German proficiency. I would welcome the opportunity to discuss how my technical skills and passion for
        creating impactful user experiences could contribute to Gymondo's mission of helping people lead
        healthier lives through engaging digital fitness solutions.

        Sincerely,
        Mohammed Sarfaraz

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
        response = model.generate_content(contents=prompt, generation_config=generation_config)
        
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