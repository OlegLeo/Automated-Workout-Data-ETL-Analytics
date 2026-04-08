from pathlib import Path
from analysis.data_loader import load_data
from analysis.cycle_detection import detect_last_cycle
from analysis.metrics import compute_cycle_metrics
from analysis.prompt_builder import build_prompt
from analysis.ollama_client import call_ollama
from analysis.summary_writer import save_summary


def main() -> None:
    """
    Run the full analysis pipeline:
    - Load data
    - Detect cycle
    - Compute metrics
    - Build prompt
    - Query LLM
    - Save summary
    """
    df, wo = load_data()
    cycle = detect_last_cycle(df)

    if cycle.empty:
        print("No valid cycle data found.")
        return

    metrics = compute_cycle_metrics(cycle, wo)
    prompt = build_prompt(metrics)
    summary = call_ollama(prompt)

    print("\n=== TRAINING ANALYSIS ===")
    print(summary)

    out_path = save_summary(summary, Path("summaries"))
    print(f"\nSaved summary to: {out_path}")


if __name__ == "__main__":
    main()
