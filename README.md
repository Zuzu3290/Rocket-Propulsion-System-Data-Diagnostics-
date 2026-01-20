🚀 Rocket Propulsion System Analysis & Dashboard

This repository contains a complete data analysis and visualization pipeline for rocket propulsion systems, combining statistical analysis, regression modeling, and interactive dashboard construction.

The project focuses on understanding relationships between combustion temperature, thrust, stability, and specific impulse, while also providing high-level system composition insights through sunburst visualizations.

📁 Repository Structure
├── Dashboard.ipynb
├── Propulsion_System.ipynb
├── Propulsion System.py
├── Linear Regression.ipynb
├── Vacuum_Statistics.csv
├── Ground_Statistics.csv
├── propulsion_dashboard.png
├── sunburst1.png
├── sunburst2.png
└── README.md

📊 Data Files
Vacuum_Statistics.csv

Performance statistics under near-vacuum conditions

Used when ambient pressure = 0.01 bar

Includes:

Combustion temperature

Thrust volume

Specific impulse

Stability margins

Thermochemical and pressure indices

Ground_Statistics.csv

Performance statistics under sea-level conditions

Used when ambient pressure = 1.01325 bar

Same schema as the vacuum dataset for consistency

📈 Notebooks
Dashboard.ipynb

Primary development notebook for the dashboard logic

Includes:

Interactive dashboard construction

Multi-panel subplot design

Trend analysis (rolling means, cumulative means)

Histogram + secondary axis plots

Sunburst visualization logic

This notebook is the source of truth for the dashboard design.

Propulsion_System.ipynb

Exploratory analysis notebook focusing on:

Data cleaning

Feature relationships

Preliminary visualization experiments

Fuel type and fuel class grouping logic

Linear Regression.ipynb

Contains:

Regression modeling

Trend fitting (e.g., thrust vs temperature, stability vs indices)

Model interpretation and diagnostics

🧠 Python Script
Propulsion System.py

Production-ready script version of the dashboard

Features:

Hard-coded file paths for reproducibility

Explicit ambient pressure selection:

0.01 → Vacuum statistics

1.01325 → Ground statistics

Automated generation of:

Overview dashboard

Fuel-class–based analytical dashboards

PNG export using Plotly + Kaleido

This script is intended for non-notebook execution.

📊 Generated Outputs
propulsion_dashboard.png

Final exported dashboard

Includes:

System-level sunbursts

Temperature histogram

Cumulative mean specific impulse

sunburst1.png

Fuel Class → Oxidizer Type distribution

sunburst2.png

Fuel Class → Fuel Type distribution

These images are generated automatically during dashboard construction and can be reused in reports or presentations.

🧩 Dashboard Design Overview
1️⃣ Overview Dashboard

Fuel Class → Oxidizer Type (Sunburst)

Fuel Class → Fuel Type (Sunburst)

Combustion Temperature Histogram

Cumulative Mean Specific Impulse (secondary axis)

2️⃣ Fuel-Class Analytical Dashboards

For each fuel_class, a 2×2 dashboard is generated:

Thrust vs Combustion Temperature

Stability vs Pressure–Isp–Gamma Index (trend line)

Cumulative Mean Stability vs Thrust

Rolling Mean Stability vs Thermochemical Index

This replaces dropdown-based filtering with systematic class-level analysis.

⚙️ How to Run
Requirements
pip install pandas numpy plotly kaleido matplotlib

Run the Script
python "Propulsion System.py"


When prompted:

Enter 0.01 for vacuum conditions

Enter 1.01325 for ground conditions

Generated PNGs will be saved automatically.

🧪 Design Philosophy

Traceable: Every dashboard element is grounded in the original notebook logic.

Deterministic: No UI widgets or hidden state.

Extensible: Easy to add new fuel classes, indices, or regression models.

Publication-ready: All dashboards export cleanly to PNG.

📌 Notes

Plotly is used for hierarchical and interactive visuals

Matplotlib is used where static composition or post-processing is required

All visual logic is centralized and reusable

📄 License

This project is provided for academic and research use.
Feel free to adapt and extend with attribution.
