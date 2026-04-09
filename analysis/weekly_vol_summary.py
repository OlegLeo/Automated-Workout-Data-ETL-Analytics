from analysis.ai.connection import ask_ai
from analysis.ai.prompt import ai_prompt
from analysis.ai.data_loader import load_data
from analysis.ai.exercise_classifier import classify_exercise
from analysis.ai_agent import update_groups_from_df 

def run():
    print("Running the AI exercise classifier...")   # Printing message to user for running program in console or IDEs etc...      

    df = load_data()
    update_groups_from_df(df)
    
    
if __name__ == "__main__":
    run()