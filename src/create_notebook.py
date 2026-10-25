"""Build the educational Jupyter notebook from maintainable cell definitions."""

from pathlib import Path

import nbformat

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "Bus_Train_Ticket_Booking_Analysis.ipynb"

MARKDOWN_CELLS = [
    "# Bus/Train Ticket Booking Data Analysis\n\nThis notebook uses a reproducible **synthetic** Indian booking dataset. It is not real operator or passenger data. Recognized revenue is Ticket_Price multiplied by Number_of_Tickets for Completed and Confirmed bookings only; refund accounting is outside scope.",
    "## 1. Imports and project paths\nThe notebook calls the same tested functions used by the command-line program.",
    "## 2. Load or generate source data\nThe fixed seed makes the generated dataset reproducible. Raw rows include intentional missing values and exact duplicates for cleaning demonstrations.",
    "## 3. Inspect missing values and exact duplicates\nOnly fully identical raw rows are duplicates. Similar-looking journeys with different booking IDs are retained.",
    "## 4. Clean and engineer features\nThe cleaner converts types, removes exact duplicates and invalid transactions, imputes selected fields, and derives route, month, and revenue values.",
    "## 5. Headline booking and revenue measures\nBooking count means unique transactions. Ticket count sums the tickets in each transaction. Cancelled and pending rows contribute zero recognized revenue.",
    "## 6. Destination and route patterns\nThese summaries describe this synthetic sample only and are not claims about actual travel demand.",
    "## 7. Passenger age and ticket prices\nAge groups, descriptive statistics, and NumPy percentiles summarize the generated records.",
    "## 8. Bus versus train and booking status\nAverage ticket price is per ticket; recognized revenue includes ticket quantity and eligible status.",
    "## 9. Monthly bookings and revenue\nMonths are based on Booking_Date. The dataset is for descriptive demonstration and does not forecast.",
    "## 10. Generate charts and export cleaned data\nSave the complete set of ten Matplotlib charts and the cleaned CSV.",
    "## 11. Interpretation and limitations\nAll apparent leaders, prices, age patterns, and seasonal changes come from assigned synthetic distributions. They are not evidence about real Indian passenger behavior or operator performance.",
]

CODE_CELLS = [
    "from pathlib import Path\nimport sys\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nfrom IPython.display import display\n\nPROJECT_ROOT = Path.cwd()\nif not (PROJECT_ROOT / 'src').exists():\n    PROJECT_ROOT = PROJECT_ROOT.parent\nsys.path.insert(0, str(PROJECT_ROOT))\n\nfrom src.generate_dataset import generate_booking_data\nfrom src.data_cleaning import clean_booking_data\nfrom src.analysis import build_analysis\nfrom src.visualizations import create_visualizations\n\nRAW_PATH = PROJECT_ROOT / 'data' / 'raw' / 'booking_data.csv'\nprint('Project root:', PROJECT_ROOT)",
    "if not RAW_PATH.exists():\n    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)\n    generate_booking_data().to_csv(RAW_PATH, index=False, date_format='%Y-%m-%d')\nraw_data = pd.read_csv(RAW_PATH)\nprint('Raw shape:', raw_data.shape)\ndisplay(raw_data.head())\nraw_data.info()",
    "display(raw_data.isna().sum().to_frame('Missing_Cells'))\nprint('Exact duplicate rows:', int(raw_data.duplicated().sum()))",
    "cleaned_data, cleaning_summary = clean_booking_data(raw_data)\ndisplay(pd.Series(cleaning_summary, name='Count').to_frame())\ndisplay(cleaned_data.head())\nprint('Missing values after cleaning:', int(cleaned_data.isna().sum().sum()))",
    "results = build_analysis(cleaned_data)\nmetrics = results['metrics']\ndisplay(pd.Series(metrics, name='Value').to_frame())\nprint('Age percentiles (25th, 50th, 75th):', results['numpy_age_percentiles'])",
    "display(results['destination_summary'].head(12))\ndisplay(results['route_summary'].head(10))",
    "display(results['age_summary'])\ndisplay(results['price_summary'])\nprint('NumPy age quartiles:', np.percentile(cleaned_data['Age'], [25, 50, 75]))",
    "display(results['mode_summary'])\ndisplay(results['status_summary'])",
    "monthly = results['monthly_summary']\ndisplay(monthly)\nfig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)\naxes[0].plot(monthly['Booking_Month'], monthly['Booking_Count'], marker='o')\naxes[0].set(title='Monthly Bookings', ylabel='Unique bookings')\naxes[1].plot(monthly['Booking_Month'], monthly['Recognized_Revenue'], marker='o', color='teal')\naxes[1].set(title='Monthly Recognized Revenue', xlabel='Booking month', ylabel='Revenue (INR)')\nplt.xticks(rotation=60, ha='right'); plt.tight_layout(); plt.show()",
    "processed_path = PROJECT_ROOT / 'data' / 'processed' / 'cleaned_booking_data.csv'\nprocessed_path.parent.mkdir(parents=True, exist_ok=True)\ncleaned_data.to_csv(processed_path, index=False, date_format='%Y-%m-%d')\nchart_paths = create_visualizations(cleaned_data, results, PROJECT_ROOT / 'figures')\nprint('Cleaned CSV:', processed_path)\nprint('Charts created:', len(chart_paths))\nfor chart_path in chart_paths:\n    print(chart_path.relative_to(PROJECT_ROOT))",
]


def main() -> None:
    """Write an unexecuted notebook; execution is performed separately by Jupyter."""
    notebook = nbformat.v4.new_notebook()
    cells = [nbformat.v4.new_markdown_cell(MARKDOWN_CELLS[0])]
    for index, markdown in enumerate(MARKDOWN_CELLS[1:]):
        cells.append(nbformat.v4.new_markdown_cell(markdown))
        if index < len(CODE_CELLS):
            cells.append(nbformat.v4.new_code_cell(CODE_CELLS[index]))
    notebook.cells = cells
    notebook.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.9.12"},
    }
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, NOTEBOOK_PATH)
    print("Created {} with {} cells".format(NOTEBOOK_PATH, len(notebook.cells)))


if __name__ == "__main__":
    main()
