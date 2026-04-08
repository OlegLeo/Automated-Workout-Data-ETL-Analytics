from typing import Tuple
import pandas as pd
from config import (
    MASTER_HEVY_CSV_PATH,
    MASTER_WEIGHT_CSV_PATH,
    MASTER_NUTRITION_CSV_PATH,
)


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and merge weight, nutrition, and workout data.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - df: merged daily dataset (weight, calories, protein, volume)
            - wo: raw workout dataset with exercises and timestamps
    """
    # Load weight
    bw = pd.read_csv(
        MASTER_WEIGHT_CSV_PATH,
        parse_dates=["date"],
        dayfirst=True
    ).rename(columns={"kg": "bodyweight"})

    # Load nutrition
    nut = pd.read_csv(
        MASTER_NUTRITION_CSV_PATH,
        parse_dates=["date"],
        dayfirst=True
    )

    # Load workouts
    wo = pd.read_csv(
        MASTER_HEVY_CSV_PATH,
        parse_dates=["start_time"],
        dayfirst=True
    )
    wo["date"] = pd.to_datetime(wo["start_time"].dt.date)

    # Aggregate daily volume
    wo_daily = wo.groupby("date", as_index=False)["volume"].sum()

    # Merge datasets
    df = (
        bw[["date", "bodyweight"]]
        .merge(nut[["date", "calories", "protein"]], on="date", how="outer")
        .merge(wo_daily, on="date", how="left")
        .sort_values("date")
        .reset_index(drop=True)
    )

    return df, wo
