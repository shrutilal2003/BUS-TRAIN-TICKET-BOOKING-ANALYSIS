# System Architecture and Diagrams

All diagrams are editable Mermaid source. The Python application is a local batch-analysis tool; no network service or booking/payment system is implemented.

## Architecture

```mermaid
flowchart LR
    A[Seeded synthetic generator] --> B[Raw CSV]
    B --> C[Schema validation and loader]
    C --> D[Cleaning and feature engineering]
    D --> E[Analysis: pandas and NumPy]
    E --> F[Summary CSV exports]
    E --> G[Matplotlib PNG figures]
    D --> H[Cleaned CSV]
    E --> I[Text execution summary]
    E --> J[Jupyter notebook and thesis]
```

## Project Workflow

```mermaid
flowchart TD
    A[Start] --> B{Raw CSV exists?}
    B -- No --> C[Generate seeded synthetic records]
    B -- Yes --> D[Load CSV and validate schema]
    C --> D
    D --> E[Remove exact duplicate rows]
    E --> F[Convert types, validate, impute missing fields]
    F --> G[Derive month, route, and revenue]
    G --> H[Calculate metrics and grouped summaries]
    H --> I[Export CSVs and execution summary]
    H --> J[Save ten charts]
    I --> K[Finish]
    J --> K
```

## Data Flow Diagram (Level 0)

```mermaid
flowchart LR
    Student[Student / analyst] -->|Run options and synthetic CSV| System[Booking analysis system]
    System -->|Cleaned records, metrics, charts| Student
    System -->|Read| Raw[(Raw CSV)]
    System -->|Write| Results[(Processed CSV and summaries)]
```

## Data Flow Diagram (Level 1)

```mermaid
flowchart LR
    D1[(Raw booking CSV)] --> P1[1. Load and validate]
    P1 --> P2[2. Clean and engineer features]
    P2 --> D2[(Cleaned booking CSV)]
    P2 --> P3[3. Aggregate and calculate statistics]
    P3 --> D3[(Summary CSV files)]
    P3 --> P4[4. Plot and summarize]
    P4 --> D4[(PNG charts and execution summary)]
```

## Use Cases

```mermaid
flowchart LR
    Analyst((Student analyst)) --> U1[Generate synthetic dataset]
    Analyst --> U2[Run cleaning and validation]
    Analyst --> U3[Analyze passengers, routes, prices, and revenue]
    Analyst --> U4[Export CSV summaries and charts]
    Analyst --> U5[Open educational notebook]
```

## Activity Diagram

```mermaid
flowchart TD
    A([Begin]) --> B[Choose input or generate default]
    B --> C{Schema valid?}
    C -- No --> X[Show actionable error]
    C -- Yes --> D[Clean and validate records]
    D --> E[Calculate eligible revenue and grouped summaries]
    E --> F[Export cleaned data and result files]
    F --> G[Create visualizations]
    G --> H([Complete])
```