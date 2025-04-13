# AI Cover Letter Generator

An AI-powered tool that generates customized cover letters based on job descriptions and your CV.

## Features

- **Intelligent Cover Letter Generation**: Automatically creates tailored cover letters based on job descriptions
- **CV Integration**: Uses your existing CV to personalize cover letters
- **PDF Export**: Download professional-looking PDFs of your cover letters
- **Editable Results**: Modify the generated content before downloading
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Frontend**: React with TypeScript, Tailwind CSS
- **Backend**: Flask (Python)
- **AI Integration**: Google's Gemini AI

## Preview

1. Home Page
<img width="1440" alt="Screenshot 2025-04-13 at 9 43 01 PM" src="https://github.com/user-attachments/assets/245df06d-f27b-4e79-ac74-8c4c3044dd97" />

2. Cover Letter Generator Page
<img width="1437" alt="Screenshot 2025-04-13 at 9 42 54 PM" src="https://github.com/user-attachments/assets/42225586-d1e1-4135-96d8-0dae9cb8a8ff" />


## Running the Application

### Option 1: Using Docker (Recommended)

Prerequisites:
- Docker and Docker Compose installed

Steps:
1. Clone the repository
2. Make sure your CV file is in the root directory (default: `cv.pdf`)
3. Run the application:
   ```
   ./docker-start.sh
   ```
4. The application will be available at:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5001/api/health

To stop the application:
```
./docker-stop.sh
```

### Option 2: Manual Setup

Prerequisites:
- Node.js (v14+)
- Python (v3.8+)
- Google Gemini AI API key

Steps:
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-cover-letter-generator.git
   cd ai-cover-letter-generator
   ```

2. Setup environment variables:
   
   Create a `.env` file in the root directory with the following content:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   CV_FILENAME=cv.pdf
   ```

3. Set up the backend:
   ```
   pip install -r requirements.txt
   ```

4. Set up the frontend:
   ```
   cd ai-chat-ui
   npm install
   ```

5. Add your CV file to the server root directory. The filename should match what you've specified in the CV_FILENAME environment variable (defaults to `cv.pdf`).

### Running the Application Manually

Use the provided scripts to start the application:

```
./restart.sh
```

This will start both the Flask backend server and React frontend.

- Backend will be available at: http://localhost:5001
- Frontend will be available at: http://localhost:3000

To stop the application:

```
./stop.sh
```

## Usage

1. Enter the job details in the form:
   - Position
   - Company name
   - About the company (optional)
   - Job description

2. Click "Generate Cover Letter"

3. The AI will generate a tailored cover letter based on your CV and the job description

4. Edit the cover letter as needed

5. Download it as a PDF or copy to clipboard

## Troubleshooting

- If you encounter a "CV Loading Error," ensure your CV file (as specified in CV_FILENAME) is in the root directory of the server.
- For API connection issues, check that your GEMINI_API_KEY is correctly set in the .env file.

## License

MIT 
