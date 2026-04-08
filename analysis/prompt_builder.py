"""
Prompt builder for hypertrophy and training analysis.
"""

from typing import Dict


def build_prompt(metrics: Dict) -> str:
    """
    Build the LLM prompt for training/nutrition analysis.

    Args:
        metrics (Dict): Computed cycle metrics.

    Returns:
        str: Formatted prompt string.
    """
    return f"""
You are my personal hypertrophy and strength coach.

Your ONLY job is to analyze:
- my exercises
- my frequency per week
- my total sessions
- my volume per exercise
- my calories and protein
- my weight change

You MUST classify each exercise into muscle groups WITHOUT me providing labels.

You MUST answer ONLY these questions:

1. Based on my exercise list, which muscles am I training, and which ones am I missing?
2. Is my weekly frequency enough for hypertrophy?
3. Is my total volume enough?
4. Is my training balanced between upper and lower?
5. Does my training frequency and volume match my goal of gaining weight?
6. What should I change to improve hypertrophy and weight gain?

Here is my data:

DATES:
- Start: {metrics['start_date']}
- End: {metrics['end_date']}

WEIGHT:
- Start: {metrics['start_weight']:.1f}
- End: {metrics['end_weight']:.1f}

NUTRITION:
- Avg calories: {metrics['avg_calories']:.0f}
- Avg protein: {metrics['avg_protein']:.0f}

TRAINING:
- Total sessions: {metrics['total_sessions']}
- Total volume: {metrics['total_volume']:.0f}
- Frequency per week: {metrics['freq_per_week']}
- Exercises performed: {metrics['exercises']}
- Volume per exercise: {metrics['volume_per_exercise']}

Give me:
- A muscle-group breakdown
- A frequency evaluation
- A volume evaluation
- A correlation between training and weight gain
- 5 specific improvements for next cycle

Do NOT invent numbers not provided.
"""
