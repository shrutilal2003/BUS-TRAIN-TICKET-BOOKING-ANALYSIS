"""Create and save the project's Matplotlib charts."""

from pathlib import Path
from typing import Dict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def create_visualizations(data: pd.DataFrame, results: Dict[str, object], output_dir: Path) -> list:
    """Save ten charts based on calculated data and return their paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []

    def save_chart(name: str) -> None:
        path = output_dir / name
        plt.tight_layout()
        plt.savefig(path, dpi=160, bbox_inches="tight")
        plt.close()
        paths.append(path)

    destination = results["destination_summary"].sort_values("Booking_Count", ascending=False)
    plt.figure(figsize=(10, 5))
    plt.bar(destination["Destination"], destination["Booking_Count"], color="#277da1")
    plt.title("Bookings by Destination")
    plt.xlabel("Destination")
    plt.ylabel("Unique bookings")
    plt.xticks(rotation=35, ha="right")
    save_chart("bookings_by_destination.png")

    modes = results["mode_summary"]
    plt.figure(figsize=(6, 6))
    plt.pie(modes["Booking_Count"], labels=modes["Transport_Mode"], autopct="%1.1f%%", startangle=90)
    plt.title("Booking Distribution by Transport Mode")
    save_chart("transport_mode_distribution.png")

    plt.figure(figsize=(8, 5))
    plt.hist(data["Age"], bins=15, color="#43aa8b", edgecolor="white")
    plt.title("Passenger Age Distribution")
    plt.xlabel("Age (years)")
    plt.ylabel("Passenger booking records")
    save_chart("passenger_age_distribution.png")

    plt.figure(figsize=(7, 5))
    plt.bar(modes["Transport_Mode"], modes["Average_Ticket_Price"], color=["#f9c74f", "#577590"])
    plt.title("Average Ticket Price by Transport Mode")
    plt.xlabel("Transport mode")
    plt.ylabel("Average price per ticket (INR)")
    save_chart("average_price_by_mode.png")

    monthly = results["monthly_summary"]
    plt.figure(figsize=(11, 5))
    plt.plot(monthly["Booking_Month"], monthly["Booking_Count"], marker="o", color="#f3722c")
    plt.title("Monthly Booking Trend")
    plt.xlabel("Booking month")
    plt.ylabel("Unique bookings")
    plt.xticks(rotation=60, ha="right")
    save_chart("monthly_booking_trends.png")

    plt.figure(figsize=(11, 5))
    plt.plot(monthly["Booking_Month"], monthly["Recognized_Revenue"], marker="o", color="#277da1")
    plt.title("Monthly Recognized Revenue")
    plt.xlabel("Booking month")
    plt.ylabel("Recognized revenue (INR)")
    plt.xticks(rotation=60, ha="right")
    save_chart("monthly_revenue_trends.png")

    routes = results["route_summary"].head(10).sort_values("Booking_Count")
    plt.figure(figsize=(9, 6))
    plt.barh(routes["Travel_Route"], routes["Booking_Count"], color="#90be6d")
    plt.title("Top 10 Routes by Booking Count")
    plt.xlabel("Unique bookings")
    plt.ylabel("Source to destination")
    save_chart("top_10_routes.png")

    revenue = destination.sort_values("Recognized_Revenue", ascending=False)
    plt.figure(figsize=(10, 5))
    plt.bar(revenue["Destination"], revenue["Recognized_Revenue"], color="#f8961e")
    plt.title("Recognized Revenue by Destination")
    plt.xlabel("Destination")
    plt.ylabel("Recognized revenue (INR)")
    plt.xticks(rotation=35, ha="right")
    save_chart("revenue_by_destination.png")

    status = results["status_summary"]
    plt.figure(figsize=(7, 5))
    plt.bar(status["Booking_Status"], status["Booking_Count"], color="#577590")
    plt.title("Booking Status Distribution")
    plt.xlabel("Booking status")
    plt.ylabel("Unique bookings")
    save_chart("booking_status_distribution.png")

    plt.figure(figsize=(8, 5))
    plt.hist(data["Ticket_Price"], bins=20, color="#9b5de5", edgecolor="white")
    plt.title("Ticket Price Distribution")
    plt.xlabel("Price per ticket (INR)")
    plt.ylabel("Booking records")
    save_chart("ticket_price_distribution.png")
    return paths