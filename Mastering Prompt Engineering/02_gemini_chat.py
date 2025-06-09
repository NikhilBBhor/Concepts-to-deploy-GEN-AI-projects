from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-05-20",
    contents="Why is the sky blue?",
)

print(response.text)