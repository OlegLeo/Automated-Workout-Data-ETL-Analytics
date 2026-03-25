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

RAW_HEVY_CSV_PATH: Path = RAW_CSV_FOLDER / "workouts.csv"
RAW_HEVY_CSV_PATH_RENAMED: Path = RAW_CSV_FOLDER / "raw_workouts.csv"

MASTER_HEVY_CSV_PATH: Path = MASTER_CSV_FOLDER / "master_workouts.csv"

RAW_GOOGLE_SHEETS_FOLDER: Path = ROOT_DIR / "data" / "raw" / "google_sheets"
MASTER_GOOGLE_SHEETS_FOLDER: Path = ROOT_DIR / "data" / "master" / "google_sheets"

RAW_NUTRITION_CSV_PATH = RAW_GOOGLE_SHEETS_FOLDER / "raw_nutrition.csv"
RAW_WEIGHT_CSV_PATH = RAW_GOOGLE_SHEETS_FOLDER / "raw_weight.csv"

MASTER_NUTRITION_CSV_PATH = MASTER_GOOGLE_SHEETS_FOLDER / "raw_nutrition.csv"
MASTER_WEIGHT_CSV_PATH = MASTER_GOOGLE_SHEETS_FOLDER / "raw_weight.csv"

GOOGLE_SHEETS_NUTRITION_ID: str = os.getenv("GOOGLE_SHEETS_NUTRITION_ID")
GOOGLE_SHEETS_WEIGHT_ID: str = os.getenv("GOOGLE_SHEETS_WEIGHT_ID")

GOOGLE_SHEETS_WEIGHT_GID: str = os.getenv("GOOGLE_SHEETS_WEIGHT_GID")
GOOGLE_SHEETS_NUTRITION_GID: str = os.getenv("GOOGLE_SHEETS_NUTRITION_GID")

LOGIN_URL: str = "https://hevy.com/login"
EXPORT_URL: str = "https://hevy.com/settings?export"

DEFAULT_TIMEOUT: int = 15

def get_credentials() -> tuple[str, str]:
    """Return Hevy credentials from environment variables."""
    username: str = os.getenv("HEVY_USERNAME")
    password: str = os.getenv("HEVY_PASSWORD")
    
    if not username or not password:
        raise ValueError("HEVY_EMAIL and HEVY_PASSWORD must be set in environment variables or .env file")
    
    return username, password