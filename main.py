import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api key not found")

client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()



messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

generated_content = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)

if generated_content.usage_metadata is None:
    raise RuntimeError("failed api request")

function_results = []

if args.verbose == True:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}")
    if generated_content.function_calls != None:
        for item in generated_content.function_calls:
            function_result = call_function(item, verbose=args.verbose)

            if not function_result.parts:
                raise Exception("Function call returned no parts")
            part = function_result.parts[0]

            if part.function_response is None:
                raise Exception("Function call returned no function_response")
            
            if part.function_response.response is None:
                raise Exception("Function call returned no response")
            
            function_results.append(part)

            if args.verbose:
                print(f"-> {part.function_response.response}")
    else:
        print(generated_content.text)
if args.verbose == False:
    if generated_content.function_calls != None:
        for item in generated_content.function_calls:
            print(f'Calling function: {item.name}({item.args})')
    else:
        print(generated_content.text)
