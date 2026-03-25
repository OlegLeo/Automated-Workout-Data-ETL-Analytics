"""
Ingest Google Sheets data (nutrition, weight) into raw CSV files.

This script downloads Google Sheets as CSV using the public export endpoint.
Sheets must be shared as "Anyone with the link can view".
"""

import requests
from pathlib import Path
from config import (
    GOOGLE_SHEETS_NUTRITION_ID, 
    GOOGLE_SHEETS_WEIGHT_ID,
    RAW_NUTRITION_CSV_PATH,
    RAW_WEIGHT_CSV_PATH,
    GOOGLE_SHEETS_WEIGHT_GID,
    GOOGLE_SHEETS_NUTRITION_GID
    )
import logging

logger = logging.getLogger(__name__)
    
    
def download_google_sheet(sheet_id: str, gid: str, output_path: Path) -> None:
    """
    Download a Google Sheet as CSV and save it to the given path.

    Args:
        sheet_id (str): Google Sheet ID.
        gid (str): Google Sheet gid
        output_path (Path): Where to save the CSV file.
    """
    url: str = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to download Google Sheet {sheet_id}. "
            f"Status code: {response.status_code}"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    
    logger.info(f"[INGEST] Saved Google Sheet to {output_path}")
    

def run():
    """Main entry point for ingesting Google Sheets data."""
    logger.info("[INGEST] Starting Google Sheets ingestion...")
    
    download_google_sheet(GOOGLE_SHEETS_NUTRITION_ID,GOOGLE_SHEETS_NUTRITION_GID, RAW_NUTRITION_CSV_PATH)
    download_google_sheet(GOOGLE_SHEETS_WEIGHT_ID, GOOGLE_SHEETS_WEIGHT_GID, RAW_WEIGHT_CSV_PATH)
    logger.info("[INGEST] Google Sheets ingestion completed.")

if __name__ == "__main__":
    run()