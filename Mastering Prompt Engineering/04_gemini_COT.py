# Understanding Chain of Thoughts step by step

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

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
Output: {{step:"analyse", content:"The user is intersted in a math query and asking a basic arithmatic operation."}}
Output: {{step:"think", content:"To perform this operation, i must go from left to right and add all of the operands.}}
Output: {{step:"output", content:"4"}}
Output: {{step:"validate", content:"Seems like 4 is correct answer for 2 + 2"}}
Output: {{step:"result", content:"2 + 2 = 4 and that is calculated by adding all the given numbers"}}

"""

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-05-20",
    config=types.GenerateContentConfig(
        max_output_tokens=500,
        temperature=0.5,
        system_instruction=system_prompt,
        response_mime_type="application/json"
    ),
    contents='''
        {{"role": "user", "content": "What is 3 + 4 * 5"}},
        {{"role": "assistant", "content": {
            "step": "analyse",
            "content": "The user is asking to evaluate a mathematical expression: '3 + 4 * 5'. This involves both addition and multiplication."
            }
        }},
        {{"role": "assistant", "content": {
            "step": "think",
            "content": "To solve '3 + 4 * 5', I need to apply the order of operations (PEMDAS/BODMAS). Multiplication takes precedence over addition. Therefore, I will first calculate '4 * 5' and then add the result to '3'."
            }
        }},
        {{"role": "assistant", "content": {
            "step": "output",
            "content": "23"
            }
        }},
        {{"role": "assistant", "content": {
            "step": "validate",
            "content": "The calculation was 4 * 5 = 20, then 3 + 20 = 23. The output '23' is consistent with the correct order of operations (multiplication before addition)."
            }
        }},
        {{"role": "assistant", "content": {
            "step": "result",
            "content": "The expression 3 + 4 * 5 is evaluated by first performing the multiplication (4 * 5 = 20) and then the addition (3 + 20 = 23). Therefore, 3 + 4 * 5 = 23."
            }
        }}
    ''',
)


print(response.text)