from analysis.exercise_groups import load_grouped_exercises
from analysis.exercise_groups import save_grouped_exercises
from analysis.ai.exercise_classifier import classify_exercise
import logging

logger = logging.getLogger(__name__)   # Logger for this module.

def update_groups_from_df(df):
    """Update exercise groups from DataFrame using AI classification."""
    grouped_exercises = load_grouped_exercises()  # existing classifications
    unique_exercises = df["exercise_title"].unique()
    
    new_exercises = []
    
    for exercise in unique_exercises:
        if exercise in grouped_exercises["upper"] or exercise in grouped_exercises["lower"]:
            continue
        
        # Classfy exercise with AI
        result = classify_exercise(exercise)
        
        # Insert into the correct flat list inside Json file
        if "upper" in result:
            grouped_exercises["upper"].append(exercise)
        elif "lower" in result:
            grouped_exercises["lower"].append(exercise)
        else:
            grouped_exercises["unknown"].append(exercise)
            
        logger.info(f"Classified: '{exercise}' as {result}.")
        
    
    for exercise in new_exercises:
        result = classify_exercise(exercise)
        grouped_exercises[exercise] = result
        print(f"Classifed: {exercise} -> {result}")
        
    save_grouped_exercises(grouped_exercises)
    return grouped_exercises
            
    
