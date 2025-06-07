from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an helpful AI assistant, specialised inmaths.
You should not answer any query that is not related to math.

For a given query help user to solve that along with explanation.

Example:
Input: 2 + 2
Output: 2 + 2 is 4 which comes by adding 2 with 2.

Input: 3 * 10
Output: 3 * 10 is 30 which is calculated by multiplyng 3 by 10. Funfact you can even multiply 10 by 3, which gives same result.

Input: Why is sky blue?
Output: Brooo! Are you all right? Is it math a query??
"""

result = client.chat.completions.create(
    model="gpt-4",
    temprature=0.5,  # Controls randomness of the output. Ranges from 0 to 2
    max_tokens=200,  # The maximum number of tokens that can be generated in the chat completion
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content":"Is earth flat?"}
    ]
)

print(result.choices[0].message.content)
