import requests
import json

url = "http://127.0.0.1:8000/content/generate"
payload = {
    "topic": "AI",
    "platform": "Linkedin",
    "tone": "professional",
    "target_audience": "business professionals"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
