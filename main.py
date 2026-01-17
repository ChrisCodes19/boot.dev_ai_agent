import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("api key not found")
client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

generated_content = client.models.generate_content(model="gemini-2.5-flash", contents=args.user_prompt)
if generated_content.usage_metadata is None:
    raise RuntimeError("failed api request")
print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}")
print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}")
print(generated_content.text)



















