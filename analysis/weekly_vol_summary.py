from analysis.ai.data_loader import load_data
from analysis.ai_agent import update_groups_from_df 
from analysis.weekly_volume import compute_weekly_volume       
from analysis.exercise_groups import load_grouped_exercises
from config import WEEKLY_SUMMARY_CSV_PATH
import logging
import sys 

logger = logging.getLogger(__name__)   # Logger for this module.


def validate_grouped_exercises(groups: dict):
    if groups.get("unknown"):
        unknown_list = ", ".join(groups["unknown"])
        logger.error(
            f"❌ ERROR: grouped_exercises.json contains exercises in 'unknown': {unknown_list}\n"
            "Please classify them as 'upper' or 'lower' before running the script again."
        )
        sys.exit(1)

def run():
    logger.info("Running the AI exercise classifier...")

    # 1. Load JSON BEFORE doing anything else
    grouped_exercises = load_grouped_exercises()

    # 2. Validate JSON BEFORE classification
    validate_grouped_exercises(grouped_exercises)

    # 3. Load workout data
    df = load_data()

    # 4. Run AI classifier (may update JSON)
    update_groups_from_df(df)

    # 5. Reload JSON AFTER classification
    grouped_exercises = load_grouped_exercises()

    # 6. Validate JSON AGAIN (catch new unknowns)
    validate_grouped_exercises(grouped_exercises)

    # 7. Compute weekly volume
    weekly_volume = compute_weekly_volume(df, grouped_exercises)

    logger.info(f"Saving resulst in {WEEKLY_SUMMARY_CSV_PATH}")
    weekly_volume.to_csv(WEEKLY_SUMMARY_CSV_PATH, index=False)
    
if __name__ == "__main__":
    run()