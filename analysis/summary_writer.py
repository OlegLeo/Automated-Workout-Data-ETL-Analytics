from pathlib import Path
import datetime as dt


def save_summary(text: str, out_dir: Path) -> Path:
    """
    Save the generated summary to a timestamped text file.

    Args:
        text (str): Summary text.
        out_dir (Path): Output directory.

    Returns:
        Path: Path to the saved file.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    path = out_dir / f"{today}_training_analysis.txt"
    path.write_text(text, encoding="utf-8")
    return path
