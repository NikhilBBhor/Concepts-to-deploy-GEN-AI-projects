# Fully functional automated COT (Chain of Thoughts)

from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistat who is expert in breaking down coplex problems and then resolve the user query.

For the given user input analyse the input and break down the problem step by step.
Think atleast 5-6 steps on how to solve the problem before answering.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "Analyse", "think", "output", "Validate" and finally "Result".

Rules:
1. Follow the strict JSON output as per Output schema
2. Always perform one step at a time and wait for next input
3. carefully analyse the user query

Example:
Input: What is 2 + 2
Output: {{step:"Analysing", content:"The user is intersted in a math query and asking a basic arithmatic operation."}}
Output: {{step:"Thinking", content:"To perform this operation, i must go from left to right and add all of the operands.}}
Output: {{step:"Output", content:"4"}}
Output: {{step:"Validating", content:"Seems like 4 is correct answer for 2 + 2"}}
Output: {{step:"Result", content:"2 + 2 = 4 and that is calculated by adding all the given numbers"}}

"""

messages=[
    {"role": "system", "content": system_prompt}
]

query = input("--> ")
messages.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

    if parsed_response.get("step") != "Result":
        print(f"{parsed_response.get("step")}: {parsed_response.get("content")}")
        continue

    print("Result:", parsed_response.get("content"))
    break


# output---------------------------------------------------------------------------------
"""
--> what came first? egg or chicken

Analysing: The user is inquiring about the philosophical and biological question concerning the origins of the chicken and the egg.

Thinking: To address this question, one needs to consider both evolutionary biology and philosophical perspectives.

Thinking: Biologically, species evolve over time through small mutations. We should consider that the chicken evolved from a non-chicken ancestor.

Thinking: The egg as a reproductive structure existed long before chickens, used by other species in evolution. Non-chickens laid eggs long before chickens existed.

Output: From the biological perspective, the egg came first, as it predates the existence of the chicken through evolutionary history.

Validating: This conclusion aligns with current scientific understanding of evolution and species development.

Result: Considering evolutionary biology, the egg came before the chicken as it is an ancestral reproductive mechanism that existed before chickens evolved. Therefore, the egg came first.
"""