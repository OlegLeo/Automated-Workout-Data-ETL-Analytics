def ai_prompt(exercise: str):
    return [
        {
            "role": "user",
            "content": (
                "You are a strict classifier.\n"
                "Respond with EXACTLY one word from this list:\n"
                "upper\n"
                "lower\n"
                "unknown\n\n"
                "Rules:\n"
                "- Output must be exactly one of those words.\n"
                "- No punctuation.\n"
                "- No explanations.\n"
                "- No explanation or additonal notes.\n"
                "- No sentences.\n"
                "- No extra words.\n"
                "- No quotes.\n"
                "- No parentheses.\n\n"
                f"Exercise: {exercise}\n"
                "Output:"
            )
        }
    ]
