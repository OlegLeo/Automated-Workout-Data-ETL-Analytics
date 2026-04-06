from config import RAW_WEIGHT_CSV_PATH, MASTER_WEIGHT_CSV_PATH
from transform.common import (
    load_raw_data_and_tranform_date_format,
    select_master_columns,
    load_master_data,
    append_only_new_rows,
    save_master_data
)


def run() -> None:
    # Load raw bodyweight data
    df = load_raw_data_and_tranform_date_format(RAW_WEIGHT_CSV_PATH)
    
    # Keep only the columns we want in the master file    
    df = select_master_columns(["date", "kg"], df)
    
    # Load nutrition master data 
    master_df = load_master_data(MASTER_WEIGHT_CSV_PATH)
    
    # Append only new rows
    updated_master = append_only_new_rows(master_df, df, key="date")
    
    # Save
    save_master_data(updated_master, MASTER_WEIGHT_CSV_PATH)


if __name__ == "__main__":
    run()
    
