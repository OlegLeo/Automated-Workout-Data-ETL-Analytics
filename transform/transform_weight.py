import pandas as pd 
from pathlib import Path
import logging

from config import RAW_WEIGHT_CSV_PATH, MASTER_WEIGHT_CSV_PATH

logger = logging.getLogger(__name__)

def select_master_weight_columns(df: pd.DataFrame) -> pd.DataFrame:
    final_columns = [
        "timestamp",
        "kg"
    ]
    return df[final_columns]

def load_raw_weight_data() -> pd.DataFrame:
    """
    Load the raw Weight Google Sheets CSV and inspect its structure.
    Also converts Timestamp (MM/DD/YYYY) into a proper datetime object - "timestamp" ("DD/MM/YYYY").
    """
    logger.info(f"Hevy Raw CSV file exists:", {Path.exists(RAW_WEIGHT_CSV_PATH)})
    
    df = pd.read_csv(RAW_WEIGHT_CSV_PATH)
    
    print(df.head(10))
    
    

def run() -> None:
    load_raw_weight_data()
    

if __name__ == "__main__":
    run()
    
