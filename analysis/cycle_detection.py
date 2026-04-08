import pandas as pd


def detect_last_cycle(
    df: pd.DataFrame,
    max_gap_days: int = 3,
    min_days: int = 14
) -> pd.DataFrame:
    """
    Detect the most recent continuous cycle of training/nutrition data.

    Args:
        df (pd.DataFrame): Merged dataset with weight, calories, protein.
        max_gap_days (int): Maximum allowed gap before breaking the cycle.
        min_days (int): Minimum number of days required for a valid cycle.

    Returns:
        pd.DataFrame: The detected cycle subset.
    """
    df = df.copy()
    df = df.dropna(subset=["bodyweight", "calories", "protein"], how="all")
    df = df.sort_values("date").reset_index(drop=True)

    if df.empty:
        return df

    df["gap"] = df["date"].diff().dt.days
    df.loc[0, "gap"] = 1

    last_idx = len(df) - 1
    cutoff_idx = 0

    for i in range(last_idx, -1, -1):
        if i == 0:
            cutoff_idx = 0
            break
        if df.loc[i, "gap"] > max_gap_days:
            cutoff_idx = i
            break

    cycle = df.iloc[cutoff_idx:].copy()

    if len(cycle) < min_days:
        cycle = df.tail(min_days).copy()

    return cycle
