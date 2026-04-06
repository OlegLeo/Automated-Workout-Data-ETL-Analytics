from config import RAW_NUTRITION_CSV_PATH, MASTER_NUTRITION_CSV_PATH
from transform.common import (
    load_raw_data_and_tranform_date_format,
    select_master_columns,
    load_master_data,
    append_only_new_rows,
    save_master_data
)
    

def run() -> None:
    # Load raw data
    df = load_raw_data_and_tranform_date_format(RAW_NUTRITION_CSV_PATH)
    
    # Keep only the columns we want in the master file    
    df = select_master_columns(["date", "calories", "protein"], df)
    
    # Load nutrition master data 
    master_df = load_master_data(MASTER_NUTRITION_CSV_PATH)
    
    # Append only new rows
    updated_master = append_only_new_rows(master_df, df, key="date")
    
    # Save
    save_master_data(updated_master, MASTER_NUTRITION_CSV_PATH)


if __name__ == "__main__":
    run()
    
