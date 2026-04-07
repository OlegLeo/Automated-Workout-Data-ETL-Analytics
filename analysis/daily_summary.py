# analysis/daily_summary.py

import datetime as dt
from pathlib import Path

import pandas as pd
import requests

from config import (
    MASTER_HEVY_CSV_PATH,
    MASTER_WEIGHT_CSV_PATH,
    MASTER_NUTRITION_CSV_PATH,
    OLLAMA_API,
    OLLAMA_MODEL,
)


def load_data():
    # -----------------------------
    # Load WEIGHT data
    # -----------------------------
    bw = pd.read_csv(
        MASTER_WEIGHT_CSV_PATH,
        parse_dates=["date"],
        dayfirst=True
    )

    # Rename kg → bodyweight
    bw = bw.rename(columns={"kg": "bodyweight"})

    # -----------------------------
    # Load NUTRITION data
    # -----------------------------
    nut = pd.read_csv(
        MASTER_NUTRITION_CSV_PATH,
        parse_dates=["date"],
        dayfirst=True
    )
    # nutrition already has: date, calories, protein

    # -----------------------------
    # Load HEVY workout data
    # -----------------------------
    wo = pd.read_csv(
        MASTER_HEVY_CSV_PATH,
        parse_dates=["start_time"],
        dayfirst=True
    )

    # Extract date from start_time
    wo["date"] = pd.to_datetime(wo["start_time"].dt.date)

    # Aggregate total volume per day
    wo_daily = wo.groupby("date", as_index=False)["volume"].sum()

    # -----------------------------
    # Merge all datasets
    # -----------------------------
    df = (
        bw[["date", "bodyweight"]]
        .merge(nut[["date", "calories", "protein"]], on="date", how="outer")
        .merge(wo_daily, on="date", how="left")
        .sort_values("date")
        .reset_index(drop=True)
    )

    return df


def detect_last_cycle(df: pd.DataFrame, max_gap_days: int = 3, min_days: int = 14):
    """
    Walk backwards from the most recent date and stop when gaps or missing data
    make the cycle unreliable.
    """
    df = df.copy()

    # Keep only rows where at least one of the key metrics exists
    df = df.dropna(subset=["bodyweight", "calories", "protein"], how="all")
    df = df.sort_values("date").reset_index(drop=True)

    if df.empty:
        return df

    df["gap"] = df["date"].diff().dt.days
    df.loc[0, "gap"] = 1  # first row

    last_idx = len(df) - 1
    cutoff_idx = 0

    for i in range(last_idx, -1, -1):
        if i == 0:
            cutoff_idx = 0
            break
        gap = df.loc[i, "gap"]
        if gap is not None and gap > max_gap_days:
            cutoff_idx = i
            break

    cycle = df.iloc[cutoff_idx:].copy()

    # Enforce minimum cycle length
    if len(cycle) < min_days:
        cycle = df.tail(min_days).copy()

    return cycle


def compute_cycle_metrics(cycle: pd.DataFrame):
    start_date = cycle["date"].min()
    end_date = cycle["date"].max()
    days = (end_date - start_date).days + 1

    start_weight = cycle.sort_values("date")["bodyweight"].iloc[0]
    end_weight = cycle.sort_values("date")["bodyweight"].iloc[-1]

    avg_weight = cycle["bodyweight"].mean()
    avg_calories = cycle["calories"].mean()
    avg_protein = cycle["protein"].mean()
    total_volume = cycle["volume"].fillna(0).sum()
    workouts_days = cycle["volume"].fillna(0).gt(0).sum()

    return {
        "start_date": start_date.date().isoformat(),
        "end_date": end_date.date().isoformat(),
        "days": int(days),
        "start_weight": float(start_weight),
        "end_weight": float(end_weight),
        "avg_weight": float(avg_weight),
        "avg_calories": float(avg_calories),
        "avg_protein": float(avg_protein),
        "total_volume": float(total_volume),
        "workout_days": int(workouts_days),
    }


def build_prompt(metrics: dict):
    return f"""
You are my personal strength and hypertrophy coach.

Use ONLY the data provided below. 
Do NOT invent additional metrics such as muscle mass, body fat, strength levels, or bodyweight separate from weight.

Here is my last training/nutrition cycle:

DATES:
- Start date: {metrics['start_date']}
- End date: {metrics['end_date']}
- Length: {metrics['days']} days

WEIGHT (kg):
- Start: {metrics['start_weight']:.1f}
- End: {metrics['end_weight']:.1f}
- Average: {metrics['avg_weight']:.1f}

NUTRITION:
- Average calories: {metrics['avg_calories']:.0f} kcal/day
- Average protein: {metrics['avg_protein']:.0f} g/day

TRAINING:
- Total volume: {metrics['total_volume']:.0f}
- Training days: {metrics['workout_days']}

My goal: gain muscle and bodyweight at a healthy, sustainable rate.

TASK:
1. Summarize my progress using ONLY the numbers above.
2. Explain what went well and what held me back.
3. Give me 3–5 specific, actionable recommendations for the next cycle.
4. Keep it concise and do NOT invent any metrics not listed above.
"""



def call_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    resp = requests.post(OLLAMA_API, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "").strip()


def save_summary(text: str, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    path = out_dir / f"{today}_cycle_summary.txt"
    path.write_text(text, encoding="utf-8")
    return path


def main():
    df = load_data()
    cycle = detect_last_cycle(df)
    if cycle.empty:
        print("No valid cycle data found.")
        return

    metrics = compute_cycle_metrics(cycle)
    prompt = build_prompt(metrics)
    summary = call_ollama(prompt)

    print("\n=== CYCLE METRICS ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\n=== AI SUMMARY ===")
    print(summary)

    out_path = save_summary(summary, Path("summaries"))
    print(f"\nSaved summary to: {out_path}")


if __name__ == "__main__":
    main()
