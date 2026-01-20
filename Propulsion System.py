import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.express as px


# ------------------------------------------------------------
# HARD-CODED PATHS (your paths)
# ------------------------------------------------------------
PROP_PATH   = r"C:\Users\zuhai\Desktop\Projects\Data Science Project\ propulsion system data\rocket_propulsion_dataset_v1.csv"
VAC_PATH    = r"C:\Users\zuhai\Desktop\Projects\Data Science Project\Vacum_Statistics.csv"
GROUND_PATH = r"C:\Users\zuhai\Desktop\Projects\Data Science Project\Ground_Statistics.csv"

SUN1_PNG = r"C:\Users\zuhai\Desktop\Projects\Data Science Project\sunburst1.png"
SUN2_PNG = r"C:\Users\zuhai\Desktop\Projects\Data Science Project\sunburst2.png"
OUT_PNG  = r"C:\Users\zuhai\Desktop\Projects\Data Science Project\propulsion_dashboard.png"


# ------------------------------------------------------------
# 1) Ambient pressure selection (ONLY 0.01 or 1.01325)
# ------------------------------------------------------------
pressure = float(input("Enter ambient pressure (0.01 or 1.01325): ").strip())
tol = 1e-6

if abs(pressure - 0.01) <= tol:
    data = pd.read_csv(VAC_PATH)
    pressure_type = "Vacuum"
elif abs(pressure - 1.01325) <= tol:
    data = pd.read_csv(GROUND_PATH)
    pressure_type = "Ground"
else:
    raise ValueError("Invalid input. Only 0.01 or 1.01325 are accepted.")

print(f"Selected ambient pressure: {pressure} bar ({pressure_type})")


# ------------------------------------------------------------
# 2) Load propulsion system data + fuel_class mapping (as in your notebook)
# ------------------------------------------------------------
fuel_classes = {
    "LH2": "Cryogenic fuel",
    "CH4": "Cryogenic fuel",
    "Ethane": "Cryogenic fuel",
    "NH3": "Cryogenic fuel",

    "RP1": "Storable hydrocarbon",
    "JP10": "Storable hydrocarbon",
    "Syntin": "Storable hydrocarbon",
    "Ethanol": "Storable hydrocarbon",
    "Methanol": "Storable hydrocarbon",
    "Paraffin": "Storable hydrocarbon",
    "Aniline": "Storable hydrocarbon",

    "UDMH": "Storable hypergolic fuels",
    "MMH": "Storable hypergolic fuels",
    "Hydrazine": "Storable hypergolic fuels",
    "Hydrazine_M": "Storable hypergolic fuels",
    "Aerozine50": "Storable hypergolic fuels",
    "UH25": "Storable hypergolic fuels",
    "Tonka250": "Storable hypergolic fuels",

    "H2O2_98": "Monopropellants",
    "LMP103S": "Monopropellants",

    "PBAN": "Solid fuels",
    "HTPB_Hybrid": "Solid fuels",
    "DB_Solid": "Solid fuels",

    "APCP": "Solid composite",
}

prop = pd.read_csv(PROP_PATH)
prop["fuel_class"] = prop["fuel_type"].map(fuel_classes).fillna("Other/Unknown")


# ------------------------------------------------------------
# 3) Create the two sunbursts (Plotly) and export as PNGs
#    - This is the piece your notebook does with make_subplots,
#      but we export them as images for Matplotlib.
# ------------------------------------------------------------
# Sunburst #1: (your notebook intent) Oxidizer Type → Fuel Type
# NOTE: your cell uses path=["fuel_class","oxidizer_type"] in one place;
#       but your titles say Oxidizer→Fuel. Adjust if you truly want different.
sun1 = px.sunburst(prop, path=["oxidizer_type", "fuel_type"])
sun1.update_layout(margin=dict(t=10, l=10, r=10, b=10), uniformtext=dict(minsize=10, mode="hide"))
sun1.write_image(SUN1_PNG, scale=2)

# Sunburst #2: Fuel Class → Fuel Type (matches your notebook)
sun2 = px.sunburst(prop, path=["fuel_class", "fuel_type"])
sun2.update_layout(margin=dict(t=10, l=10, r=10, b=10), uniformtext=dict(minsize=10, mode="hide"))
sun2.write_image(SUN2_PNG, scale=2)


# ------------------------------------------------------------
# 4) 4×4 matrix plot (Matplotlib) — choose 4 columns from your stats data
#    If you want specific 4 columns, set them here explicitly.
# ------------------------------------------------------------
preferred = [
    "combustion_temperature_K",
    "specific_impulse_s",
    "thrust_volume",
    "chamber_pressure_Pa",
    "mixture_ratio",
    "expansion_ratio",
]
numeric_cols = [c for c in preferred if c in data.columns and pd.api.types.is_numeric_dtype(data[c])]
if len(numeric_cols) < 4:
    numeric_cols = list(data.select_dtypes(include=[np.number]).columns)

if len(numeric_cols) < 4:
    raise ValueError("Not enough numeric columns in stats dataset to build a 4×4 matrix.")

matrix_cols = numeric_cols[:4]
df_m = data.dropna(subset=matrix_cols).copy()


# ------------------------------------------------------------
# 5) Temperature histogram + cumulative mean Isp (Matplotlib)
#    This matches your notebook logic:
#       df_sorted = data.sort_values("combustion_temperature_K")
#       cum_mean_isp = ... expanding().mean()
# ------------------------------------------------------------
needed = ["combustion_temperature_K", "specific_impulse_s"]
for c in needed:
    if c not in data.columns:
        raise KeyError(f"Stats dataset missing required column: {c}")

df_sorted = data.dropna(subset=needed).sort_values("combustion_temperature_K")
cum_mean_isp = df_sorted["specific_impulse_s"].expanding().mean()


# ------------------------------------------------------------
# 6) Compose final dashboard in Matplotlib and save ONE PNG
#    Layout:
#      Top (2/3 height): 4×4 matrix
#      Bottom row: Sunburst1 | Sunburst2 | Temp histogram + cum mean Isp
# ------------------------------------------------------------
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(nrows=3, ncols=3, height_ratios=[1.1, 1.1, 1.0], hspace=0.35, wspace=0.25)

# --- Top: 4×4 scatter-matrix spanning rows 0-1, cols 0-2 (as a sub-gridspec)
sg = gs[0:2, 0:3].subgridspec(4, 4, wspace=0.08, hspace=0.08)

for i, ycol in enumerate(matrix_cols):
    for j, xcol in enumerate(matrix_cols):
        ax = fig.add_subplot(sg[i, j])
        if i == j:
            ax.hist(df_m[xcol].values, bins=20)
        else:
            ax.scatter(df_m[xcol].values, df_m[ycol].values, s=6, alpha=0.6)

        # label only outer edges (clean like a matrix)
        if i < 3:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel(xcol, fontsize=9, rotation=15)

        if j > 0:
            ax.set_yticklabels([])
        else:
            ax.set_ylabel(ycol, fontsize=9)

# --- Bottom row panels
ax_sun1 = fig.add_subplot(gs[2, 0])
ax_sun2 = fig.add_subplot(gs[2, 1])
ax_temp = fig.add_subplot(gs[2, 2])

# Load exported sunbursts
img1 = plt.imread(SUN1_PNG)
img2 = plt.imread(SUN2_PNG)

ax_sun1.imshow(img1)
ax_sun1.axis("off")
ax_sun1.set_title("Oxidizer Type → Fuel Type", fontsize=11)

ax_sun2.imshow(img2)
ax_sun2.axis("off")
ax_sun2.set_title("Fuel Class → Fuel Type", fontsize=11)

# Temperature histogram + cumulative mean Isp with twin y-axis
ax_temp.hist(df_sorted["combustion_temperature_K"].values, bins=30, alpha=0.55)
ax_temp.set_xlabel("Combustion Temperature (K)")
ax_temp.set_ylabel("Count")
ax_temp.set_title("Temperature Histogram + Cumulative Mean Isp", fontsize=11)

ax2 = ax_temp.twinx()
ax2.plot(df_sorted["combustion_temperature_K"].values, cum_mean_isp.values, linewidth=2)
ax2.set_ylabel("Cumulative Mean Specific Impulse (s)")

# Figure title
fig.suptitle(f"Propulsion Overview — {pressure_type} (P={pressure} bar)", fontsize=18, y=0.98)

# Save final dashboard PNG
fig.savefig(OUT_PNG, dpi=220, bbox_inches="tight")
plt.show()

print(f"\nSaved dashboard PNG to:\n{OUT_PNG}\n")
