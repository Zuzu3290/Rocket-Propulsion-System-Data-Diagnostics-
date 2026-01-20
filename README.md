# 🚀 Rocket Propulsion System Analysis & Dashboard

This repository contains a complete **data analysis and visualization pipeline** for rocket propulsion systems, combining statistical analysis, regression modeling, and interactive dashboard construction.

The project focuses on understanding relationships between **combustion temperature, thrust, stability, and specific impulse**, while also providing **high-level system composition insights** through sunburst visualizations.

---

## 📁 Repository Structure

```text
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

## 📊 Data Files

The project uses two primary statistical datasets representing different ambient pressure environments.  
Both datasets share the **same schema**, enabling direct comparison between vacuum and ground conditions.

---

### `Vacuum_Statistics.csv`

Performance statistics collected under **near-vacuum operating conditions**.

**Usage**
- Selected when ambient pressure = **0.01 bar**

**Contents**
- Combustion temperature (`combustion_temperature_K`)
- Thrust volume (`thrust_volume`)
- Specific impulse (`specific_impulse_s`)
- Combustion stability margin (`combustion_stability_margin`)
- Thermochemical power index (`thermochemical_power_index`)
- Pressure–Isp–Gamma index (`pressure_isp_gamma_index`)
- Additional derived thermodynamic and performance metrics

This dataset is primarily used to analyze **upper-stage and in-space propulsion behavior**.

---

### `Ground_Statistics.csv`

Performance statistics collected under **sea-level operating conditions**.

**Usage**
- Selected when ambient pressure = **1.01325 bar**

**Contents**
- Identical column structure to `Vacuum_Statistics.csv`
- Enables one-to-one comparison between ground and vacuum performance

This dataset is primarily used to analyze **launch and lower-atmosphere propulsion behavior**.

---

### Notes on Data Consistency

- Both datasets:
  - Use the same units and column naming conventions
  - Are interchangeable within the dashboard pipeline
  - Support cumulative, rolling, and regression-based analyses

- Dataset selection is handled programmatically based on **user-specified ambient pressure**, ensuring deterministic and reproducible results.
