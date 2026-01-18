#Inclusion of all necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 
#Data COllection
df = pd.read_csv(" propulsion system data/rocket_propulsion_dataset_v1.csv")
df = df[df.physics_violation_flag == 0] 

#Exploration and Visualization
df['fuel_oxidizer'] = df['fuel_type'] 

# 2. Pivot for Ambient Pressure
pivot_ambient = df.groupby('fuel_type')['ambient_pressure_bar'].mean().to_frame()

# 3. Pivot for Stability Margin
pivot_stability = df.groupby('fuel_type')['combustion_stability_margin'].mean().to_frame()

# 4. Sort fuel_oxidizer by mean stability descending
sorted_index = pivot_stability.sort_values(by='combustion_stability_margin', ascending=False).index
pivot_ambient = pivot_ambient.loc[sorted_index]
pivot_stability = pivot_stability.loc[sorted_index]

# 5. Plots
fig, axes = plt.subplots(1, 2, figsize=(14, max(6, len(sorted_index)/2)))
sns.heatmap(
    pivot_ambient,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    cbar_kws={'label':'Mean Ambient Pressure'},
    ax=axes[0]
)
axes[0].set_title('Ambient Pressure by Fuel ')
axes[0].set_xlabel('')
axes[0].set_ylabel('Fuel')

sns.heatmap(
    pivot_stability,
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    cbar_kws={'label':'Mean Stability Margin'},
    ax=axes[1]
)
axes[1].set_title('Combustion Stability Margin by Fuel')
axes[1].set_xlabel('')
axes[1].set_ylabel('')

plt.tight_layout()
plt.show()


df['fuel_oxidizer'] = df['fuel_type'] + " | " + df['oxidizer_type']

# 2. Pivot for Ambient Pressure
pivot_ambient = df.groupby('fuel_oxidizer')['ambient_pressure_bar'].mean().to_frame()

# 3. Pivot for Stability Margin
pivot_stability = df.groupby('fuel_oxidizer')['combustion_stability_margin'].mean().to_frame()

# 4. Sort fuel_oxidizer by mean stability descending
sorted_index = pivot_stability.sort_values(by='combustion_stability_margin', ascending=False).index
pivot_ambient = pivot_ambient.loc[sorted_index]
pivot_stability = pivot_stability.loc[sorted_index]

# 5. Plotting
fig, axes = plt.subplots(1, 2, figsize=(14, max(6, len(sorted_index)/2)))

# Heatmap 1: Ambient Pressure
sns.heatmap(
    pivot_ambient,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    cbar_kws={'label':'Mean Ambient Pressure'},
    ax=axes[0]
)
axes[0].set_title('Ambient Pressure by Fuel + Oxidizer')
axes[0].set_xlabel('')
axes[0].set_ylabel('Fuel | Oxidizer')

# Heatmap 2: Combustion Stability
sns.heatmap(
    pivot_stability,
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    cbar_kws={'label':'Mean Stability Margin'},
    ax=axes[1]
)
axes[1].set_title('Combustion Stability Margin by Fuel + Oxidizer')
axes[1].set_xlabel('')
axes[1].set_ylabel('')

plt.tight_layout()

fuel_classes = {
    "LH2": "Cryogenic fuel", #High performance, source petroluem deposits plus organic wastes
    "CH4": "Cryogenic fuel",
    "Ethane": "Cryogenic fuel",
    "NH3": "Cryogenic fuel",

    "RP1": "Storable hydrocarbon", #Liquid at ambient conditions
    "JP10": "Storable hydrocarbon",
    "Syntin": "Storable hydrocarbon",
    "Ethanol": "Storable hydrocarbon",
    "Methanol": "Storable hydrocarbon",
    "Paraffin": "Storable hydrocarbon",
    "Aniline": "Storable hydrocarbon",

    "UDMH": "Storable hypergolic fuels", # Ignite on contact with NTO
    "MMH": "Storable hypergolic fuels",
    "Hydrazine": "Storable hypergolic fuels",
    "Hydrazine_M": "Storable hypergolic fuels",
    "Aerozine50": "Storable hypergolic fuels",
    "UH25": "Storable hypergolic fuels",
    "Tonka250": "Storable hypergolic fuels",

    "H2O2_98": "Monopropellants",
    "LMP103S": "Monopropellants",

    "PBAN": "Solid fuels", #decompose without external oxidizer
    "HTPB_Hybrid": "Solid fuels",
    "DB_Solid": "Solid fuels",
    
    "APCP": "Solid composite"  #Fuel + oxidizer in one grain
}
#https://headedforspace.com/what-fuels-do-rockets-use/
#https://spacecraftandvehicles.com/articles/types-of-rocket-fuel/
# RP1 - HIghly Reformed Kerosene 
# Apply mapping directly to the 'fuel_type' column
df["fuel_type"] = df["fuel_type"].map(fuel_classes)

df['ambient_pressure_bar'].value_counts()
# 0.01 --> vacuum testing.
# 1.01325 --> standard atmospheric pressure for ground-level tests
cols_of_interest = [
    "combustion_stability_margin",
    "chamber_pressure_bar",
    "oxidizer_fuel_ratio",
    "combustion_temperature_K",
    "heat_capacity_ratio",
    "nozzle_expansion_ratio",
    "ambient_pressure_bar",
    "specific_impulse_s"
]
# Compute correlation matrix
corr_matrix = df[cols_of_interest].corr()
# Plot heatmap
plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix,annot=True,fmt=".2f",cmap='coolwarm',center=0)
plt.title('Correlation Heatmap of Numerical Parameters (Excluding Last Column)')
plt.show()

df['fuel_type'] = df['fuel_type'].astype(str).str.strip()
df['oxidizer_type'] = df['oxidizer_type'].astype(str).str.strip()

# 1️⃣ Oxidizer Type vs Sum of O/F Ratio
oxidizers = ['LOX', 'NTO', 'catalyst', 'Internal_AP']
y_oxidizer = []

for ox in oxidizers:
    subset = df[df['oxidizer_type'] == ox]
    y_oxidizer.append(subset['oxidizer_fuel_ratio'].sum())

plt.figure(figsize=(8, 5))
plt.bar(oxidizers, y_oxidizer, color=['blue', 'red', 'green', 'orange'])
plt.xlabel('Oxidizer Type')
plt.ylabel('Sum of O/F Ratio')
plt.title('Sum of O/F Ratio by Oxidizer Type')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# 2️⃣ Fuel Type vs Sum of O/F Ratio
fuels = df['fuel_type'].unique()
y_fuel = []

for f in fuels:
    subset = df[df['fuel_type'] == f]
    y_fuel.append(subset['oxidizer_fuel_ratio'].sum())

plt.figure(figsize=(12, 6))
plt.bar(fuels, y_fuel, color='skyblue')
plt.xlabel('Fuel Type')
plt.ylabel('Sum of O/F Ratio')
plt.title('Sum of O/F Ratio by Fuel Type')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

x_mech = df['chamber_pressure_bar']
y_mech = df['combustion_stability_margin']

# Fit a simple linear trend line using np.polyfit
coeffs_mech = np.polyfit(x_mech, y_mech, 1)  # degree 1 → straight line
y_fit_mech = np.polyval(coeffs_mech, x_mech)

plt.figure(figsize=(10, 6))
plt.scatter(x_mech, y_mech, color='skyblue', edgecolor='k', alpha=0.7, label='Data')
plt.plot(x_mech, y_fit_mech, color='red', linewidth=2, label='Trend Line')
plt.xlabel('Chamber Pressure (bar)')
plt.ylabel('Combustion Stability Margin')
plt.title('Mechanical Performance Proxy')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


x_chem = df['specific_impulse_s']
y_chem = df['heat_capacity_ratio']

# Fit a simple linear trend line
coeffs_chem = np.polyfit(x_chem, y_chem, 1)
y_fit_chem = np.polyval(coeffs_chem, x_chem)

plt.figure(figsize=(10, 6))
plt.scatter(x_chem, y_chem, color='salmon', edgecolor='k', alpha=0.7, label='Data')
plt.plot(x_chem, y_fit_chem, color='blue', linewidth=2, label='Trend Line')
plt.xlabel('Specific Impulse (s)')
plt.ylabel('Heat Capacity Ratio (γ)')
plt.title('Chemical / Thermodynamic Contribution')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
plt.show()
