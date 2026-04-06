from hevy_scraper.main import run as run_scraper
from transform.transform_hevy import run as run_hevy
from transform.transform_nutrition import run as run_nutrition
from transform.transform_weight import run as run_weight
from ingest.google_sheets_ingest import run as run_google_sheets
import logging

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Hevy data pipeline...")
    
    logger.info("Starting Hevy Scraper")
    run_scraper()
    
    logger.info("Starting Google Sheets ingestion")
    run_google_sheets()
    
    logger.info("Starting Trasnformation...")
    run_hevy()
    run_nutrition()
    run_weight()
    
    logger.info("Pipeline completed successfully.")
    

if __name__ == "__main__":
    main()