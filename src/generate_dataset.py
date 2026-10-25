"""Create a reproducible synthetic Indian bus and train booking dataset."""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "booking_data.csv"
RANDOM_SEED = 20261019

CITY_NAMES = [
    "Delhi", "Lucknow", "Varanasi", "Jaipur", "Mumbai", "Patna",
    "Prayagraj", "Kanpur", "Kolkata", "Agra", "Bhopal", "Ranchi",
]
FIRST_NAMES = [
    "Aarav", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Meera",
    "Neha", "Rohan", "Sana", "Vihaan", "Zoya", "Aditi", "Kabir",
]
LAST_NAMES = [
    "Sharma", "Verma", "Singh", "Gupta", "Khan", "Patel", "Das",
    "Mishra", "Rao", "Joshi", "Yadav", "Roy",
]


def generate_booking_data(record_count: int = 1200, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Generate synthetic bookings with controlled missing and duplicate rows."""
    if record_count < 1000:
        raise ValueError("record_count must be at least 1,000")

    random = np.random.default_rng(seed)
    sources = random.choice(CITY_NAMES, record_count)
    destinations = random.choice(CITY_NAMES, record_count)
    same_city = sources == destinations
    while same_city.any():
        destinations[same_city] = random.choice(CITY_NAMES, int(same_city.sum()))
        same_city = sources == destinations

    booking_dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(
        random.integers(0, 650, record_count), unit="D"
    )
    travel_dates = booking_dates + pd.to_timedelta(random.integers(1, 91, record_count), unit="D")
    modes = random.choice(["Bus", "Train"], record_count, p=[0.54, 0.46])
    base_prices = np.where(modes == "Bus", random.uniform(350, 1800, record_count), random.uniform(500, 2600, record_count))
    route_distance_factor = random.uniform(0.75, 1.35, record_count)
    prices = np.round(base_prices * route_distance_factor, 2)

    frame = pd.DataFrame({
        "Booking_ID": ["BK{:06d}".format(number) for number in range(1, record_count + 1)],
        "Passenger_Name": ["{} {}".format(first, last) for first, last in zip(
            random.choice(FIRST_NAMES, record_count), random.choice(LAST_NAMES, record_count)
        )],
        "Age": random.integers(5, 81, record_count),
        "Gender": random.choice(["Female", "Male", "Other"], record_count, p=[0.46, 0.51, 0.03]),
        "Transport_Mode": modes,
        "Source": sources,
        "Destination": destinations,
        "Booking_Date": booking_dates,
        "Travel_Date": travel_dates,
        "Ticket_Price": prices,
        "Number_of_Tickets": random.integers(1, 6, record_count),
        "Booking_Status": random.choice(
            ["Completed", "Confirmed", "Cancelled", "Pending"],
            record_count, p=[0.70, 0.12, 0.12, 0.06]
        ),
        "Payment_Mode": random.choice(["UPI", "Card", "Net Banking", "Cash", "Wallet"], record_count),
    })

    # Missing values are intentional examples for the cleaning workflow.
    for column, count in (("Age", 12), ("Gender", 8), ("Payment_Mode", 10), ("Passenger_Name", 5)):
        missing_rows = random.choice(record_count, count, replace=False)
        frame.loc[missing_rows, column] = np.nan

    # Exact duplicate rows are injected separately from legitimate repeated trips.
    duplicate_rows = frame.sample(n=8, random_state=seed)
    return pd.concat([frame, duplicate_rows], ignore_index=True)


def main() -> None:
    """Write the generated dataset to the project's raw data directory."""
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset = generate_booking_data()
    dataset.to_csv(RAW_DATA_PATH, index=False, date_format="%Y-%m-%d")
    print("Created synthetic dataset: {} ({} rows)".format(RAW_DATA_PATH, len(dataset)))


if __name__ == "__main__":
    main()