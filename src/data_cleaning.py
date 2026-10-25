"""Validation and cleaning functions for booking records."""

import pandas as pd

from .data_loader import REQUIRED_COLUMNS


def clean_booking_data(raw_data: pd.DataFrame) -> tuple:
    """Normalize data, remove exact duplicate rows, and impute selected fields.

    Returns the cleaned frame and a dictionary of auditable cleaning counts.
    Repeated bookings are retained unless every column in a row is identical.
    """
    frame = raw_data.copy()
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing_columns:
        raise ValueError("Dataset is missing required columns: {}".format(", ".join(missing_columns)))

    original_count = len(frame)
    missing_cells = int(frame[REQUIRED_COLUMNS].isna().sum().sum())
    duplicate_count = int(frame.duplicated(subset=REQUIRED_COLUMNS).sum())
    frame = frame.drop_duplicates(subset=REQUIRED_COLUMNS).copy()

    frame["Booking_ID"] = frame["Booking_ID"].astype("string").str.strip()
    frame["Passenger_Name"] = frame["Passenger_Name"].fillna("Unknown").astype(str).str.strip()
    frame["Gender"] = frame["Gender"].fillna("Unknown").astype(str).str.strip()
    frame["Payment_Mode"] = frame["Payment_Mode"].fillna("Unknown").astype(str).str.strip()
    frame["Transport_Mode"] = frame["Transport_Mode"].astype(str).str.strip().str.title()
    frame["Booking_Status"] = frame["Booking_Status"].astype(str).str.strip().str.title()
    frame["Age"] = pd.to_numeric(frame["Age"], errors="coerce")
    frame["Ticket_Price"] = pd.to_numeric(frame["Ticket_Price"], errors="coerce")
    frame["Number_of_Tickets"] = pd.to_numeric(frame["Number_of_Tickets"], errors="coerce")
    frame["Booking_Date"] = pd.to_datetime(frame["Booking_Date"], errors="coerce")
    frame["Travel_Date"] = pd.to_datetime(frame["Travel_Date"], errors="coerce")

    invalid = (
        frame["Booking_ID"].isna() | frame["Booking_ID"].eq("")
        | frame["Booking_Date"].isna() | frame["Travel_Date"].isna()
        | frame["Source"].isna() | frame["Destination"].isna()
        | ~frame["Transport_Mode"].isin(["Bus", "Train"])
        | ~frame["Booking_Status"].isin(["Completed", "Confirmed", "Cancelled", "Pending"])
        | frame["Ticket_Price"].le(0)
        | frame["Number_of_Tickets"].lt(1)
        | (frame["Number_of_Tickets"] % 1 != 0)
    )
    invalid_count = int(invalid.sum())
    frame = frame.loc[~invalid].copy()

    valid_ages = frame["Age"].between(1, 100)
    age_median = float(frame.loc[valid_ages, "Age"].median()) if valid_ages.any() else 0.0
    frame.loc[~valid_ages, "Age"] = age_median
    frame["Age"] = frame["Age"].round().astype(int)
    frame["Number_of_Tickets"] = frame["Number_of_Tickets"].astype(int)
    frame["Revenue"] = frame["Ticket_Price"] * frame["Number_of_Tickets"]
    frame["Revenue_Eligible"] = frame["Booking_Status"].isin(["Completed", "Confirmed"])
    frame["Recognized_Revenue"] = frame["Revenue"].where(frame["Revenue_Eligible"], 0.0)
    frame["Booking_Month"] = frame["Booking_Date"].dt.to_period("M").astype(str)
    frame["Travel_Route"] = frame["Source"].astype(str) + " to " + frame["Destination"].astype(str)

    cleaning_summary = {
        "input_rows": original_count,
        "exact_duplicates_removed": duplicate_count,
        "invalid_rows_removed": invalid_count,
        "missing_cells_before_cleaning": missing_cells,
        "cleaned_rows": len(frame),
        "rows_removed": original_count - len(frame),
    }
    return frame.reset_index(drop=True), cleaning_summary