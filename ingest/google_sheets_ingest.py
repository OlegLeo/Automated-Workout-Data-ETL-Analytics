"""
Ingest Google Sheets data (calories, weight) into raw CSV files.

This script downloads Google Sheets as CSV using the public export endpoint.
Sheets must be shared as "Anyone with the link can view".
"""

import requests
from pathlib import Path
from config import (
    GOOGLE_SHEETS_CALORIES_ID, 
    GOOGLE_SHEETS_WEIGHT_ID,
    RAW_GOOGLE_SHEETS_FOLDER,
    MASTER_GOOGLE_SHEETS_FOLDER
    )
import logging

logger = logging.getLogger(__name__)
    
    
def download_google_sheet(sheet_id: str, output_path: Path) -> None:
    """
    Download a Google Sheet as CSV and save it to the given path.

    Args:
        sheet_id (str): Google Sheet ID.
        output_path (Path): Where to save the CSV file.
    """
    url: str = f"https://docs.google.com/forms/d/{sheet_id}/edit"
    
    
    if __name__ == "__main__":
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to download Google Sheet {sheet_id}. "
                f"Status code: {response.status_code}"
            )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    
    logger.info(f"[INGEST] Saved Google Sheet to {output_path}")
    

def main():
    """Main entry point for ingesting Google Sheets data."""
    logger.info("[INGEST] Starting Google Sheets ingestion...")
    
    download_google_sheet(GOOGLE_SHEETS_CALORIES_ID, RAW_GOOGLE_SHEETS_FOLDER)
        
    logger.info("[INGEST] Google Sheets ingestion completed.")

if __name__ == "__main__":
    main()