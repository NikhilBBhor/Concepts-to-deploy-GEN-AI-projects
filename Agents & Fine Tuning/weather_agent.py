from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

def get_weather(city: str):
    # TODO!: Do an actual API call
    return "31 Degree Celcius"

system_prompt = """
You are a helpful AI assistant who is specialised in resolving user query.
You work on start, plan, action, observe mode.
For the given user query and available tools, plan the step step execution, based on planning.
Select the relevant tool from the availabl tool. And based on the tool selection you perform an action to call the tool.
Wait for the observation and based on the observation from the tool call resolve the user query.

Rules:
1. Follow the strict JSON output as per Output schema
2. Always perform one step at a time and wait for next input
3. carefully analyse the user query

Output JSON Format:
{{
    "step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "input": "The input parameter for the function"
}}

Example:
User Query: What is the weather of New York?
Output: {{"step": "Plan", "content": "The user is interested in weather data of New York"}}
Output: {{"step": "Plan", "content": "From the available tools I should call get_weather"}}
Output: {{"step": "Action", "function": "get_weather", "input": "New York"}}
Output: {{"step": "Observe", "output": "12 Degree Celsius"}}
Output: {{"step": "Output", "output": "The weather for New York seems to be 12 Degree Celsius"}}
"""

result = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content":"What is the current wheather in Pune?"},
        {"role": "assistant", "content": json.dumps({"step": "Plan", "content": "The user is interested in current weather data of Pune"})},
        {"role": "assistant", "content": json.dumps({"step": "Plan", "content": "From the available tools I should call get_weather"})},
        {"role": "assistant", "content": json.dumps({"step": "Action", "function": "get_weather", "input": "Pune"})},
        {"role": "assistant", "content": json.dumps({"step": "Observe", "output": "31 Degree Celcius"})}
    ]
)

print(result.choices[0].message.content)