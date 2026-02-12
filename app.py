import os
import io
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

VACUUM_STATS = "Vacum_Statistics.csv"
GROUND_STATS = "Ground_Statistics.csv"
PROP_DATASET = " propulsion system data/rocket_propulsion_dataset_v1.csv"  # keep as you want


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

    "APCP": "Solid composite"
}


PROP = pd.read_csv(PROP_DATASET)
PROP["fuel_class"] = PROP["fuel_type"].map(fuel_classes)  # keep your preference (no fillna)

if "ambient_pressure_bar" in PROP.columns:
    PRESSURE_VALUES = sorted(pd.Series(PROP["ambient_pressure_bar"]).dropna().astype(float).unique().tolist())
else:
    PRESSURE_VALUES = [0.01, 1.01325]


def load_stats_for_pressure(pressure: float) -> tuple[pd.DataFrame, str]:
    # your original behavior: pressure chooses which stats file
    if np.isclose(pressure, 0.01, atol=1e-9):
        return pd.read_csv(VACUUM_STATS), "Vacuum"
    return pd.read_csv(GROUND_STATS), "Ground"


def filter_prop_for_pressure(pressure: float) -> pd.DataFrame:
    if "ambient_pressure_bar" not in PROP.columns:
        return PROP.copy()
    p = pd.Series(PROP["ambient_pressure_bar"]).astype(float).round(6)
    return PROP.loc[p.eq(round(float(pressure), 6))].copy()


def fig_2x2_all_fuels(data: pd.DataFrame, pressure: float, pressure_label: str) -> go.Figure:
    required = [
        "fuel_type",
        "combustion_temperature_K",
        "thrust_volume",
        "pressure_isp_gamma_index",
        "combustion_stability_margin",
        "thermochemical_power_index",
    ]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns in stats CSV: {missing}")

    fuels = sorted(data["fuel_type"].dropna().unique().tolist())

    fig = make_subplots(
        rows=2, cols=2,
        vertical_spacing=0.12, horizontal_spacing=0.10,
        subplot_titles=[
            "Thrust vs Combustion Temperature (by fuel)",
            "Stability vs Pressure Index (by fuel + global trend)",
            "Cumulative Mean Stability vs Thrust (by fuel)",
            "Rolling Mean Stability vs Thermochemical Index (by fuel)",
        ],
    )

    # (1,1) scatter per fuel
    for fuel in fuels:
        df = data.loc[data["fuel_type"] == fuel]
        fig.add_trace(
            go.Scattergl(
                x=df["combustion_temperature_K"],
                y=df["thrust_volume"],
                mode="markers",
                name=str(fuel),
                showlegend=True,
            ),
            row=1, col=1
        )
    fig.update_xaxes(title_text="Combustion Temperature (K)", row=1, col=1)
    fig.update_yaxes(title_text="Thrust Volume", row=1, col=1)

    # (1,2) per fuel scatter (legend kept), plus one global trendline
    x_all = []
    y_all = []
    for fuel in fuels:
        df = data.loc[data["fuel_type"] == fuel].copy()
        x = df["pressure_isp_gamma_index"].to_numpy()
        y = df["combustion_stability_margin"].to_numpy()
        m = np.isfinite(x) & np.isfinite(y)
        x = x[m]; y = y[m]
        x_all.append(x); y_all.append(y)
        fig.add_trace(
            go.Scattergl(
                x=x, y=y,
                mode="markers",
                name=str(fuel),
                showlegend=False,  # legend already in (1,1)
            ),
            row=1, col=2
        )

    x_all = np.concatenate(x_all) if len(x_all) else np.array([])
    y_all = np.concatenate(y_all) if len(y_all) else np.array([])

    if len(x_all) >= 2:
        order = np.argsort(x_all)
        xs = x_all[order]
        ys = y_all[order]
        c = np.polyfit(xs, ys, 1)
        y_fit = np.polyval(c, xs)
        fig.add_trace(
            go.Scatter(x=xs, y=y_fit, mode="lines", name="Global trend", showlegend=False),
            row=1, col=2
        )

    fig.update_xaxes(title_text="Pressure–Isp–Gamma Index", row=1, col=2)
    fig.update_yaxes(title_text="Combustion Stability Margin", row=1, col=2)

    # (2,1) cumulative mean stability vs thrust, per fuel (lines)
    for fuel in fuels:
        df = data.loc[data["fuel_type"] == fuel].sort_values("thrust_volume").copy()
        y = df["combustion_stability_margin"].to_numpy()
        x = df["thrust_volume"].to_numpy()
        # allow NaNs: expanding mean in pandas handles them reasonably; keep simple:
        cum_mean = pd.Series(y).expanding().mean().to_numpy()
        fig.add_trace(
            go.Scatter(
                x=x, y=cum_mean,
                mode="lines",
                name=str(fuel),
                showlegend=False,
            ),
            row=2, col=1
        )
    fig.update_xaxes(title_text="Thrust Volume", row=2, col=1)
    fig.update_yaxes(title_text="Cumulative Mean Stability Margin", row=2, col=1)

    # (2,2) rolling mean stability vs thermochemical index, per fuel (lines)
    window_size = 5
    for fuel in fuels:
        df = data.loc[data["fuel_type"] == fuel].sort_values("thermochemical_power_index").copy()
        roll = df["combustion_stability_margin"].rolling(window=window_size, min_periods=1).mean()
        fig.add_trace(
            go.Scatter(
                x=df["thermochemical_power_index"],
                y=roll,
                mode="lines",
                name=str(fuel),
                showlegend=False,
            ),
            row=2, col=2
        )
    fig.update_xaxes(title_text="Thermochemical Power Index", row=2, col=2)
    fig.update_yaxes(title_text=f"Rolling Mean Stability Margin (w={window_size})", row=2, col=2)

    fig.update_layout(
        title=f"Rocket Propulsion Dashboard 2×2 — ALL fuels ({pressure_label}, {pressure} bar)",
        height=900,
        width=1400,
        margin=dict(t=90, l=60, r=40, b=60),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12, yanchor="top"),
    )
    return fig


def fig_sunburst2(prop_df: pd.DataFrame, pressure: float) -> go.Figure:
    fig = px.sunburst(
        prop_df,
        path=["fuel_class", "fuel_type"],
        title=f"Fuel Class → Fuel Type (ambient_pressure_bar = {pressure})"
    )
    fig.update_layout(height=520, width=700, margin=dict(t=70, l=10, r=10, b=10))
    return fig


def fig_histogram(data: pd.DataFrame, pressure: float, pressure_label: str) -> go.Figure:
    required = ["combustion_temperature_K", "specific_impulse_s"]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns for histogram figure: {missing}")

    df_sorted = data.sort_values("combustion_temperature_K").copy()
    cum_mean_isp = df_sorted["specific_impulse_s"].expanding().mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Histogram(x=df_sorted["combustion_temperature_K"], nbinsx=30, opacity=0.55, name="Temperature histogram"),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=df_sorted["combustion_temperature_K"], y=cum_mean_isp, mode="lines", name="Cumulative mean Isp"),
        secondary_y=True
    )

    fig.update_xaxes(title_text="Combustion Temperature (K)")
    fig.update_yaxes(title_text="Count", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Mean Specific Impulse (s)", secondary_y=True)

    fig.update_layout(
        title=f"Temperature Histogram & Cumulative Mean Isp ({pressure_label}, {pressure} bar)",
        height=520,
        width=700,
        margin=dict(t=70, l=50, r=50, b=60),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18, yanchor="top"),
    )
    return fig


def stitch_dashboard_png(fig2x2: go.Figure, figSun: go.Figure, figHist: go.Figure) -> bytes:
    """
    Exports each plotly figure to PNG (kaleido) and stitches:
      Top: 2x2 figure full width
      Bottom: Sunburst2 (left) + Histogram (right)
    Returns PNG bytes.
    """
    img2x2 = Image.open(io.BytesIO(fig2x2.to_image(format="png", scale=2)))
    imgSun = Image.open(io.BytesIO(figSun.to_image(format="png", scale=2)))
    imgHist = Image.open(io.BytesIO(figHist.to_image(format="png", scale=2)))

    # Make bottom row same height by padding if needed
    bottom_h = max(imgSun.height, imgHist.height)
    def pad_to_height(im: Image.Image, h: int) -> Image.Image:
        if im.height == h:
            return im
        out = Image.new("RGBA", (im.width, h), (255, 255, 255, 255))
        out.paste(im, (0, (h - im.height) // 2))
        return out

    imgSun = pad_to_height(imgSun, bottom_h)
    imgHist = pad_to_height(imgHist, bottom_h)

    bottom = Image.new("RGBA", (imgSun.width + imgHist.width, bottom_h), (255, 255, 255, 255))
    bottom.paste(imgSun, (0, 0))
    bottom.paste(imgHist, (imgSun.width, 0))

    # Make overall width = max(top width, bottom width) and center narrower row
    W = max(img2x2.width, bottom.width)
    H = img2x2.height + bottom.height

    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))

    x_top = (W - img2x2.width) // 2
    x_bottom = (W - bottom.width) // 2

    canvas.paste(img2x2, (x_top, 0))
    canvas.paste(bottom, (x_bottom, img2x2.height))

    out = io.BytesIO()
    canvas.convert("RGB").save(out, format="PNG")
    return out.getvalue()


# -------------------- Dash app --------------------
app = Dash(__name__)
app.title = "Rocket Propulsion Dashboard"


app.layout = html.Div(
    style={"fontFamily": "Arial", "padding": "14px"},
    children=[
        html.H2("Rocket Propulsion Dashboard (ALL fuels, by fuel traces)"),

        html.Div(
            style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "alignItems": "center"},
            children=[
                html.Div([
                    html.Label("ambient_pressure_bar"),
                    dcc.Dropdown(
                        id="pressure",
                        options=[{"label": str(p), "value": float(p)} for p in PRESSURE_VALUES],
                        value=float(PRESSURE_VALUES[0]) if PRESSURE_VALUES else 1.01325,
                        clearable=False,
                        style={"width": "260px"},
                    ),
                ]),
                html.Button("Capture dashboard (PNG)", id="btn-capture", n_clicks=0),
                dcc.Download(id="download-dashboard"),
            ],
        ),

        html.Hr(),

        dcc.Graph(id="fig-2x2", config={"responsive": True}),
        html.Div(
            style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
            children=[
                dcc.Graph(id="fig-sunburst2", config={"responsive": True}, style={"flex": "1"}),
                dcc.Graph(id="fig-hist", config={"responsive": True}, style={"flex": "1"}),
            ]
        ),
    ]
)


@app.callback(
    Output("fig-2x2", "figure"),
    Output("fig-sunburst2", "figure"),
    Output("fig-hist", "figure"),
    Input("pressure", "value"),
)
def update_figures(pressure):
    pressure = float(pressure)
    stats, label = load_stats_for_pressure(pressure)
    prop_f = filter_prop_for_pressure(pressure)

    f2x2 = fig_2x2_all_fuels(stats, pressure, label)
    fsun = fig_sunburst2(prop_f, pressure)
    fhist = fig_histogram(stats, pressure, label)
    return f2x2, fsun, fhist


@app.callback(
    Output("download-dashboard", "data"),
    Input("btn-capture", "n_clicks"),
    State("pressure", "value"),
    prevent_initial_call=True
)
def capture_dashboard(n_clicks, pressure):
    if not n_clicks:
        raise PreventUpdate

    pressure = float(pressure)
    stats, label = load_stats_for_pressure(pressure)
    prop_f = filter_prop_for_pressure(pressure)

    f2x2 = fig_2x2_all_fuels(stats, pressure, label)
    fsun = fig_sunburst2(prop_f, pressure)
    fhist = fig_histogram(stats, pressure, label)

    png_bytes = stitch_dashboard_png(f2x2, fsun, fhist)
    filename = f"dashboard_pressure_{pressure}.png"

    return dcc.send_bytes(png_bytes, filename)


if __name__ == "__main__":
    # Run: python app.py
    app.run(debug=True)


