import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def log_file_exists(path: Path) -> None:
    """Log wheter a file exists."""
    logger.info(f"Raw CSV file exists: {path} -> {path.exists()}")


def load_raw_data_and_tranform_date_format(raw_csv_path: Path) -> pd.DataFrame:
    """
    Load the raw Bodyweight or Nutrition data from CSV and inspect its structure.
    Also converts date (MM/DD/YYYY) into a proper datetime object ("DD/MM/YYYY").
    """
    log_file_exists(raw_csv_path)
    
    df = pd.read_csv(raw_csv_path)
        
    df["date"] = pd.to_datetime(df["date"])
    
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        
    return df

def load_raw_hevy_data_and_tranform_date_format(raw_csv_path: Path) -> pd.DataFrame:
    """
    Load the raw Hevy CSV and inspect its structure.
    Also converts start_time to a proper datetime object.
    """
    log_file_exists(raw_csv_path)

    # Read the raw workouts.csv  
    df = pd.read_csv(raw_csv_path)
    
    # Transform start_time string -> datetime format
    df["start_time"] = pd.to_datetime(df["start_time"])

    return df
    

def select_master_columns(final_columns: tuple, df: pd.DataFrame) -> pd.DataFrame:
    """Tuple of none mutable columns that will be present in the master data CSV"""
    return df[final_columns]
    

def load_master_data(path: Path) -> Path:
    """Loading master data. If there is existing master csv data file, we return the existing CSV as Data Frame. If not, we create a new master empty csv file."""
    if path.exists():
        df = pd.read_csv(path)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], dayfirst=True).dt.strftime("%d/%m/%Y")
        logger.info(f"Loaded master file with {len(df)} rows: {path}")
        return df
    else:
        logger.info(f"Master csv file does not exist yet. Creating one: {path}")
        return pd.DataFrame()
    
def append_only_new_rows(master_df: pd.DataFrame, new_df: pd.DataFrame, key) -> pd.DataFrame:
    """We check if master data file exist. If it does exist, we only add a new rows which are different from already existing identifier key."""
    if master_df.empty:
        logger.info(f"Master data is empty - using all new rows.")
        return new_df

    new_unique = new_df[~new_df[key].isin(master_df[key])]
    logger.info(f"Found {len(new_unique)} new rows to append.")
    
    return pd.concat([master_df, new_unique], ignore_index=True)


def save_master_data(df: pd.DataFrame, path: Path) -> None:
    """Store the master data as CSV into a specified path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Master file saved with {len(df)} total rows. Path: {path}")
