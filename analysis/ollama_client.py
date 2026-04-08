import requests
from config import OLLAMA_API, OLLAMA_MODEL


def call_ollama(prompt: str) -> str:
    """
    Send a prompt to the Ollama API and return the response.

    Args:
        prompt (str): The LLM prompt.

    Returns:
        str: The model's response text.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    resp = requests.post(OLLAMA_API, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json().get("response", "").strip()
