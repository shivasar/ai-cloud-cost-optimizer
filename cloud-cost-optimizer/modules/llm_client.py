import os
import requests
import json
import re
from dotenv import load_dotenv
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://router.huggingface.co/v1/chat/completions"
# Using a reliable model like Llama-3-8B-Instruct
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
def query_llm(messages, max_tokens=1000, temperature=0.1):
    if not HF_API_TOKEN:
        raise ValueError("HF_API_TOKEN not found in .env")
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_ID,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise ValueError(f"API Error: {response.text}")
        
    data = response.json()
    return data["choices"][0]["message"]["content"]
def extract_json_from_text(text):
    # Regex to find JSON block
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Fallback: simple brace matching
        start = text.find('{')
        end = text.rfind('}') + 1
        if start == -1 or end == 0: return None
        json_str = text[start:end]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None