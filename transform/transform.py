import pandas as pd
import numpy as np
from pathlib import Path
import logging

from config import RAW_HEVY_CSV_PATH_RENAMED, MASTER_HEVY_CSV_PATH

logger = logging.getLogger(__name__)

def select_master_columns(df: pd.DataFrame) -> pd.DataFrame:
    final_columns = [
        "uid",
        "title",
        "start_time",
        "end_time",
        "exercise_title",
        "set_index",
        "weight_kg",
        "reps",
        "volume"
    ]
    return df[final_columns]


def load_raw_hevy_data() -> pd.DataFrame:
    """
    Load the raw Hevy CSV and inspect its structure.
    Also converts start_time to a proper datetime object.
    """
    logger.info(f"File Exists: {Path(RAW_HEVY_CSV_PATH_RENAMED).exists()}")

    # Read the raw workouts.csv  
    df = pd.read_csv(RAW_HEVY_CSV_PATH_RENAMED)
    
    # Transform start_time string -> datetime format
    df["start_time"] = pd.to_datetime(df["start_time"])
    
    # print("DF shape:", df.shape)

    # print("Preview of raw data:")
    # print(df.head(5))

    # print("\nColumn names:")
    # print(df.columns)

    # print("\nData types:")
    # print(df.dtypes)

    # print("\nInfo:")
    # print(df.info())

    return df


def load_master_data(path: Path) -> pd.DataFrame:
    if path.exists():
        df = pd.read_csv(path)
        logger.info(f"Loaded Hevy master file with {len(df)} rows.")
        return df
    else:
        logger.info("Hevy master file does not exist yet. Creating one...")
        return pd.DataFrame()
    

def append_only_new_rows(master_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    if master_df.empty:
        logger.info("Master is empty - using all new rows.")
        return new_df
    
    # Keep only rows whose UID is not in master
    new_unique = new_df[~new_df["uid"].isin(master_df["uid"])]
    logger.info(f"Found {len(new_unique)} new rows to append.")
    
    return pd.concat([master_df, new_unique], ignore_index=True)

def save_master_data(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Master file saved with {len(df)} total rows.")
    


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


def normalize(text: str) -> str:
    return (
        text.lower()
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "_")
    )


def run() -> None:
    # Load raw data
    df = load_raw_hevy_data()
    
    # Add unique identifier column
    df = add_uid(df)
    
    # Add volume column
    df = add_volume(df)
    
    # Keep only the columns we want in the master file
    df = select_master_columns(df)
    
    # Load Hevy master data 
    master_df = load_master_data(MASTER_HEVY_CSV_PATH)
    
    # Append only new rows
    updated_master = append_only_new_rows(master_df, df)
    
    # Save
    save_master_data(updated_master, MASTER_HEVY_CSV_PATH)
    

if __name__ == "__main__":
    run()

