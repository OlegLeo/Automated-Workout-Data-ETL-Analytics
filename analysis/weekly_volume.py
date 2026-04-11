import pandas as pd

def compute_weekly_volume(df: pd.DataFrame, groups: dict) -> pd.DataFrame:
    """Compute weekly volume with upper/lower body split, including empty weeks."""

    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    df["date"] = df["date"].dt.normalize()

    # Week boundaries (Sun–Sat → start Monday)
    df["week_start"] = df["date"].dt.to_period("W-FRI").dt.start_time
    df["week_end"]   = df["date"].dt.to_period("W-FRI").dt.end_time

    # Map exercise → group
    df["group"] = df["exercise_title"].apply(lambda ex: map_grouped_exercises(ex, groups))

    # --- YOUR WORKING WEEKLY VOLUME (DO NOT TOUCH) ---
    weekly_volume = (
        df.groupby(["week_start", "week_end", "group"])["volume"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Rename columns early
    weekly_volume = weekly_volume.rename(columns={
        "upper": "upper_body_volume",
        "lower": "lower_body_volume"
    })

    # Ensure missing columns exist
    for col in ["upper_body_volume", "lower_body_volume", "unknown"]:
        if col not in weekly_volume.columns:
            weekly_volume[col] = 0

    # --- BUILD CONTINUOUS WEEK INDEX ---
    min_week = weekly_volume["week_start"].min()
    max_week = weekly_volume["week_start"].max()

    all_week_starts = pd.date_range(start=min_week, end=max_week, freq="7D")

    all_weeks_df = pd.DataFrame({"week_start": all_week_starts})

    # Merge on week_start ONLY
    weekly_volume = all_weeks_df.merge(
        weekly_volume,
        on="week_start",
        how="left"
    ).fillna(0)

    # Recompute week_end (always week_start + 6 days)
    weekly_volume["week_end"] = weekly_volume["week_start"] + pd.Timedelta(days=6)

    # Compute total volume
    weekly_volume["volume"] = (
        weekly_volume["upper_body_volume"] +
        weekly_volume["lower_body_volume"]
    )

    # Add week numbers
    weekly_volume["week_number"] = range(1, len(weekly_volume) + 1)

    # Reorder columns
    weekly_volume = weekly_volume[
        [
            "week_number",
            "week_start",
            "week_end",
            "upper_body_volume",
            "lower_body_volume",
            "unknown",
            "volume"
        ]
    ]

    return weekly_volume


def map_grouped_exercises(exercise: str, groups: dict) -> str:
    if exercise in groups["upper"]:
        return "upper"
    elif exercise in groups["lower"]:
        return "lower"
    else:
        raise ValueError(
            f"ERROR: Exercise '{exercise}' is not found in grouped_exercises.json.\n"
            f"Please update grouped_exercises.json and add this exercise to either 'upper' or 'lower'."
        )
