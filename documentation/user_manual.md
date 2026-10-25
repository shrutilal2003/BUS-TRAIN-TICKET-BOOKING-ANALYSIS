# User Manual

## Installation

Install Python 3.9 or later. From the project root create and activate a virtual environment, then install `requirements.txt`. The commands are listed in the README for both Windows PowerShell and Linux/macOS.

## Run

1. Open a terminal in the folder containing `src/`.
2. Run `python -m src.generate_dataset` to create the seeded raw data, or run `python -m src.main` to generate it when absent and immediately analyze it.
3. Review `outputs/execution_summary.txt` for the cleaning counts and headline measures.
4. Open `data/processed/cleaned_booking_data.csv`, the grouped tables in `data/output/`, and PNG charts in `figures/`.
5. Run `python -m unittest discover -s tests -v` to execute tests.
6. Open `notebooks/Bus_Train_Ticket_Booking_Analysis.ipynb` in Jupyter for the same workflow with explanations.

## Options and Interpretation

`python -m src.main --regenerate` replaces the raw dataset with the default seed. `--data PATH` uses a different CSV with the documented schema. `--skip-charts` omits figures. Booking count counts unique transaction IDs, ticket count sums passenger seats, and revenue sums per-ticket price times ticket quantity for Completed and Confirmed statuses. Cancellation refunds are not modeled. All records are synthetic and should not be interpreted as actual travel-market evidence.

## Common Issues

Run commands from the project root. Install requirements into the same Python interpreter used for execution. If an input does not contain all required fields, the loader reports the missing column names. If a DOCX-to-PDF converter is unavailable, the DOCX remains editable and can be exported using Microsoft Word or LibreOffice.