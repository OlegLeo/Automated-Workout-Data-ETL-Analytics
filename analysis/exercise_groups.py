import json
import os
from config import GROUPED_EXERCISES_JSON_PATH

def load_grouped_exercises() -> dict:
    """Load exercise classification groups from JSON, or create default structure."""
    if not os.path.exists(GROUPED_EXERCISES_JSON_PATH):   # Checking file exists or no, based on the condition given in config module...      
        # File does not exist yet -> create deafult structure
        return {"upper": [], "lower": [], "unknown": []}   # Return default groups
    
    try:
            
        with open(GROUPED_EXERCISES_JSON_PATH,"r") as f:
            content = f.read().strip()
            
            # File exists but its empty
            if content == "":
                return {"upper": [], "lower":[], "unknown": []}   # Return default groups if the content is empty
            
            # Try parsing JSON
            return json.loads(content) #
    except json.JSONDecodeError:
        # File exists but its not valid JSON -> create default structure 
        return  {"upper": [], "lower" :[], 'unknown': []}   # Return default

def save_grouped_exercises(groups: dict):
    """Save exercise classification groups to JSON."""   # Save the data in a file...      
    with open(GROUPED_EXERCISES_JSON_PATH,"w") as f:   # Opening and writing into json format.
        json.dump(groups,f, indent=4)