import time
from pathlib import Path
from typing import Optional
import os

def rename_existing_raw_csv(src: Path, dst: Path) -> None:
    """Rename a file from src to dst, safely and cleanly."""
    if src.exists():
        # Ensure the target folder exists
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        # If a previous raw_workouts.csv exists, remove it to avoid errors
        if dst.exists():
            dst.unlink()
            
        os.rename(src, dst)
    

def delete_existing_csv_files(folder: Path) -> None:
    """Deletes existing raw hevy data."""
    folder.mkdir(parents=True, exist_ok=True)
    for file in folder.glob("*.csv"):
        file.unlink()
        

def wait_for_new_csv(folder: Path, timeout: int = 30) -> Path:
    """Wait for a new CSV file to appear in the folder within the timeout."""
    folder.mkdir(parents=True, exist_ok=True)
    
    start = time.time()
    while time.time() - start < timeout:
        csv_files = list(folder.glob("*.csv"))
        if csv_files:
            # Return the most recently modified CSV file
            latest_file: Optional[Path] = max(csv_files, key=lambda f: f.stat().st_mtime)
            return latest_file
        time.sleep(1)
        
    raise TimeoutError("CSV download did not complete within the expected time.")

