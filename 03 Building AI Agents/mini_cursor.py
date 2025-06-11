from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os

load_dotenv()

client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    
    return "Something went wrong"


available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "get_weather": Takes a city name as an input and returns the current weather for the city
    - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.

    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

"""

messages = [
  { "role": "system", "content": SYSTEM_PROMPT }
]

while True:
    query = input("> ")
    messages.append({ "role": "user", "content": query })

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({ "role": "assistant", "content": response.choices[0].message.content })
        parsed_response = json.loads(response.choices[0].message.content)

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue

        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")

            if available_tools.get(tool_name) != False:
                output = available_tools[tool_name](tool_input)
                messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) })
                continue
        
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break


# Example ------------------------------------------------------------------------
"""
Input: “Create a simple TODO app in a dedicated folder with a modern dark theme”

Output: 

🧠: The user requests creation of a simple TODO app in a dedicated folder with a modern dark theme. The first step is to create a dedicated folder for the app. 

🧠: To create the folder, I should use the 'run_command' tool to execute a command that makes a new directory for the TODO app. 

🛠️: Calling Tool:run_command with input mkdir todo_app 

🧠: The folder 'todo_app' has been created. Next, I need to set up the basic files for a simple TODO app. Typically, the main files include index.html, style.css (for modern dark theme), and script.js. 

🧠: To set up the initial project structure, I should create index.html, style.css, and script.js files inside the 'todo_app' directory. This step can be handled with a Linux command. 

🛠️: Calling Tool:run_command with input touch todo_app/index.html todo_app/style.css todo_app/script.js 

🧠: The required files (index.html, style.css, script.js) have been created in the 'todo_app' directory. Now, I should populate index.html with a basic HTML structure that links to the CSS and JavaScript files. 

🧠: To add the basic HTML structure to index.html, including linking to style.css and script.js, I will use a Linux command with echo/redirection. 

🛠️: Calling Tool:run_command with input echo <HTML_CODE>

🧠: The index.html file now contains a basic structure for the TODO app. The next step is to create a modern dark theme style in style.css to ensure the app has a visually appealing dark mode appearance. 

🧠: I will now add modern dark theme CSS to the style.css file using a Linux command. 

🛠️: Calling Tool:run_command with input echo  <CSS_CODE> 

🧠: The modern dark theme CSS has been added to style.css. The next step is to implement the JavaScript logic in script.js to handle adding, toggling, and removing TODO list items. 

🧠: I will add JavaScript code to script.js that allows users to add, mark as completed, and delete TODO items, by responding to form events and dynamically manipulating the DOM. 

🛠️: Calling Tool:run_command with input echo  <JS_CODE>

🤖: Your simple TODO app with a modern dark theme has been created in the 'todo_app' folder. Open index.html in your browser to start using it! The app supports adding tasks, marking them as complete, and deleting them—all with a stylish dark mode.
"""