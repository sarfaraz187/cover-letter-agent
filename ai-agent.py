# from groq import Groq

# client = Groq(api_key="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")

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama-3.3-70b-versatile",
# )

# print(chat_completion.choices[0].message.content)

from google import genai
from google.genai import types
import markdown

client = genai.Client(api_key="AIzaSyC6ruGAJ2Xeaa3ZqAZsDfdYEUxl6P75MmM")

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