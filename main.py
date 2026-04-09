from hevy_scraper.main import run as run_scraper
from ingest.google_sheets_ingest import run as ingest_google_sheets
from transform.transform_hevy import run as transform_hevy
from transform.transform_nutrition import run as transform_nutrition
from transform.transform_weight import run as transform_weight

import logging

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Hevy data pipeline...")
    
    logger.info("Starting Hevy Scraper")
    run_scraper()
    
    logger.info("Starting Google Sheets ingestion")
    ingest_google_sheets()
    
    logger.info("Starting Trasnformation...")
    transform_hevy()
    transform_nutrition()
    transform_weight()
    
    logger.info("Pipeline completed successfully.")
    

if __name__ == "__main__":
    main()