from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

text = "The cat sat on the mat"

response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
)

print("Embedings:", response.data[0].embedding)
