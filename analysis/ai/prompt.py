def ai_prompt(exercise: str) -> str:
    """Return a valid Ollama chat message list."""
    
    return [
        {
            "role": "user",
            "content": (
                f"Based on the exercise name, respond with one word either its working specifically upper or lower body: {exercise}"
                "'upper', 'lower', or 'unknown'."
            )
        }
    ]
    