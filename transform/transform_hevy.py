import pandas as pd
import numpy as np
from config import RAW_HEVY_CSV_PATH_RENAMED, MASTER_HEVY_CSV_PATH
from transform.common import (
    load_raw_hevy_data_and_tranform_date_format,
    select_master_columns,
    load_master_data,
    append_only_new_rows,
    save_master_data
)


def add_uid(df) -> pd.DataFrame:
    """
    Create a unique identifier for each set using:
    start_time + exercise_title + set_index
    """
    df["start_time_str"] = df["start_time"].dt.strftime("%Y-%m-%d_%H-%M-%S")
    df["uid"] = (
        df["start_time_str"] + "_" +
        df["exercise_title"].apply(normalize) + "_" +
        df["set_index"].astype(str)
    )
    return df


def add_volume(df) -> pd.DataFrame:
    """
    Add a volume column:
      - If weight is missing or zero → volume = reps
      - Otherwise → volume = weight * reps
      - Round to 2 decimals
    """
    weight = df["weight_kg"].fillna(0)
    reps = df["reps"].fillna(0)
    
    df["volume"] = np.where(weight == 0, reps, weight * reps)
    
    # Round to 2 decimals
    df["volume"] = df["volume"].round(2)
    
    return df

def add_date(df) -> pd.DataFrame:
    """
    Add a date column:
      - New date column formatted into ISO date from start_time column
      """
    df["date"] = pd.to_datetime(df["start_time"]).dt.strftime("%Y-%m-%d")
    return df

def normalize(text: str) -> str:
    """Normalization function for the formatted UID column"""
    return (
        text.lower()
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "_")
    )


def run() -> None:
    # Load raw data
    df = load_raw_hevy_data_and_tranform_date_format(RAW_HEVY_CSV_PATH_RENAMED)
    
    # Add unique identifier column
    df = add_uid(df)
    
    # Add volume column
    df = add_volume(df)
    
    # Add ISO date column
    df = add_date(df)
    
    # Keep only the columns we want in the master file    
    df = select_master_columns([
        "uid",
        "title",
        "start_time",
        "end_time",
        "date",
        "exercise_title",
        "set_index",
        "weight_kg",
        "reps",
        "volume"
        ], df)
    
    # Load Hevy master data 
    master_df = load_master_data(MASTER_HEVY_CSV_PATH)
    
    
    # Append only new rows
    updated_master = append_only_new_rows(master_df, df, key="uid")
    
    # Sort by start_time from older to latest date
    updated_master = updated_master.sort_values(["start_time", "exercise_title"]) 

    # Save
    save_master_data(updated_master, MASTER_HEVY_CSV_PATH)
    

if __name__ == "__main__":
    run()
