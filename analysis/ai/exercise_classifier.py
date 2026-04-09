import pandas as pd 
from analysis.ai.connection import ask_ai
from analysis.ai.prompt import ai_prompt

def classify_exercise(exercise: str) -> str:
    """Classify exercise name based on AI. Return the classification result from Ollama's chat as "upper", "lower" or 'unknown'."""
    response= ask_ai(ai_prompt(exercise))
    return response['message']['content'].strip().lower()
