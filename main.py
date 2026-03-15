from hevy_scraper.main import run as run_scraper
from transform.transform import run as run_transform
import logging

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Hevy data pipeline...")
    
    run_scraper()
    run_transform()
    
    logger.info("Pipeline completed successfully.")
    

if __name__ == "__main__":
    main()