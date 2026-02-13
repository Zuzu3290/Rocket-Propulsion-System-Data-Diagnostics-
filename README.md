# 🚀 Rocket Propulsion System Analysis & Dashboard

This repository contains a complete **data analysis and visualization pipeline** for rocket propulsion systems, combining statistical analysis, regression modeling, and interactive dashboard construction.

The project focuses on understanding relationships between **combustion temperature, thrust, stability, and specific impulse**, while also providing **high-level system composition insights** through sunburst visualizations.

The repository is organized as follows:

---

## 📁 Repository Structure

- **`Propulsion_System.ipynb`**: This is the **main data science diagnostics script** that performs in-depth analysis of the rocket propulsion system. It investigates key relationships between various performance metrics like combustion temperature, thrust, and specific impulse, laying the groundwork for further analysis.

- **`Dashboard.ipynb`**: This notebook presents the **main result of the diagnostic analysis**. It generates interactive visualizations and insights into the propulsion system, enabling users to explore key relationships and understand the system’s performance visually.

- **`app.py`**: This Python script is used for **Dashbaord visualization**. It launches a web-based dashboard for a more interactive and user-friendly presentation of the data analysis, suitable for real-time exploration and diagnosis.

- **`Linear Regression.ipynb`**: This notebook focuses on **progress in building an optimal model** capable of diagnosing combustion system stability during runtime. Using linear regression techniques, it helps predict performance metrics and analyze system behavior under various conditions.

---

## 📊 Data Files

The project uses two primary statistical datasets representing different ambient pressure environments.  
Both datasets share the **same schema**, enabling direct comparison between vacuum and ground conditions.
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
### `Ground_Statistics.csv`

Performance statistics collected under **sea-level operating conditions**.

**Usage**
- Selected when ambient pressure = **1.01325 bar**

**Contents**
- Identical column structure to `Vacuum_Statistics.csv`
- Enables one-to-one comparison between ground and vacuum performance

This dataset is primarily used to analyze **launch and lower-atmosphere propulsion behavior**.
### Key Analyses:

* Combustion Temperature vs Specific Impulse: This analysis explores the relationship between the combustion temperature and specific impulse across different pressure conditions.

* Stability vs Performance Metrics: Investigates how stability margins affect the overall performance and reliability of the propulsion system.

* System Composition: Uses sunburst charts to give high-level insights into the components of the propulsion system and how they relate to overall performance.
---

### 📉 Linear Regression Modeling
Currently, the project focuses on developing and refining a linear regression model to understand key performance metrics of rocket propulsion systems. The model is built using data from both Vacuum_Statistics.csv and Ground_Statistics.csv.

The primary goals of the regression model:
1) Prediction of Combustion Stability Margin based on combustion temperature and other thermodynamic properties.
2) Analysis of performance trends across different environments (vacuum vs ground).
3) Diagnostic tool: Dashbaord for identifying key factors influencing rocket propulsion efficiency and stability.
---
### ⚙️ Running the Application
To get started with the interactive dashboard, follow these steps:
1. Install [Python](https://www.python.org/downloads/)
2. Clone the Repository
```bash
git clone https://github.com/Zuzu3290/Rocket-Propulsion-System-Data-Diagnostics-.git
```
3.Run the Application
```Terminal
python app.py
```
### 📈 Visualizations
The dashboard generates interactive visualizations, including:
* Sunburst Charts: For understanding the system composition.
* Regression Plots: For analyzing the relationships between combustion parameters and propulsion performance.
* Time-Series Plots: To visualize performance trends over different operating conditions.
