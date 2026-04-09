import pandas as pd
from config import MASTER_HEVY_CSV_PATH

def load_data() -> pd.DataFrame:
    """Load the data from master_workout csv file
        - date column used to group data into weekly
        - exercise_title column used to categorize eithe its a upper or lower body exercise
        - volume column used to calcule weekly volume
    """   
    df = pd.read_csv(MASTER_HEVY_CSV_PATH)
    
    # Using only the columns that are important for weekly volume calculation based on weigher upper or lower body
    final_columns = [
        "date",
        "exercise_title",
        "volume"
    ]
    
    return df[final_columns]