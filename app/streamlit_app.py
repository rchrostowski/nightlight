from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Night Lights & Stock Returns",
    layout="wide"
)

# -------------------------
# Global styling
# -------------------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #050509;
            color: #f5f5f5;
        }
        .stDataFrame, .stTable {
            color: #f5f5f5;
        }
        h1, h2, h3, h4 {
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Dummy data builders (fallback)
# -------------------------

@st.cache_data
def build_dummy_panel() -> pd.DataFrame:
    """Fallback firm-month panel if real CSV is missing."""
    data = [
        # date, ticker, ret, ret_excess, light_level, light_change, RF, Mkt-RF, lat, lon
        ["2023-01-01","AAPL",0.02,0.018,10.0,0.05,0.002,0.01,37.3349,-122.0090],
        ["2023-01-01","MSFT",0.015,0.013,9.5,0.03,0.002,0.01,47.6396,-122.1281],
        ["2023-01-01","AMZN",0.01,0.008,8.0,0.02,0.002,0.01,47.6229,-122.3373],
        ["2023-02-01","AAPL",0.01,0.007,10.5,0.04,0.003,0.012,37.3349,-122.0090],
        ["2023-02-01","MSFT",0.012,0.009,9.8,0.02,0.003,0.012,47.6396,-122.1281],
        ["2023-02-01","AMZN",0.008,0.005,8.1,0.01,0.003,0.012,47.6229,-122.3373],
        ["2023-03-01","AAPL",0.015,0.013,10.9,0.03,0.002,0.009,37.3349,-122.0090],
        ["2023-03-01","MSFT",0.017,0.015,10.0,0.04,0.002,0.009,47.6396,-122.1281],
        ["2023-03-01","AMZN",0.009,0.007,8.3,0.02,0.002,0.009,47.6229,-122.3373],
    ]
    cols = ["date","ticker","ret","ret_excess","light_level","light_change","RF","Mkt-RF","lat","lon"]
    df = pd.DataFrame(data, columns=cols)
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data
def build_dummy_capm_table() -> pd.DataFrame:
    """Simple static CAPM-style table for the Factor Results tab."""
    return pd.DataFrame({
        "Portfolio": ["Port1","Port5","Port10","HighLow"],
        "CAPM_alpha": [0.0005, 0.0010, 0.0020, 0.0015],
        "t_stat":     [0.8,    1.5,    2.3,    2.0],
        "beta":       [0.9,    1.0,    1.1,    0.2],
    })


@st.cache_data
def load_panel() -> pd.DataFrame:
    """
    Try to load real firm_month_panel.csv from data_processed.
    If anything goes wrong, fall back to dummy panel.
    """
    project_root = Path(__file__).resolve().parents[1]
    panel_path = project_root / "data_processed" / "firm_month_panel.csv"

    try:
        df = pd.read_csv(panel_path)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        st.warning(f"Could not load real panel ({e}). Using demo data instead.")
        return build_dummy_panel()


@st.cache_data
def load_capm_table() -> pd.DataFrame:
    """
    For now, always use dummy CAPM table.
    Later we can wire this to a real capm_table() function.
    """
    return build_dummy_capm_table()


df_panel = load_panel()
capm_tbl = load_capm_table()

# -------------------------
# Layout
# -------------------------

st.title("Night Lights, Local Economic Activity, and Stock Returns")

st.write(
    "This dashboard visualizes the idea that changes in nighttime satellite lights "
    "around firm headquarters (ΔLight) might be related to next-month excess returns."
)

tab_overview, tab_factor, tab_globe, tab_ticker = st.tabs(
    ["Overview", "Factor Results (CAPM)", "3D Globe", "Ticker Lookup"]
)

# -------------------------
# Overview
# -------------------------
with tab_overview:
    st.header("Project Overview")
    st.markdown(
        """
        In the full version of this project, we:

        - Merge firm headquarters coordinates with monthly night-lights data  
        - Construct a ΔLight signal for each firm each month  
        - Sort firms into portfolios by ΔLight and compute next-month excess returns  
        - Estimate CAPM-style models to test if the ΔLight long–short portfolio earns alpha  

        Right now, this app will use your real processed dataset
        (`data_processed/firm_month_panel.csv`) **if it exists**, and otherwise
        falls back to a small synthetic demo panel.
        """
    )
    st.subheader("Panel Preview")
    st.dataframe(df_panel.head())

# -------------------------
# Factor Results
# -------------------------
with tab_factor:
    st.header("CAPM Table 1 — ΔLight-Sorted Portfolios (Demo)")
    st.markdown(
        """
        In the live research version, this table would be estimated from ΔLight-sorted portfolios
        using a CAPM regression:

        \\[
        r_{p,t} - r_{f,t} = \\alpha_p + \\beta_p (Mkt - RF)_t + \\varepsilon_{p,t}.
        \\]

        For now, we display placeholder values to illustrate the structure of the Table 1 output.
        """
    )
    st.dataframe(
        capm_tbl.style.format(
            {"CAPM_alpha": "{:.4f}", "t_stat": "{:.2f}", "beta": "{:.2f}"}
        )
    )

# -------------------------
# 3D Globe (enhanced)
# -------------------------
with tab_globe:
    st.header("3D Globe — Headquarters & Nighttime Lights (Enhanced Demo)")

    if not {"lat", "lon"}.issubset(df_panel.columns):
        st.warning("lat/lon not found in the panel; cannot render globe.")
    else:
        sample = (
            df_panel
            .dropna(subset=["lat","lon"])
            .drop_duplicates(subset=["ticker"])[["ticker","lat","lon"]]
        )

        fig = px.scatter_geo(
            sample,
            lat="lat",
            lon="lon",
            hover_name="ticker",
            projection="orthographic",
        )

        # Dark space look + subtle country outlines
        fig.update_layout(
            geo=dict(
                projection_type="orthographic",
                showland=True,
                landcolor="#050510",
                showocean=True,
                oceancolor="#020207",
                bgcolor="#050509",
                showcountries=True,
                countrycolor="rgba(255,255,255,0.25)",
                showcoastlines=False,
                showlakes=False,
                showrivers=False,
            ),
            paper_bgcolor="#050509",
            plot_bgcolor="#050509",
            margin=dict(r=0, t=0, l=0, b=0),
        )

        # Neon-glow markers
        fig.update_traces(
            marker=dict(
                size=14,
                color="rgba(0,255,180,0.95)",        # bright aqua
                line=dict(width=6, color="rgba(0,255,180,0.35)"),
                opacity=1,
            )
        )

        # Add NASA Earth-at-night texture as a background image
        fig.add_layout_image(
            dict(
                source="https://eoimages.gsfc.nasa.gov/images/imagerecords/55000/55167/earth_lights_lrg.jpg",
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                opacity=0.85,
                layer="below",
            )
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Ticker Lookup
# -------------------------
with tab_ticker:
    st.header("Ticker Lookup — ΔLight and Excess Returns")

    if "ticker" not in df_panel.columns:
        st.warning("No 'ticker' column found in panel.")
    else:
        tickers = sorted(df_panel["ticker"].dropna().unique().tolist())
        if not tickers:
            st.warning("No tickers available in the panel.")
        else:
            selected = st.selectbox("Select a ticker:", tickers, index=0)
            sub = (
                df_panel[df_panel["ticker"] == selected]
                .sort_values("date")
                .set_index("date")
            )

            cols_to_plot = []
            if "light_change" in sub.columns:
                cols_to_plot.append("light_change")
            if "ret_excess" in sub.columns:
                cols_to_plot.append("ret_excess")

            if cols_to_plot:
                st.subheader(f"ΔLight and Excess Return Over Time — {selected}")
                st.line_chart(sub[cols_to_plot])
                st.write("Recent data:")
                st.dataframe(sub[cols_to_plot].tail(12))
            else:
                st.write("No plottable columns ('light_change' / 'ret_excess') for this ticker.")


