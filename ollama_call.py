import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3-vl:4b"

def call_qwen_vl(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "top_p": 0.9},
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=600)
    resp.raise_for_status()
    return resp.json()["response"]

if __name__ == "__main__":
    print(call_qwen_vl("Return JSON only"))
