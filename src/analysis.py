"""Booking, passenger, route, and revenue analyses."""

from typing import Dict

import numpy as np
import pandas as pd


def build_analysis(cleaned_data: pd.DataFrame) -> Dict[str, object]:
    """Calculate headline metrics and grouped summaries from cleaned records."""
    eligible = cleaned_data.loc[cleaned_data["Revenue_Eligible"]]
    destination_summary = cleaned_data.groupby("Destination", as_index=False).agg(
        Booking_Count=("Booking_ID", "nunique"), Ticket_Count=("Number_of_Tickets", "sum"),
        Recognized_Revenue=("Recognized_Revenue", "sum"),
    ).sort_values(["Booking_Count", "Destination"], ascending=[False, True])
    route_summary = cleaned_data.groupby("Travel_Route", as_index=False).agg(
        Booking_Count=("Booking_ID", "nunique"), Ticket_Count=("Number_of_Tickets", "sum"),
        Recognized_Revenue=("Recognized_Revenue", "sum"),
    ).sort_values(["Booking_Count", "Travel_Route"], ascending=[False, True])
    monthly_summary = cleaned_data.groupby("Booking_Month", as_index=False).agg(
        Booking_Count=("Booking_ID", "nunique"), Ticket_Count=("Number_of_Tickets", "sum"),
        Recognized_Revenue=("Recognized_Revenue", "sum"),
    ).sort_values("Booking_Month")
    mode_summary = cleaned_data.groupby("Transport_Mode", as_index=False).agg(
        Booking_Count=("Booking_ID", "nunique"), Ticket_Count=("Number_of_Tickets", "sum"),
        Average_Ticket_Price=("Ticket_Price", "mean"),
        Recognized_Revenue=("Recognized_Revenue", "sum"),
    )
    revenue_summary = mode_summary[["Transport_Mode", "Booking_Count", "Ticket_Count", "Recognized_Revenue"]].copy()
    age_groups = pd.cut(
        cleaned_data["Age"], bins=[0, 17, 25, 40, 60, 100],
        labels=["0-17", "18-25", "26-40", "41-60", "61+"], include_lowest=True,
    )
    age_summary = age_groups.value_counts(sort=False).rename_axis("Age_Group").reset_index(name="Passenger_Records")
    price_stats = cleaned_data["Ticket_Price"].agg(["mean", "min", "max", "median"]).to_dict()

    metrics = {
        "dataset_records": int(len(cleaned_data)),
        "total_bookings": int(cleaned_data["Booking_ID"].nunique()),
        "completed_bookings": int(cleaned_data["Booking_Status"].eq("Completed").sum()),
        "confirmed_bookings": int(cleaned_data["Booking_Status"].eq("Confirmed").sum()),
        "cancelled_bookings": int(cleaned_data["Booking_Status"].eq("Cancelled").sum()),
        "pending_bookings": int(cleaned_data["Booking_Status"].eq("Pending").sum()),
        "eligible_bookings": int(len(eligible)),
        "ticket_count": int(cleaned_data["Number_of_Tickets"].sum()),
        "eligible_ticket_count": int(eligible["Number_of_Tickets"].sum()),
        "recognized_revenue": float(cleaned_data["Recognized_Revenue"].sum()),
        "average_ticket_price": float(price_stats["mean"]),
        "minimum_ticket_price": float(price_stats["min"]),
        "maximum_ticket_price": float(price_stats["max"]),
        "most_popular_destination": str(destination_summary.iloc[0]["Destination"]),
        "age_mean": float(np.mean(cleaned_data["Age"])),
        "age_median": float(np.median(cleaned_data["Age"])),
        "eligible_average_ticket_price": float(eligible["Ticket_Price"].mean()) if len(eligible) else 0.0,
    }
    return {
        "metrics": metrics,
        "destination_summary": destination_summary,
        "route_summary": route_summary,
        "monthly_summary": monthly_summary,
        "mode_summary": mode_summary,
        "revenue_summary": revenue_summary,
        "age_summary": age_summary,
        "status_summary": cleaned_data["Booking_Status"].value_counts().rename_axis("Booking_Status").reset_index(name="Booking_Count"),
        "price_summary": cleaned_data["Ticket_Price"].describe().rename_axis("Statistic").reset_index(name="Ticket_Price"),
        "numpy_age_percentiles": np.percentile(cleaned_data["Age"], [25, 50, 75]).tolist(),
    }