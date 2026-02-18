import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Use the chat completions endpoint with GPT-4o (supports image generation)
url = "https://models.inference.ai.azure.com/chat/completions"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

prompt = input("Enter your image prompt: ")

payload = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": f"Generate an image of: {prompt}"
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    message = data["choices"][0]["message"]
    print("\nResponse received!")
    print(message.get("content", "No text content"))
else:
    print(f"Error ({response.status_code}):", response.text)
