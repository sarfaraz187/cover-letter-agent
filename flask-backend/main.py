import google.generativeai as genai
from google.api_core import retry
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv
from embedder import get_client, embed_cv, query_collection, GeminiEmbeddingFunction

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Step 2: Create a model client
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

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

# Step 1: Authenticate
genai.configure(api_key=api_key)

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

    logger.info(f"Message: {message}")
    # Relevant experience and skills for a {job_title} position at {company_name}.
    # The job requires: {job_requirements}.
    chroma_client = get_client()
    embedding_function = GeminiEmbeddingFunction() 
    collection = chroma_client.get_or_create_collection(name="resumeDB", embedding_function=embedding_function)
    results = query_collection(collection, message)
    matched_chunks = [doc for doc in results['documents'][0]]

    logger.info(f"Matched chunks: {matched_chunks}")

    if not message:
        return jsonify({'error': 'No job details provided'}), 400
    
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
        You are an expert in writing tailored cover letters. Given a resume and a job description, write a customized, professional, and engaging cover letter.
        
        ### Example 1:
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

        
        ### Now Your Turn:
        **Resume:**
        {matched_chunks}
        
        **Job Description (Summary):**
        {message}
        
        """
        
        prompt += f"""
        Write a compelling and concise cover letter (max 450 words).

        It should:

        1. Start with an attention-grabbing and personalized opening
        2. Highlight my relevant experience from my resume, including:
            - Work at Learnship GmbH (HALO, Elevate, Solo platforms)
            - React + TypeScript npm library for MyRA Web at SevenCs
            - Use of testing frameworks (Testing Library, Cypress)
        3. Address key job requirements like:
            - Strong JavaScript/TypeScript and React skills
            - Writing DRY, maintainable code
            - Familiarity with Git, HTML, CSS, testing
        4. Include a concrete example of overcoming a technical challenge (e.g. integrating a third-party mapping library)
        5. Emphasize my strengths:
            - Collaborative mindset
            - Passion for scalable and user-friendly solutions
            - Growth mindset toward technical leadership
        6. Explain why I want to join ePages specifically (their mission to empower SMBs, focus on innovation, e-commerce impact)
        7. Clearly state:
            - I hold a valid work permit, am available to relocate
            - Fluent in English, intermediate German

        End professionally with a closing paragraph

        Use this format for the closing:

        Sincerely,
        Mohammed Sarfaraz
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
    
    logger.info(f"Message: {message}")
    logger.info(f"CV Data: {cv_data}")

    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        logger.info(f"Processing cover letter request")
        
        # Set up the model configuration
        generation_config = {
            "max_output_tokens": 1048,
            "temperature": 0.4,
            "top_p": 0.90
        }

        # Prepare content based on request type
        # Create a structured prompt for cover letter generation
        prompt = f"""
        I need to write a cover letter for a job application. Here's information about me:
        
        My CV/Resume:
    
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

# This API will check if the CV is present in the Chroma DB
@app.route('/api/get-cv', methods=['GET', 'OPTIONS'])
def get_cv():
    """Check if embedded CV is present in Chroma DB"""
    if request.method == 'OPTIONS':
        return '', 204

    logger.info("CV presence check in ChromaDB initiated")

    try:
        chroma_client = get_client()
        collection = chroma_client.get_or_create_collection(name="resumeDB")

        count = collection.count()
        logger.info(f"Found {count} embedded document(s) in resumeDB")

        if count == 0:
            return jsonify({'embedded': False, 'message': 'No CV found in Chroma DB'}), 200
        else:
            return jsonify({'embedded': True, 'message': f'{count} document(s) found in Chroma DB'}), 200

        # Optional: If you stored with a known ID, you can use .get() instead:
        # result = collection.get(ids=["cv-main"])
        # if result["documents"] and result["documents"][0] is not None:
        #     return jsonify({'embedded': True}), 200

    except Exception as e:
        logger.exception(f"Error checking Chroma DB: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.after_request
def after_request(response):
    """Log response details after each request"""
    logger.info(f"Response status: {response.status}")
    logger.info(f"Response headers: {response.headers}")
    return response

if __name__ == '__main__':
    embed_cv()
    logger.info("Starting Flask API server...")
    app.run(debug=True, port=5001, host='0.0.0.0')