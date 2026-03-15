import os 
from pathlib import Path
import logging
from dotenv import load_dotenv

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

load_dotenv()

ROOT_DIR: Path = Path(__file__).resolve().parent
RAW_CSV_FOLDER: Path = ROOT_DIR / "data" / "raw" / "hevy"
MASTER_CSV_FOLDER: Path = ROOT_DIR / "data" / "master" / "hevy"

RAW_HEVY_CSV_PATH = RAW_CSV_FOLDER / "workouts.csv"
RAW_HEVY_CSV_PATH_RENAMED = RAW_CSV_FOLDER / "raw_workouts.csv"

MASTER_HEVY_CSV_PATH: Path = MASTER_CSV_FOLDER / "master_workouts.csv"

LOGIN_URL: str = "https://hevy.com/login"
EXPORT_URL: str = "https://hevy.com/settings?export"

DEFAULT_TIMEOUT: int = 15

def get_credentials() -> tuple[str, str]:
    """Return Hevy credentials from environment variables."""
    username = os.getenv("HEVY_USERNAME")
    password = os.getenv("HEVY_PASSWORD")
    
    if not username or not password:
        raise ValueError("HEVY_EMAIL and HEVY_PASSWORD must be set in environment variables or .env file")
    
    return username, password