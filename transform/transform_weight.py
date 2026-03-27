import pandas as pd 
from pathlib import Path
import logging

from config import RAW_WEIGHT_CSV_PATH, MASTER_WEIGHT_CSV_PATH
from transform.common import (
    log_file_exists, 
    load_master_data
)

logger = logging.getLogger(__name__)

def select_master_weight_columns(df: pd.DataFrame) -> pd.DataFrame:
    final_columns = [
        "date",
        "kg"
    ]
    return df[final_columns]

    
def load_raw_weight_data() -> pd.DataFrame:
    """
    Load the raw Weight Google Sheets CSV and inspect its structure.
    Also converts date (MM/DD/YYYY) into a proper datetime object ("DD/MM/YYYY").
    """
    log_file_exists(RAW_WEIGHT_CSV_PATH)
    
    df = pd.read_csv(RAW_WEIGHT_CSV_PATH)
        
    df["date"] = pd.to_datetime(df["date"])
    
    df["date"] = df["date"].dt.strftime("%d/%m/%Y")
    
    print(df.head(10))
    
    return df
    

def run() -> None:
    load_raw_weight_data()
    load_master_data(MASTER_WEIGHT_CSV_PATH)


if __name__ == "__main__":
    run()
    
