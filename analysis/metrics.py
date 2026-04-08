from typing import Dict, Any
import pandas as pd


def compute_cycle_metrics(cycle: pd.DataFrame, wo: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute key metrics for the detected training/nutrition cycle.

    Args:
        cycle (pd.DataFrame): Filtered cycle dataset.
        wo (pd.DataFrame): Raw workout dataset.

    Returns:
        Dict[str, Any]: Dictionary of computed metrics.
    """
    start_date = cycle["date"].min()
    end_date = cycle["date"].max()

    # Filter workouts inside cycle
    wo_cycle = wo[(wo["date"] >= start_date) & (wo["date"] <= end_date)].copy()

    # Exercises
    exercises = sorted(wo_cycle["exercise_title"].unique())

    # Sessions
    total_sessions = wo_cycle["start_time"].dt.date.nunique()

    # Weekly frequency
    wo_cycle["week"] = wo_cycle["date"].dt.isocalendar().week
    freq_per_week = wo_cycle.groupby("week")["date"].nunique().to_dict()

    # Volume per exercise
    volume_per_ex = wo_cycle.groupby("exercise_title")["volume"].sum().to_dict()

    # Total volume
    total_volume = wo_cycle["volume"].sum()

    # Weight change
    start_weight = cycle["bodyweight"].iloc[0]
    end_weight = cycle["bodyweight"].iloc[-1]

    return {
        "start_date": start_date.date().isoformat(),
        "end_date": end_date.date().isoformat(),
        "start_weight": float(start_weight),
        "end_weight": float(end_weight),
        "avg_calories": float(cycle["calories"].mean()),
        "avg_protein": float(cycle["protein"].mean()),
        "total_volume": float(total_volume),
        "total_sessions": int(total_sessions),
        "exercises": exercises,
        "volume_per_exercise": volume_per_ex,
        "freq_per_week": freq_per_week,
    }
