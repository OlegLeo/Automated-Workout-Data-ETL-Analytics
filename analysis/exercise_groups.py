import json
import os
from config import GROUPED_EXERCISES_JSON_PATH

def load_grouped_exercises() -> dict:
    """Load exercise classification groups from JSON."""
    if not os.path.exists(GROUPED_EXERCISES_JSON_PATH):   # Checking file exists or no, based on the condition given in config module...      
        return {"upper": [], "lower": [], "unknown": []}   # Return default groups
    
    with open(GROUPED_EXERCISES_JSON_PATH,"r") as f:
        return json.load(f)
        

def save_grouped_exercises(groups: dict):
    """Save exercise classification groups to JSON."""   # Save the data in a file...      
    with open(GROUPED_EXERCISES_JSON_PATH,"w") as f:   # Opening and writing into json format.
        json.dump(groups,f, indent=4)