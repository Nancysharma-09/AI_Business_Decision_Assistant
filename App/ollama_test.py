import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")

url = "https://ollama.com/api/chat"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-oss:20b",
    "messages": [
        {
            "role": "user",
            "content": "Which country generated the highest revenue?"
        }
    ],
    "stream": False
}

print("\n========== REQUEST ==========")
print("URL:", url)
print("Model:", data["model"])
print("User question:", data["messages"][0]["content"])

response = requests.post(
    url,
    headers=headers,
    json=data
)

print("\n========== RESPONSE ==========")
print("Status code:", response.status_code)
print("Response:")
print(response.text)