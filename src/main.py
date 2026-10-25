"""Command-line entry point for the booking analysis workflow."""

import argparse
from pathlib import Path

from .analysis import build_analysis
from .data_cleaning import clean_booking_data
from .data_loader import load_booking_data
from .generate_dataset import RAW_DATA_PATH, generate_booking_data
from .report_summary import export_analysis
from .visualizations import create_visualizations

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_analysis(data_path: Path = RAW_DATA_PATH, regenerate: bool = False, charts: bool = True) -> dict:
    """Run generation (when needed), cleaning, analysis, exports, and charts."""
    if regenerate or not data_path.exists():
        data_path.parent.mkdir(parents=True, exist_ok=True)
        generate_booking_data().to_csv(data_path, index=False, date_format="%Y-%m-%d")
        print("Generated synthetic input data at {}".format(data_path))
    raw = load_booking_data(data_path)
    cleaned, cleaning_summary = clean_booking_data(raw)
    processed_path = PROJECT_ROOT / "data" / "processed" / "cleaned_booking_data.csv"
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(processed_path, index=False, date_format="%Y-%m-%d")

    results = build_analysis(cleaned)
    export_analysis(results, cleaning_summary, PROJECT_ROOT / "data" / "output")
    if charts:
        create_visualizations(cleaned, results, PROJECT_ROOT / "figures")

    print("\nAnalysis complete")
    print("Cleaned rows: {}".format(results["metrics"]["dataset_records"]))
    print("Unique bookings: {}".format(results["metrics"]["total_bookings"]))
    print("Ticket count: {}".format(results["metrics"]["ticket_count"]))
    print("Recognized revenue: INR {:,.2f}".format(results["metrics"]["recognized_revenue"]))
    print("Most popular destination: {}".format(results["metrics"]["most_popular_destination"]))
    print("Execution summary: {}".format(PROJECT_ROOT / "outputs" / "execution_summary.txt"))
    return {"cleaned_data": cleaned, "cleaning_summary": cleaning_summary, "results": results}


def main() -> None:
    """Parse command-line options and report actionable errors."""
    parser = argparse.ArgumentParser(description="Analyze synthetic bus and train booking records.")
    parser.add_argument("--data", type=Path, default=RAW_DATA_PATH, help="Input booking CSV path")
    parser.add_argument("--regenerate", action="store_true", help="Replace the input with a new seeded dataset")
    parser.add_argument("--skip-charts", action="store_true", help="Skip PNG chart generation")
    args = parser.parse_args()
    try:
        run_analysis(args.data, args.regenerate, not args.skip_charts)
    except (FileNotFoundError, ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()