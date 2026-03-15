import logging 

from config import RAW_CSV_FOLDER, RAW_HEVY_CSV_PATH, RAW_HEVY_CSV_PATH_RENAMED, get_credentials
from .browser import create_driver
from .auth import login
from .export import navigate_to_export_page, trigger_export
from utils.file_utils import delete_existing_csv_files, wait_for_new_csv, rename_existing_raw_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

def run() -> None: 
    """Run the full Hevy export workflow."""
    email, password = get_credentials()
    driver = create_driver(RAW_CSV_FOLDER)
    
    try:
        logger.info("Logging into Hevy...")
        login(driver, email, password)
        
        logger.info("Deleting existing CSV files...")
        delete_existing_csv_files(RAW_CSV_FOLDER)
        
        logger.info("Navigating to export page...")
        navigate_to_export_page(driver)
        
        logger.info("Triggering CSV export...")
        trigger_export(driver)
    
        logger.info("Waiting for CSV download to complete...")
        csv_file = wait_for_new_csv(RAW_CSV_FOLDER, timeout=60)
        
        logger.info("CSV downloaded successfully: %s", csv_file)
    except Exception as exc:
        logger.exception("An error occured during the Hevy export workflow: %s", exc)
        raise
    finally:
        logger.info("Closing browser...")
        driver.quit()
        
        rename_existing_raw_csv(RAW_HEVY_CSV_PATH, RAW_HEVY_CSV_PATH_RENAMED)
        

if __name__ == "__main__":
    run()