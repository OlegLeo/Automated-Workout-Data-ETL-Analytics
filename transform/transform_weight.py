import pandas as pd 
from config import RAW_WEIGHT_CSV_PATH, MASTER_WEIGHT_CSV_PATH
from transform.common import (
    log_file_exists, 
    select_master_columns,
    load_master_data,
    append_only_new_rows,
    save_master_data
)

    
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
    df = load_raw_weight_data()
    df = select_master_columns(["date", "kg"], df)
    master_df = load_master_data(MASTER_WEIGHT_CSV_PATH)
    updated_master_df = append_only_new_rows(master_df, df, key="date")
    save_master_data(updated_master_df, MASTER_WEIGHT_CSV_PATH)


if __name__ == "__main__":
    run()
    
