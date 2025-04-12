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

## Setup

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- Google Gemini AI API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-cover-letter-generator.git
   cd ai-cover-letter-generator
   ```

2. Setup environment variables:
   
   Create a `.env` file in the root directory with the following content:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
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

5. Add your CV (must be named `mohammed_sarfaraz_cv.pdf`) to the server root directory.

### Running the Application

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

- If you encounter a "CV Loading Error," ensure your CV file (mohammed_sarfaraz_cv.pdf) is in the root directory of the server.
- For API connection issues, check that your GEMINI_API_KEY is correctly set in the .env file.

## License

MIT 