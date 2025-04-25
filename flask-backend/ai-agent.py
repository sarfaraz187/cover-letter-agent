# from groq import Groq
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Get Groq API key from environment variable
# groq_api_key = os.getenv('GROQ_API_KEY')
# if groq_api_key:
#     client = Groq(api_key=groq_api_key)
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Explain the importance of fast language models",
#             }
#         ],
#         model="llama-3.3-70b-versatile",
#     )
#     print(chat_completion.choices[0].message.content)

from google import genai
from google.genai import types
import markdown
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")

client = genai.Client(api_key=api_key)

model_config = types.GenerateContentConfig(
    max_output_tokens=50, 
    temperature=1.0, 
    top_p=0.95 
    )

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=model_config,
    contents="Explain AI to me like I'm a kid.")

print(markdown.markdown(response.text))

# print(client)
# chat = client.chats.create(model='gemini-2.0-flash', history=[])
# response = chat.send_message('Hello! My name is Zlork.')

# print(response.text)