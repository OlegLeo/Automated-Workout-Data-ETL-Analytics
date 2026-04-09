from ollama import Client
from config import OLLAMA_API, OLLAMA_MODEL

client = Client(
    host=OLLAMA_API
)


def ask_ai(messages: list[dict]) -> str:
  """Ask local Ollama API about exercise input, returns JSON object containing all messages from server (chat log)."""
  response = client.chat(
    model=OLLAMA_MODEL, # Model
    messages=messages,  # Prompt
    stream=False        # Streaming or not? (default False). If set to True the chat will be returned in real time. Default is false and it's recommended when we want a live conversation with your bot
  )
  print(response)
  return response