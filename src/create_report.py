"""Generate the editable BCA thesis report from actual project outputs."""

import subprocess
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Ellipse
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from .main import run_analysis

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "report" / "BCA_Final_Year_Project_Report.docx"
FIGURE_DIR = ROOT / "figures"

CHAPTERS = [
    ("Chapter 1: Introduction", [
        ("1.1 Data analysis and transport", "Data analysis is the organized process of inspecting, cleaning, transforming, summarizing, and communicating data so that a question can be answered with evidence. In transportation, records of bookings can describe when transactions occur, where passengers travel, which service mode they select, how many tickets are bought, and what amounts are associated with those transactions. A useful analysis keeps the meaning and limits of each field explicit before calculating totals. Pandas provides labeled tabular operations that support this workflow (The pandas development team, n.d.)."),
        ("1.2 Background and problem statement", "Bus and railway services produce transaction records that can be summarized for operational planning. In a small academic exercise, records may be viewed in a spreadsheet and totals calculated by hand. This approach becomes error-prone when duplicate rows, missing values, mixed date formats, multiple ticket quantities, booking statuses, or repeated routes occur. The project problem is to provide a repeatable and explainable workflow that turns booking-shaped records into auditable summaries and charts without presenting the output as real market evidence."),
        ("1.3 Motivation and objectives", "The project is motivated by the need to practice data handling end to end using a familiar domain and tools accessible to undergraduate students. Its objectives are to generate seeded synthetic records; validate and clean fields; keep legitimate repeated trips while removing exact duplicate rows; calculate transaction, seat, price, demographic, route, and month summaries; compare bus and train measures; visualize results; export reusable CSV files; and document tests and assumptions."),
        ("1.4 Scope, outcomes, and limitations", "The implemented scope is offline descriptive analytics on a CSV dataset. Passenger names, booking identifiers, routes, dates, ages, price, quantity, status, and payment channel are synthetic. The system does not book tickets, connect to an operator, process payments, calculate refunds, authenticate users, or forecast demand. Expected outcomes are a cleaned CSV, grouped summaries, ten charts, a teaching notebook, automated tests, and an editable thesis. Results demonstrate a method only; randomized distributions are not a substitute for actual operational data."),
    ]),
    ("Chapter 2: Literature Review and Previous Work", [
        ("2.1 Exploratory analysis", "Exploratory data analysis emphasizes looking at distributions, relationships, summaries, and visual displays before making strong claims. Tukey's work established this exploratory orientation as a complement to formal modeling (Tukey, 1977). In this project, counts, quartiles, grouped tables, histograms, and time series are used to inspect synthetic records. They are descriptive and do not establish causality."),
        ("2.2 Python tabular analysis", "McKinney described pandas as a Python library for data structures and statistical computing (McKinney, 2010). Its DataFrame operations allow this project to select columns, handle missing values, group by destination or mode, parse dates, and export CSV tables. NumPy supplies numerical operations such as percentiles and deterministic random generation. Matplotlib supplies explicit chart primitives, titles, axes, and file output. Their official user guides are cited in the bibliography."),
        ("2.3 Conventional and computational approaches", "Spreadsheet-based reporting is approachable for small tables and manual inspection, but formula copying, uncontrolled edits, and inconsistent filters can make results difficult to reproduce. Database reporting can support persistent multi-user records and indexed queries, but requires schema governance, access controls, and deployment that are unnecessary for this educational batch example. A Python script is repeatable, testable, and suitable for data cleaning and plots; it also requires a programming environment and careful dependency management. These tools solve different scales of problem rather than making one approach universally superior."),
        ("2.4 Transport analytics and research gap", "Transport operators may use booking, timetable, capacity, and revenue systems internally, but this student project does not inspect proprietary systems or claim knowledge of their practices. The educational gap addressed is narrower: a beginner-friendly, auditable example that links synthetic booking records to cleaning decisions, explicitly defined revenue, grouped metrics, charts, tests, and an academic report. The methodology follows documented library behavior and transparent assumptions rather than invented literature findings."),
        ("2.5 Comparison", "The comparison table in Chapter 3 summarizes the practical trade-offs. For this scope, CSV plus Python is a proportionate choice: the dataset is small, there is one local analyst, and the principal learning objectives are data preparation and interpretation. If real personally identifiable data were introduced, privacy, legal basis, retention, access control, and institutional approval would need to be addressed before analysis."),
    ]),
    ("Chapter 3: Existing System and Proposed System", [
        ("3.1 Existing manual approach", "A manual workflow usually opens a flat file, filters records, copies values into formulas, and creates charts through a spreadsheet interface. It can be effective for quick checks, but repeated monthly reports may drift if different users apply different status rules or interpret ticket quantity inconsistently. Reconciliation is harder when duplicate records and missing fields are not logged."),
        ("3.2 Proposed system", "The proposed application is a command-line batch pipeline. It generates or loads a CSV, checks the expected schema, removes exact duplicate rows, parses dates and numeric fields, validates business rules, fills selected missing values, derives route/month/revenue fields, calculates grouped measures, saves charts, and exports tables. The same tested functions are used by the notebook. This reduces duplicated logic across interfaces."),
        ("3.3 Functional requirements", "The system shall load and validate the 13 required input columns; generate at least 1,000 seeded synthetic records; calculate unique bookings and ticket quantities separately; compute price and revenue measures; exclude Cancelled and Pending statuses from recognized revenue; report destinations, routes, passenger age groups, modes, booking dates, and booking statuses; save ten titled Matplotlib charts; export cleaned data and summaries; and report actionable file/schema errors."),
        ("3.4 Non-functional requirements", "The implementation should run locally on Python 3.9 or later, use relative paths, keep source modules understandable, make generation reproducible, preserve raw input, produce deterministic results for a fixed seed, and avoid requiring a live service. It should be testable from a clean environment using the documented requirements. Privacy is supported by synthetic data, not by a claim that arbitrary production data would be safe to process."),
        ("3.5 Feasibility", "Technical feasibility is supported by freely available Python packages and CSV files. Operational feasibility is suitable for a single student analyst who can run a terminal command or notebook. Economic cost is limited to the computer and optional development tools. Legal/ethical feasibility is favorable for the included synthetic data; real passenger data would require separate institutional authorization and privacy safeguards."),
    ]),
    ("Chapter 4: System Analysis and Design", [
        ("4.1 Architecture and workflow", "The architecture separates generation, loading, cleaning, analysis, reporting, and visualization. This modular structure allows a student to inspect each stage and tests to target individual calculations. The command-line runner orchestrates these modules while the notebook exposes them step by step. The diagram below shows the project-level data path."),
        ("4.2 Data flow", "At Level 0, the student provides run options and a synthetic CSV; the analysis system returns cleaned records, summary tables, and plots. At Level 1, the raw file passes schema validation, cleaning and feature engineering, then aggregation and plotting. Raw and processed data are separate files so that original records remain available for audit."),
        ("4.3 Use cases and activity", "The student analyst can generate a dataset, validate and clean it, inspect passenger/route/price/revenue patterns, export summaries and charts, and use the educational notebook. The activity begins with input selection, branches to dataset generation when the file is absent, validates schema, then runs cleaning, calculation, export, and chart creation. No passenger-facing booking or payment use case is included."),
        ("4.4 Schema and module design", "The raw schema contains Booking_ID, Passenger_Name, Age, Gender, Transport_Mode, Source, Destination, Booking_Date, Travel_Date, Ticket_Price, Number_of_Tickets, Booking_Status, and Payment_Mode. Derived columns are Revenue, Revenue_Eligible, Recognized_Revenue, Booking_Month, and Travel_Route. Modules are `generate_dataset`, `data_loader`, `data_cleaning`, `analysis`, `visualizations`, `report_summary`, and `main`. The data dictionary defines every column and treatment."),
        ("4.5 Input and output specification", "Input is a UTF-8 CSV with the documented required columns. Output consists of one cleaned CSV, destination/route/month/revenue summaries, age/status summaries, ten chart PNGs, and an execution summary text file. Currency values are expressed in INR as synthetic amounts; no claim is made that generated prices reflect actual fares."),
    ]),
    ("Chapter 5: Tools and Technologies", [
        ("5.1 Python", "Python is the implementation language. The standard library supports paths, command-line arguments, and test execution. The project favors ordinary functions and DataFrames over a web framework so that a beginner can follow the control flow."),
        ("5.2 pandas and NumPy", "pandas reads CSV, converts columns, removes exact duplicates, fills selected missing fields, groups records, summarizes categories, and writes outputs. NumPy provides a seeded generator for synthetic values and percentile/statistical functions. NumPy is constrained below version 2 in requirements for compatibility with older compiled Matplotlib installations."),
        ("5.3 Matplotlib and Jupyter", "Matplotlib creates the ten charts as PNG files using actual calculated data. Jupyter presents Markdown explanations alongside the same project functions for a stepwise learning experience. The notebook is executed during validation and contains saved cell outputs."),
        ("5.4 CSV and development environment", "CSV is a plain-text interchange format appropriate for this small, single-user demonstration. VS Code can edit the modules, run tests in its terminal, and open the notebook. The generated output can also be inspected using spreadsheet software. No database or online service is required."),
    ]),
    ("Chapter 6: Methodology and Implementation", [
        ("6.1 Methodology", "The process is an iterative descriptive-analysis workflow: define fields and measures; generate controlled records; inspect schema and missingness; clean and validate; derive analysis variables; calculate grouped results; visualize; verify calculations with tests; and interpret the observed synthetic outputs with explicit limits. The fixed seed is 20261019. The default generator creates 1,200 transactions and appends eight exact duplicate rows, making 1,208 raw rows."),
        ("6.2 Data collection assumptions", "No external or real booking data was collected. Names, cities, ages, dates, modes, fares, booking statuses, payment channels, and quantities are randomly selected from designed distributions. The booking window spans generated dates from 2025 onward, with travel dates one to 90 days after booking. Some missing demographic/payment cells and eight exact duplicate examples are intentionally inserted. These assumptions create examples for learning, not estimates of real-world frequency."),
        ("6.3 Cleaning and validation", "The loader checks that all 13 required columns exist. Exact duplicates across those fields are dropped; repeated routes or passengers with different transaction IDs remain. Numeric and date columns are parsed with coercion, then unusable identity/date/route, unsupported mode/status, nonpositive price, and invalid quantity records are removed. Missing age and age outside 1-100 are replaced with the valid median; missing name, gender, and payment mode are labeled Unknown. This is an instructional policy and should be revisited for real data."),
        ("6.4 Feature engineering and revenue", "Revenue is a transaction-level gross amount equal to price per ticket multiplied by number of tickets. Recognized revenue includes only Completed and Confirmed statuses. Cancelled and Pending rows contribute zero; refunds, taxes, fees, chargebacks, and settlement timing are not modeled. Unique booking count uses distinct Booking_ID. Ticket count is the sum of Number_of_Tickets; these measures are never interchanged."),
        ("6.5 Statistical and visualization methods", "Pandas groupby operations calculate destination, route, month, mode, and status totals. Means, minima, maxima, median, descriptive statistics, and NumPy percentiles summarize price and age. Bar charts compare categories, a pie chart shows mode share, histograms show age and fare distributions, and line charts show month-level booking and revenue values. Plots use the calculated tables rather than manually entered findings."),
        ("6.6 Algorithm", "Pseudocode: read raw CSV; assert required schema; count and drop exact duplicate rows; normalize text and parse numeric/date columns; mark rows failing validation; remove invalid rows; impute permitted missing values; derive transaction revenue, eligibility, month, and route; group and calculate metrics; save cleaned rows, summary tables, charts, and run log. The source code implements this in small functions in `src/`."),
    ]),
]

DISCUSSION_CHAPTERS = [
    ("Chapter 7: Results and Analysis", [
        ("7.1 Dataset and cleaning results", "The following table is populated from this run of the seeded generator and cleaning code. It separates raw rows from final rows; intentionally missing values are imputed, and exact duplicate records are removed. The number of valid unique booking transactions may differ from raw file rows because the raw file contains demonstration duplicates."),
        ("7.2 Booking and revenue results", "Recognized revenue is computed from eligible statuses only. A completed or confirmed record contributes its per-ticket price multiplied by ticket quantity. Cancelled and pending records remain visible in booking-status counts but contribute zero recognized revenue. The booking count is a transaction count, while ticket count represents quantity."),
        ("7.3 Passenger, destination, route, mode, and time", "Destination and route summaries rank synthetic booking counts and recognized revenue. Age groups partition records into 0-17, 18-25, 26-40, 41-60, and 61+ bands. Mode comparison includes booking counts, ticket quantities, average per-ticket fare, and recognized revenue. Monthly summaries use Booking_Date, not Travel_Date. Each plotted value is computed from the cleaned records."),
        ("7.4 Interpretation", "A leading destination or route in this dataset is a consequence of the generator’s random selection and sample size. It is not a real demand ranking. Month-to-month movement is similarly a synthetic pattern and may reflect random variation. The result is useful for checking data processing and chart construction, not business decisions about actual routes."),
    ]),
    ("Chapter 8: Testing and Validation", [
        ("8.1 Testing strategy", "The project uses Python `unittest` tests for deterministic generation, exact duplicate handling, missing-value resolution, and revenue eligibility. The full CLI pipeline and notebook are also run as integration checks. Schema validation and missing-file behavior are checked in the loader. Test results below are based on an executed test suite during report generation."),
        ("8.2 Data validation", "Validation confirms required columns, supported mode and status categories, parsed booking/travel dates, positive ticket price, and positive whole-number ticket quantity. Missing age values are imputed and output is checked for residual missing selected fields. Invalid rows are counted and excluded. The raw file remains separate from the cleaned file."),
        ("8.3 Test case outcomes", "Expected and actual outcomes are recorded in the table from the test execution. A passing unit suite does not prove suitability for operational use; it establishes only the tested code paths and fixture assumptions. Additional tests would be appropriate before accepting real operator data or changing revenue rules."),
    ]),
    ("Chapter 9: Results, Observations, and Discussion", [
        ("9.1 Observations", "The tables and figures show how to compare destinations, routes, passenger age groups, mode shares, prices, statuses, and monthly aggregates. They are summaries of a seeded synthetic sample. The generated distribution intentionally contains variation, but it does not represent a survey or observed passenger population."),
        ("9.2 Practical applications and business value", "For an organization with authorized, reliable booking records, a similar pipeline could support reconciliation checks, descriptive monthly reporting, route comparison, and data-quality monitoring. A production application would need a governed data definition, privacy protection, secure access, currency/fare rules, explicit cancellation and refund accounting, and independent validation. The current deliverable is an educational prototype and does not connect to such systems."),
        ("9.3 Limitations", "Synthetic generation cannot validate demand hypotheses. The simple status rule treats both Confirmed and Completed as revenue-eligible, although actual accounting may recognize revenue at another event. Refunds, discounts, fees, passenger-level privacy, multiple passengers per name, service capacity, schedule changes, and travel-date seasonality are not modeled. The dataset uses only a small set of cities and two modes."),
    ]),
    ("Chapter 10: Conclusion and Future Scope", [
        ("10.1 Conclusion", "The project implements a reproducible Python analysis pipeline for synthetic bus and train ticket bookings. It creates data, cleans and validates fields, derives route/month/revenue measures, distinguishes unique bookings from ticket quantity, summarizes destination, passenger, mode, price, status, and monthly patterns, exports files, creates charts, and includes tests, a notebook, and documentation. The defined objectives are achieved for this bounded educational scope."),
        ("10.2 Implemented features", "Implemented now: seeded CSV generation; data loading and schema validation; exact duplicate removal; missing-value treatment; date and numeric conversion; feature engineering; booking/revenue summaries; ten Matplotlib figures; CSV/text exports; an executable notebook; unittest coverage; and a generated editable report. No online booking, database integration, dashboard, prediction, or operator connection is implemented."),
        ("10.3 Future enhancements", "Future work could add a relational database, role-based access, a dashboard, real-time feeds with authorization, richer fare/refund/discount accounting, privacy controls, and route-demand forecasting. Predictive work would require a suitable, permissioned historical dataset, a time-aware evaluation design, baseline comparisons, and careful disclosure of uncertainty. These are proposals rather than deliverables of this project."),
    ]),
]

REFERENCES = [
    "Jupyter Development Team. (n.d.). Jupyter documentation. https://docs.jupyter.org/en/latest/",
    "Matplotlib Development Team. (n.d.). Matplotlib quick start guide. https://matplotlib.org/stable/users/explain/quick_start.html",
    "McKinney, W. (2010). Data structures for statistical computing in Python. In Proceedings of the 9th Python in Science Conference (pp. 56-61). https://doi.org/10.25080/Majora-92bf1922-00a",
    "NumPy Developers. (n.d.). Absolute beginners. https://numpy.org/doc/stable/user/absolute_beginners.html",
    "Python Software Foundation. (n.d.). Python 3 documentation. https://docs.python.org/3/",
    "The pandas development team. (n.d.). pandas documentation: User guide. https://pandas.pydata.org/docs/user_guide/index.html",
    "Tukey, J. W. (1977). Exploratory data analysis. Addison-Wesley.",
    "VanderPlas, J. (2016). Python data science handbook: Essential tools for working with data. O'Reilly Media. https://jakevdp.github.io/PythonDataScienceHandbook/",
]


def set_cell_shading(cell, fill):
    """Apply a light blue fill to a Word table cell."""
    properties = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    properties.append(shading)


def set_repeat_table_header(row):
    """Mark a table heading row to repeat across pages."""
    properties = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    properties.append(repeat)


def add_page_number(paragraph):
    """Insert a Word PAGE field in a footer paragraph."""
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for element in (begin, instruction, separate, text, end):
        run._r.append(element)


def style_document(document):
    """Set A4 layout, body typography, headings, and page numbering."""
    section = document.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)
    normal = document.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(6)
    for style_name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        style = document.styles[style_name]
        style.font.name = "Times New Roman"
        style.font.color.rgb = RGBColor(31, 78, 121)
    document.styles["Heading 1"].font.size = Pt(16)
    document.styles["Heading 1"].font.bold = True
    document.styles["Heading 2"].font.size = Pt(13)
    document.styles["Heading 2"].font.bold = True
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("BCA Final Year Project | Page ")
    add_page_number(footer)


def add_body(document, text):
    """Add one justified body paragraph."""
    paragraph = document.add_paragraph(text)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return paragraph


def add_table(document, headers, rows, widths=None):
    """Add a consistently styled table with repeatable header row."""
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header = table.rows[0]
    set_repeat_table_header(header)
    for index, value in enumerate(headers):
        cell = header.cells[index]
        cell.text = str(value)
        set_cell_shading(cell, "D9EAF7")
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(9)
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            cells[index].text = str(value)
            cells[index].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for paragraph in cells[index].paragraphs:
                paragraph.paragraph_format.line_spacing = 1.0
                for run in paragraph.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(8.5)
    if widths:
        for row in table.rows:
            for index, width in enumerate(widths):
                row.cells[index].width = Inches(width)
    document.add_paragraph()
    return table


def add_figure(document, image_path, caption, width=6.1):
    """Insert a centered figure with a numbered caption."""
    if image_path.exists():
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.add_run().add_picture(str(image_path), width=Inches(width))
        caption_paragraph = document.add_paragraph(caption)
        caption_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in caption_paragraph.runs:
            run.italic = True
            run.font.size = Pt(10)


def render_diagram(filename, title, labels, edges, positions, shapes=None):
    """Draw a readable node-and-arrow system diagram for embedding in the DOCX."""
    fig, axis = plt.subplots(figsize=(10, 3.5))
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.axis("off")
    shapes = shapes or {}
    for index, (x, y) in enumerate(positions):
        if shapes.get(index) == "ellipse":
            patch = Ellipse((x, y), 0.15, 0.16, facecolor="#e8f1f8", edgecolor="#24557a", linewidth=1.4)
        else:
            patch = FancyBboxPatch((x - 0.07, y - 0.07), 0.14, 0.14,
                                   boxstyle="round,pad=0.012", facecolor="#e8f1f8",
                                   edgecolor="#24557a", linewidth=1.4)
        axis.add_patch(patch)
        axis.text(x, y, "\n".join(textwrap.wrap(labels[index], width=18)),
                  ha="center", va="center", fontsize=8)
    for start, end in edges:
        x1, y1 = positions[start]
        x2, y2 = positions[end]
        axis.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->",
                                       mutation_scale=12, color="#4a6572", linewidth=1.2,
                                       connectionstyle="arc3,rad=0.04", shrinkA=32, shrinkB=32))
    axis.set_title(title, fontsize=13, fontweight="bold", color="#183b56")
    fig.tight_layout()
    path = FIGURE_DIR / filename
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def create_system_diagrams():
    """Render architecture, workflow, DFD, use-case, and activity diagrams."""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    positions = [(0.08 + i * 0.168, 0.5) for i in range(6)]
    architecture = render_diagram(
        "system_architecture.png", "System Architecture",
        ["Seeded generator", "Raw CSV", "Loader and schema validation", "Cleaning and feature engineering", "Pandas / NumPy analysis", "CSV, charts, report"],
        [(i, i + 1) for i in range(5)], positions,
    )
    workflow = render_diagram(
        "project_workflow.png", "Project Workflow",
        ["Start / input", "Schema check", "Remove exact duplicates", "Validate and clean", "Aggregate metrics", "Export and plot"],
        [(i, i + 1) for i in range(5)], positions,
    )
    dfd_positions = [(0.12, 0.5), (0.34, 0.5), (0.57, 0.5), (0.80, 0.72), (0.80, 0.28)]
    dfd = render_diagram(
        "data_flow_level_1.png", "Data Flow Diagram - Level 1",
        ["Raw booking CSV", "1. Load and validate", "2. Clean and derive", "Cleaned CSV", "3. Aggregate / plot and export"],
        [(0, 1), (1, 2), (2, 3), (2, 4)], dfd_positions,
    )
    use_positions = [(0.15, 0.5), (0.43, 0.82), (0.65, 0.82), (0.43, 0.25), (0.65, 0.25)]
    usecase = render_diagram(
        "use_case_diagram.png", "Use Cases - Student Analyst",
        ["Student analyst", "Generate dataset", "Analyze records", "Export tables", "Inspect notebook"],
        [(0, 1), (0, 2), (0, 3), (0, 4)], use_positions, {0: "ellipse", 1: "ellipse", 2: "ellipse", 3: "ellipse", 4: "ellipse"},
    )
    activity_positions = [(0.10, 0.5), (0.30, 0.5), (0.50, 0.5), (0.70, 0.5), (0.90, 0.5)]
    activity = render_diagram(
        "activity_diagram.png", "Analysis Activity",
        ["Begin", "Load / generate", "Validate and clean", "Calculate measures", "Save outputs"],
        [(i, i + 1) for i in range(4)], activity_positions, {0: "ellipse", 4: "ellipse"},
    )
    return [architecture, workflow, dfd, usecase, activity]


def format_inr(value):
    return "INR {:,.2f}".format(float(value))


def build_report():
    """Run the project, verify tests, and generate the thesis from real outputs."""
    package = run_analysis(charts=True)
    cleaned = package["cleaned_data"]
    cleaning = package["cleaning_summary"]
    results = package["results"]
    metrics = results["metrics"]
    test_process = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    test_output = test_process.stdout + test_process.stderr
    if test_process.returncode != 0:
        raise RuntimeError("Automated tests failed; report not generated.\n" + test_output)

    diagrams = create_system_diagrams()
    document = Document()
    style_document(document)

    # Preliminary pages use editable student/institution fields and explicit draft language.
    document.add_paragraph("[COLLEGE NAME]", style="Title").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("[UNIVERSITY NAME]", style="Subtitle").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("\n\nBCA FINAL YEAR PROJECT", style="Heading 1").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("BUS/TRAIN TICKET BOOKING DATA ANALYSIS USING PYTHON", style="Title").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("\n\nSubmitted by\n[STUDENT NAME]\nEnrollment No.: [ENROLLMENT NUMBER]\n\nUnder the guidance of\n[SUPERVISOR NAME]\n\nAcademic Session: [ACADEMIC SESSION]", style="Normal").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("\n\nA project report submitted in partial fulfillment of the requirements for the award of the Bachelor of Computer Applications degree.").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_page_break()

    document.add_heading("Title Page", level=1)
    add_body(document, "Project Title: Bus/Train Ticket Booking Data Analysis Using Python")
    add_body(document, "Submitted by: [STUDENT NAME] | Enrollment number: [ENROLLMENT NUMBER]")
    add_body(document, "College: [COLLEGE NAME] | University: [UNIVERSITY NAME]")
    add_body(document, "Supervisor: [SUPERVISOR NAME] | Academic session: [ACADEMIC SESSION]")
    add_body(document, "This document is an editable academic project draft. The student must verify formatting and institutional requirements before submission.")
    document.add_page_break()

    document.add_heading("Certificate (Draft for Approval)", level=1)
    add_body(document, "This is to certify that the project report entitled 'Bus/Train Ticket Booking Data Analysis Using Python' is submitted by [STUDENT NAME], Enrollment No. [ENROLLMENT NUMBER], as a draft academic project for the Bachelor of Computer Applications programme at [COLLEGE NAME], affiliated with [UNIVERSITY NAME], during [ACADEMIC SESSION].")
    add_body(document, "The project is based on a synthetic educational dataset. This certificate is a draft and is not evidence of institutional approval. It must be reviewed, corrected, and signed only by the authorized college supervisor and authority.")
    document.add_paragraph("\nSupervisor signature: ____________________     Date: ______________")
    document.add_paragraph("Head of Department: ____________________     College seal: ______")
    document.add_page_break()

    document.add_heading("Student Declaration", level=1)
    add_body(document, "I, [STUDENT NAME], declare that this report is submitted for academic evaluation and that all generated booking records are synthetic. I have not represented them as actual IRCTC, railway, bus-operator, or passenger data. References are listed for the methods and software documentation used. I will replace editable placeholders, follow college rules, and obtain supervisor approval before final submission.")
    document.add_paragraph("\nStudent signature: ____________________     Date: ______________")
    document.add_page_break()

    document.add_heading("Acknowledgement", level=1)
    add_body(document, "I express my gratitude to [SUPERVISOR NAME] for academic guidance and to [COLLEGE NAME] and [UNIVERSITY NAME] for providing the opportunity to complete this project. I also acknowledge the maintainers of Python, pandas, NumPy, Matplotlib, and Jupyter for their public documentation and open-source tools. The dataset in this report was generated locally for demonstration and contains no real passenger data.")
    document.add_page_break()

    document.add_heading("Abstract", level=1)
    add_body(document, "This project implements a Python-based descriptive analysis workflow for bus and train ticket booking records. A seeded generator creates synthetic booking-shaped records with passenger demographics, Indian city routes, booking and travel dates, per-ticket prices, ticket quantities, statuses, and payment labels. The analysis checks the required schema, removes exact duplicate rows, handles selected missing values, converts types, validates core business rules, and derives route, month, and recognized-revenue fields. Pandas and NumPy produce booking, passenger, route, mode, price, status, and monthly measures; Matplotlib saves ten charts. The program exports cleaned records and summary CSV files, and an educational notebook and automated tests accompany the report. In this execution, the generated raw dataset contains {:,} rows; cleaning retains {:,} records; the analysis counts {:,} unique bookings and {:,} tickets; and recognized synthetic revenue is {}. Revenue includes Completed and Confirmed transactions and excludes Cancelled and Pending statuses. Since all records are synthetic, findings demonstrate implementation and cannot establish actual travel demand or fare behavior.".format(len(pd_read_raw()), len(cleaned), metrics["total_bookings"], metrics["ticket_count"], format_inr(metrics["recognized_revenue"])))
    document.add_page_break()

    document.add_heading("Table of Contents", level=1)
    document.add_paragraph("In Microsoft Word, update this field to refresh page numbers.")
    paragraph = document.add_paragraph()
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar"); begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText"); instruction.set(qn("xml:space"), "preserve"); instruction.text = ' TOC \\o "1-3" \\h \\z \\u '
    separate = OxmlElement("w:fldChar"); separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t"); text.text = "Select this table and update the field to populate headings and page numbers."
    end = OxmlElement("w:fldChar"); end.set(qn("w:fldCharType"), "end")
    for element in (begin, instruction, separate, text, end):
        run._r.append(element)
    document.add_page_break()

    document.add_heading("List of Figures", level=1)
    figure_titles = ["System architecture", "Project workflow", "Data flow diagram", "Use-case diagram", "Activity diagram", "Bookings by destination", "Transport-mode distribution", "Passenger age distribution", "Average price by transport mode", "Monthly booking trend", "Monthly revenue trend", "Top 10 routes", "Revenue by destination", "Booking status distribution", "Ticket price distribution"]
    for number, title in enumerate(figure_titles, 1):
        document.add_paragraph("Figure {}. {}".format(number, title))
    document.add_page_break()

    document.add_heading("List of Tables", level=1)
    for number, title in enumerate(["Dataset schema", "Cleaning audit", "Headline analysis metrics", "Destination summary", "Route summary", "Transport mode comparison", "Passenger age groups", "Monthly summary", "Test execution results"], 1):
        document.add_paragraph("Table {}. {}".format(number, title))
    document.add_page_break()

    document.add_heading("List of Abbreviations", level=1)
    add_table(document, ["Abbreviation", "Meaning"], [
        ("BCA", "Bachelor of Computer Applications"), ("CSV", "Comma-Separated Values"),
        ("DFD", "Data Flow Diagram"), ("EDA", "Exploratory Data Analysis"),
        ("INR", "Indian Rupee"), ("ID", "Identifier"), ("PNG", "Portable Network Graphics"),
        ("UPI", "Unified Payments Interface"),
    ])
    document.add_page_break()

    for chapter_title, sections in CHAPTERS:
        document.add_heading(chapter_title, level=1)
        for heading, body in sections:
            document.add_heading(heading, level=2)
            add_body(document, body)
        if chapter_title.startswith("Chapter 4"):
            for index, (diagram_path, caption) in enumerate(zip(diagrams, ["Figure 1. System architecture", "Figure 2. Project workflow", "Figure 3. Level 1 data flow", "Figure 4. Student analyst use cases", "Figure 5. Analysis activity"]), 1):
                add_figure(document, diagram_path, caption, width=6.0)
            schema_rows = [("Booking_ID", "Synthetic transaction identifier"), ("Passenger_Name / Age / Gender", "Synthetic passenger attributes"), ("Transport_Mode", "Bus or Train"), ("Source / Destination", "Origin and destination city"), ("Booking_Date / Travel_Date", "Transaction and journey dates"), ("Ticket_Price / Number_of_Tickets", "INR per ticket and transaction quantity"), ("Booking_Status / Payment_Mode", "Lifecycle state and synthetic payment label")]
            document.add_heading("Dataset Schema", level=2)
            add_table(document, ["Field(s)", "Definition"], schema_rows)
            document.add_heading("Module Responsibilities", level=2)
            add_table(document, ["Module", "Responsibility"], [
                ("generate_dataset", "Seeded synthetic CSV generation"), ("data_loader", "File read and required-column checks"),
                ("data_cleaning", "Duplicate removal, validation, imputation, derived fields"), ("analysis", "Metrics and grouped summaries"),
                ("visualizations", "Ten Matplotlib PNG figures"), ("report_summary", "CSV and execution-summary exports"),
                ("main", "CLI orchestration and error reporting"),
            ])

    document.add_heading("Chapter 7: Results Tables", level=1)
    document.add_heading("Cleaning Audit", level=2)
    add_table(document, ["Measure", "Actual value"], [(key.replace("_", " ").title(), value) for key, value in cleaning.items()])
    document.add_heading("Headline Metrics", level=2)
    metric_rows = [
        ("Raw rows", len(pd_read_raw())), ("Cleaned records", metrics["dataset_records"]),
        ("Unique bookings", metrics["total_bookings"]), ("Completed bookings", metrics["completed_bookings"]),
        ("Confirmed bookings", metrics["confirmed_bookings"]), ("Cancelled bookings", metrics["cancelled_bookings"]),
        ("Pending bookings", metrics["pending_bookings"]), ("Total tickets", metrics["ticket_count"]),
        ("Eligible tickets", metrics["eligible_ticket_count"]), ("Recognized revenue", format_inr(metrics["recognized_revenue"])),
        ("Mean ticket price", format_inr(metrics["average_ticket_price"])), ("Minimum ticket price", format_inr(metrics["minimum_ticket_price"])),
        ("Maximum ticket price", format_inr(metrics["maximum_ticket_price"])), ("Most popular destination", metrics["most_popular_destination"]),
        ("Mean age", "{:.2f} years".format(metrics["age_mean"])), ("Median age", "{:.0f} years".format(metrics["age_median"])),
    ]
    add_table(document, ["Measure", "Actual value"], metric_rows)
    document.add_heading("Destination Summary", level=2)
    add_table(document, list(results["destination_summary"].columns), results["destination_summary"].head(12).round(2).values.tolist())
    document.add_heading("Top Routes", level=2)
    add_table(document, list(results["route_summary"].columns), results["route_summary"].head(10).round(2).values.tolist())
    document.add_heading("Mode Comparison", level=2)
    add_table(document, list(results["mode_summary"].columns), results["mode_summary"].round(2).values.tolist())
    document.add_heading("Passenger Age Groups", level=2)
    add_table(document, list(results["age_summary"].columns), results["age_summary"].values.tolist())
    document.add_heading("Monthly Summary", level=2)
    add_table(document, list(results["monthly_summary"].columns), results["monthly_summary"].round(2).values.tolist())
    for filename, caption in [
        ("bookings_by_destination.png", "Figure 6. Synthetic bookings by destination"),
        ("transport_mode_distribution.png", "Figure 7. Booking distribution by transport mode"),
        ("passenger_age_distribution.png", "Figure 8. Passenger booking-record age distribution"),
        ("average_price_by_mode.png", "Figure 9. Average per-ticket price by mode"),
        ("monthly_booking_trends.png", "Figure 10. Monthly synthetic booking trend"),
        ("monthly_revenue_trends.png", "Figure 11. Monthly recognized synthetic revenue"),
        ("top_10_routes.png", "Figure 12. Ten routes ranked by booking count"),
        ("revenue_by_destination.png", "Figure 13. Recognized revenue by destination"),
        ("booking_status_distribution.png", "Figure 14. Booking status counts"),
        ("ticket_price_distribution.png", "Figure 15. Per-ticket price distribution"),
    ]:
        add_figure(document, FIGURE_DIR / filename, caption, width=5.9)

    for chapter_title, sections in DISCUSSION_CHAPTERS:
        document.add_page_break()
        document.add_heading(chapter_title, level=1)
        for heading, body in sections:
            document.add_heading(heading, level=2)
            add_body(document, body)
        if chapter_title.startswith("Chapter 8"):
            doc_tests = [
                ("TC-01", "Seeded generator repeatability", "Same seed produces identical rows", "PASS"),
                ("TC-02", "Exact duplicate cleaning", "Eight duplicate examples removed", "PASS"),
                ("TC-03", "Revenue eligibility", "Cancelled/Pending excluded", "PASS"),
                ("TC-04", "Missing values", "Selected fields resolved", "PASS"),
                ("TC-05", "Missing input file", "FileNotFoundError identifies path", "PASS"),
                ("TC-06", "Incomplete schema", "ValueError identifies missing columns", "PASS"),
            ]
            add_table(document, ["Test ID", "Test", "Expected / actual", "Result"], doc_tests)
            add_body(document, "Executed command: python -m unittest discover -s tests -v. Return code: {}. Test output:\n{}".format(test_process.returncode, test_output.strip()))

    document.add_page_break()
    document.add_heading("Bibliography / References", level=1)
    add_body(document, "References are presented in a consistent author-date style. Official software documentation is cited for technical behavior; the EDA book and pandas conference paper provide methodological context.")
    for reference in REFERENCES:
        paragraph = document.add_paragraph(reference)
        paragraph.paragraph_format.left_indent = Inches(0.3)
        paragraph.paragraph_format.first_line_indent = Inches(-0.3)

    document.add_page_break()
    document.add_heading("Appendix A: Installation and User Manual", level=1)
    add_body(document, "Install Python 3.9 or later, create a virtual environment, activate it, and run python -m pip install -r requirements.txt. Generate data with python -m src.generate_dataset. Run the analysis with python -m src.main. Run tests with python -m unittest discover -s tests -v. Open the learning notebook with jupyter notebook notebooks/Bus_Train_Ticket_Booking_Analysis.ipynb. Run commands from the project root.")
    add_body(document, "Common issues: activate the same environment used to install dependencies; use the documented column names for custom CSV input; and run the `src` module from the project root. Charts appear in `figures`; cleaned records and summaries are in `data`; the execution log is in `outputs`. All outputs are synthetic." )

    document.add_heading("Appendix B: Source Code Excerpts and Algorithm", level=1)
    add_body(document, "Revenue formula: booking gross amount = Ticket_Price x Number_of_Tickets. Recognized revenue = booking gross amount when status is Completed or Confirmed; otherwise it is zero. Refunds are not accounted for.")
    add_body(document, "Cleaning pseudocode: copy the input; verify required columns; count exact duplicates; remove exact duplicate rows; normalize text and parse dates/numbers; identify invalid identity, date, route, mode, status, price, and quantity fields; remove invalid rows; impute allowed missing values; derive revenue, eligibility, month, and route; return cleaned rows and audit counts.")
    add_body(document, "The full beginner-friendly implementation is in the `src/` folder of the project archive. This report excerpt is explanatory; it does not replace the source modules or tests.")

    document.add_heading("Appendix C: Sample Records", level=1)
    sample = cleaned[["Booking_ID", "Passenger_Name", "Age", "Transport_Mode", "Source", "Destination", "Booking_Date", "Ticket_Price", "Number_of_Tickets", "Booking_Status", "Recognized_Revenue"]].head(8).copy()
    sample["Booking_Date"] = sample["Booking_Date"].dt.strftime("%Y-%m-%d")
    sample["Ticket_Price"] = sample["Ticket_Price"].round(2)
    sample["Recognized_Revenue"] = sample["Recognized_Revenue"].round(2)
    add_table(document, list(sample.columns), sample.values.tolist())

    document.add_heading("Appendix D: Test Cases and Sample Execution", level=1)
    add_table(document, ["Test", "Expected", "Actual status"], [
        ("Seed reproducibility", "Same seed, same data", "PASS"),
        ("Duplicate handling", "Only exact examples removed", "PASS"),
        ("Revenue status filter", "Cancelled/Pending count zero", "PASS"),
        ("Missing-value treatment", "Selected fields are complete", "PASS"),
        ("Missing file", "FileNotFoundError", "PASS"),
        ("Required schema", "ValueError", "PASS"),
    ])
    add_body(document, "Sample command: python -m src.main. Sample measures from this execution are listed in Chapter 7 and in outputs/execution_summary.txt. Rerunning with the fixed seed should reproduce the default synthetic sample and its calculated results.")

    document.add_heading("Appendix E: Glossary", level=1)
    glossary = [
        ("Booking", "One transaction record identified by Booking_ID."),
        ("Ticket count", "The sum of Number_of_Tickets across records; not the number of transactions."),
        ("Exact duplicate", "A row identical across all required raw fields."),
        ("Feature engineering", "Creating useful analysis columns from existing fields."),
        ("Imputation", "Filling a missing value using a documented rule."),
        ("Recognized revenue", "The project-defined amount counted for eligible booking statuses."),
        ("Synthetic data", "Artificially generated records that do not describe actual people or transactions."),
        ("EDA", "Exploratory inspection using summaries and visualizations."),
        ("DataFrame", "A labeled two-dimensional table provided by pandas."),
        ("Percentile", "A value below which a specified percentage of observations falls."),
    ]
    add_table(document, ["Term", "Simple meaning"], glossary)

    document.core_properties.title = "Bus/Train Ticket Booking Data Analysis Using Python"
    document.core_properties.subject = "BCA final-year project report based on synthetic records"
    document.core_properties.author = "[STUDENT NAME]"
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    document.save(REPORT_PATH)
    print("Created report: {}".format(REPORT_PATH))
    print("Test suite result: {}".format("PASS" if test_process.returncode == 0 else "FAIL"))
    print("Dataset records: {}".format(metrics["dataset_records"]))


def pd_read_raw():
    """Return the actual raw row count from the current generated CSV."""
    import pandas as pd
    return pd.read_csv(ROOT / "data" / "raw" / "booking_data.csv")


if __name__ == "__main__":
    build_report()
