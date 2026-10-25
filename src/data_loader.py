"""Dataset loading and schema validation utilities."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "Booking_ID", "Passenger_Name", "Age", "Gender", "Transport_Mode",
    "Source", "Destination", "Booking_Date", "Travel_Date", "Ticket_Price",
    "Number_of_Tickets", "Booking_Status", "Payment_Mode",
]


def load_booking_data(path: Path) -> pd.DataFrame:
    """Read a CSV file and reject files that do not have the expected schema."""
    if not path.exists():
        raise FileNotFoundError("Booking data not found: {}".format(path))
    frame = pd.read_csv(path)
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing_columns:
        raise ValueError("Dataset is missing required columns: {}".format(", ".join(missing_columns)))
    return frame