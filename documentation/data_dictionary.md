# Dataset Dictionary

The raw CSV is synthetic and contains 1,200 generated bookings plus eight exact duplicate rows used for cleaning demonstrations. Each normal row represents one booking transaction; `Number_of_Tickets` represents the number of seats/tickets in that transaction.

| Column | Type after cleaning | Meaning / rule |
|---|---|---|
| Booking_ID | string | Synthetic unique transaction identifier; exact duplicate rows repeat it. |
| Passenger_Name | string | Synthetic name label; missing values become `Unknown`. |
| Age | integer | Synthetic age in years; missing or out-of-range ages use the valid-age median. |
| Gender | string | Synthetic category; missing values become `Unknown`. |
| Transport_Mode | category | `Bus` or `Train`. |
| Source | string | Origin city. |
| Destination | string | Destination city, distinct from source. |
| Booking_Date | datetime | Synthetic date the transaction was recorded. |
| Travel_Date | datetime | Synthetic journey date, 1-90 days after booking. |
| Ticket_Price | numeric INR | Price per ticket; must be positive. |
| Number_of_Tickets | positive integer | Quantity in the transaction. |
| Booking_Status | category | `Completed`, `Confirmed`, `Cancelled`, or `Pending`. |
| Payment_Mode | string | Synthetic payment channel; missing values become `Unknown`. |
| Revenue | numeric INR | Derived gross booking value: price per ticket multiplied by quantity. |
| Revenue_Eligible | boolean | True for Completed or Confirmed transactions. |
| Recognized_Revenue | numeric INR | Revenue for eligible statuses; zero otherwise. Refunds are not modeled. |
| Booking_Month | YYYY-MM | Derived from Booking_Date for monthly reporting. |
| Travel_Route | string | Derived `Source to Destination` label. |

Exact rows identical across the raw schema are removed. Distinct transactions with similar passenger/route/date details remain; a similar-looking trip is not assumed to be a duplicate. Missing age, passenger name, gender, and payment mode are intentionally injected. Date, identity, route, mode, status, and numeric business-rule failures are rejected if encountered.