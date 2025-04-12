# AI Cover Letter Generator

An AI-powered application that generates personalized cover letters based on your CV and job descriptions.

## Features

- **PDF CV Integration**: Automatically extracts text from your CV in PDF format
- **Tailored Cover Letters**: Generates professional cover letters that match job requirements
- **Simple Interface**: Easy-to-use UI for entering job details
- **Copy to Clipboard**: Quick copy function for your generated cover letters

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-cover-letter-generator.git
   cd ai-cover-letter-generator
   ```

2. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

4. Place your CV in PDF format in the root directory with the name `mohammed_sarfaraz_cv.pdf` (or update the file path in `flask_api.py`)

5. Install frontend dependencies:
   ```
   cd ai-chat-ui
   npm install
   ```

## Running the Application

You can use the provided scripts to run both the backend and frontend:

```
./restart.sh
```

Or run them individually:

- Backend: `python3 flask_api.py`
- Frontend: `cd ai-chat-ui && npm start`

Visit `http://localhost:3000` to use the application.

## How to Use

1. Enter the position you're applying for
2. Add the company name
3. (Optional) Include details about the company 
4. Paste the job description
5. Click "Generate Cover Letter"
6. Copy the generated cover letter to your clipboard

## Technologies Used

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Flask (Python)
- **AI**: Google Gemini AI
- **PDF Processing**: PyPDF2

## License

MIT 