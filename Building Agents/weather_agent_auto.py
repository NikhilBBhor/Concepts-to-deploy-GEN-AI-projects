from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
import os

load_dotenv()

client = OpenAI()

def run_command(command):
    result = os.system(command=command)
    return result

def get_weather(city: str):
    # TODO!: Do an actual API call
    url = f'https://wttr.in/{city}?format=%C+%t'
    weather = requests.get(url)

    if weather.status_code == 200:
        print("Tool called: get_weather")
        return weather.text
    return "Something went wrong!"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output"
    }
}

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

Available Tools:
- get_weather: Takes city name as an input and returns the current weather for the city
- run_command: Takes a command as input to execute on system and returns output

Example:
User Query: What is the weather of New York?
Output: {{"step": "plan", "content": "The user is interested in weather data of New York"}}
Output: {{"step": "plan", "content": "From the available tools I should call get_weather"}}
Output: {{"step": "action", "function": "get_weather", "input": "New York"}}
Output: {{"step": "observe", "output": "12 Degree Celsius"}}
Output: {{"step": "output", "content": "The weather for New York seems to be 12 Degree Celsius"}}
"""

messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_query = input("--> ")
    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

        if parsed_output.get("step") == "plan":
            print(f"Processing: {parsed_output.get("content")}")
            continue

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                continue

        if parsed_output.get("step") == "output":
            print("AI:", parsed_output.get("content"))
            break