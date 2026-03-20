from hevy_scraper.main import run as run_scraper
from transform.transform import run as run_transform
from ingest.google_sheets_ingest import run as run_google_sheets
import logging

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Hevy data pipeline...")
    
    run_scraper()
    run_transform()
    
    logger.info("Starting Google Sheets ingestion")
    run_google_sheets()
    logger.info("Pipeline completed successfully.")
    

if __name__ == "__main__":
    main()