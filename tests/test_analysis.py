"""Unit tests for synthetic generation, cleaning, and core calculations."""

import unittest
import tempfile
from pathlib import Path

import pandas as pd

from src.analysis import build_analysis
from src.data_cleaning import clean_booking_data
from src.data_loader import load_booking_data
from src.generate_dataset import generate_booking_data


class BookingAnalysisTests(unittest.TestCase):
    def test_generator_is_reproducible_and_includes_duplicate_examples(self):
        first = generate_booking_data(1000, seed=17)
        second = generate_booking_data(1000, seed=17)
        pd.testing.assert_frame_equal(first, second)
        self.assertEqual(len(first), 1008)

    def test_cleaning_removes_only_exact_duplicate_rows(self):
        raw = generate_booking_data(1000, seed=22)
        cleaned, summary = clean_booking_data(raw)
        self.assertEqual(summary["exact_duplicates_removed"], 8)
        self.assertEqual(len(cleaned), 1000)
        self.assertTrue(cleaned["Age"].between(1, 100).all())

    def test_cancelled_and_pending_records_do_not_contribute_to_revenue(self):
        raw = pd.DataFrame([
            {"Booking_ID": "A", "Passenger_Name": "A", "Age": 30, "Gender": "Other",
             "Transport_Mode": "Bus", "Source": "Delhi", "Destination": "Jaipur",
             "Booking_Date": "2025-01-01", "Travel_Date": "2025-01-02", "Ticket_Price": 100,
             "Number_of_Tickets": 2, "Booking_Status": "Completed", "Payment_Mode": "UPI"},
            {"Booking_ID": "B", "Passenger_Name": "B", "Age": 30, "Gender": "Other",
             "Transport_Mode": "Train", "Source": "Delhi", "Destination": "Mumbai",
             "Booking_Date": "2025-01-01", "Travel_Date": "2025-01-02", "Ticket_Price": 200,
             "Number_of_Tickets": 1, "Booking_Status": "Cancelled", "Payment_Mode": "Card"},
            {"Booking_ID": "C", "Passenger_Name": "C", "Age": 30, "Gender": "Other",
             "Transport_Mode": "Train", "Source": "Delhi", "Destination": "Patna",
             "Booking_Date": "2025-01-01", "Travel_Date": "2025-01-02", "Ticket_Price": 300,
             "Number_of_Tickets": 1, "Booking_Status": "Pending", "Payment_Mode": "Card"},
        ])
        cleaned, _ = clean_booking_data(raw)
        result = build_analysis(cleaned)
        self.assertEqual(result["metrics"]["recognized_revenue"], 200)
        self.assertEqual(result["metrics"]["ticket_count"], 4)

    def test_missing_age_is_imputed_and_missing_fields_are_resolved(self):
        raw = generate_booking_data(1000, seed=31)
        cleaned, _ = clean_booking_data(raw)
        self.assertFalse(cleaned[["Age", "Gender", "Payment_Mode", "Passenger_Name"]].isna().any().any())

    def test_loader_reports_missing_file(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing_path = Path(temporary_directory) / "missing.csv"
            with self.assertRaises(FileNotFoundError):
                load_booking_data(missing_path)

    def test_loader_rejects_incomplete_schema(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "incomplete.csv"
            pd.DataFrame({"Booking_ID": ["BK000001"]}).to_csv(csv_path, index=False)
            with self.assertRaisesRegex(ValueError, "missing required columns"):
                load_booking_data(csv_path)


if __name__ == "__main__":
    unittest.main()