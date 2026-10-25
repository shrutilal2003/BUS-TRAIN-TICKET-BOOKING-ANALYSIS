"""Export analysis tables and a concise text summary."""

from pathlib import Path
from typing import Dict


def export_analysis(results: Dict[str, object], cleaning: Dict[str, int], output_dir: Path) -> Path:
    """Write required summary CSV files and the human-readable execution log."""
    output_dir.mkdir(parents=True, exist_ok=True)
    results["destination_summary"].to_csv(output_dir / "destination_summary.csv", index=False)
    results["route_summary"].to_csv(output_dir / "route_summary.csv", index=False)
    results["monthly_summary"].to_csv(output_dir / "monthly_summary.csv", index=False)
    results["revenue_summary"].to_csv(output_dir / "revenue_summary.csv", index=False)
    results["age_summary"].to_csv(output_dir / "age_group_summary.csv", index=False)
    results["status_summary"].to_csv(output_dir / "booking_status_summary.csv", index=False)

    metrics = results["metrics"]
    lines = [
        "BUS / TRAIN TICKET BOOKING DATA ANALYSIS",
        "Dataset designation: synthetic educational data; not operator or passenger records.",
        "",
        "Cleaning summary:",
    ]
    lines.extend("{}: {}".format(key.replace("_", " ").title(), value) for key, value in cleaning.items())
    lines.extend(["", "Analysis results:"])
    lines.extend("{}: {}".format(key.replace("_", " ").title(), value) for key, value in metrics.items())
    lines.extend([
        "",
        "Revenue rule: per-ticket price multiplied by ticket quantity; Completed and Confirmed statuses count.",
        "Cancelled and Pending bookings contribute zero recognized revenue. Refund accounting is not modeled.",
    ])
    summary_path = output_dir.parent.parent / "outputs" / "execution_summary.txt"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary_path