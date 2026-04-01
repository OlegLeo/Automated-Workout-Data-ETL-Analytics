import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def log_file_exists(path: Path) -> None:
    """Log wheter a file exists."""
    logger.info(f"Raw CSV file exists: {path} -> {path.exists()}")


def load_master_data(path: Path) -> Path:
    if path.exists():
        df = pd.read_csv(path)
        logger.info(f"Loaded master file with {len(df)} rows: {path}")
        return df
    else:
        logger.info(f"Master csv file does not exist yet. Creating one: {path}")
        return pd.DataFrame()
    
def append_only_new_rows(master_df: pd.DataFrame, new_df: pd.DataFrame, key) -> pd.DataFrame:
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
