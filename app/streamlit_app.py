import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Make sure Python can find the src/ package when running `streamlit run app/streamlit_app.py`
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import FIRM_MONTH_PANEL  # type: ignore
from src.capm_table1 import capm_table   # type: ignore


# ----------------------------
# Streamlit Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Night Lights & Stock Returns",
    layout="wide"
)

# Basic dark theme styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #050509;
            color: #f5f5f5;
        }
        /* Make tables readable on dark background */
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

# ----------------------------
# Data Loading Helpers
# ----------------------------
@st.cache_data(show_spinner=True)
def load_panel() -> pd.DataFrame:
    """Load the firm-month panel from disk."""
    if not Path(FIRM_MONTH_PANEL).exists():
        return pd.DataFrame()
    df = pd.read_csv(FIRM_MONTH_PANEL, parse_dates=["date"])
    return df


@st.cache_data(show_spinner=True)
def load_capm_table() -> pd.DataFrame:
    """Run / load the CAPM Table 1 style results."""
    try:
        table = capm_table()
        return table
    except Exception as e:
        st.warning(f"Could not compute CAPM table: {e}")
        return pd.DataFrame()


df_panel = load_panel()

# ----------------------------
# Page Title
# ----------------------------
st.title("Night Lights, Local Economic Activity, and Stock Returns")

st.write(
    "This dashboard explores whether changes in satellite-measured nighttime lights "
    "around firm headquarters (ΔLight) predict next-month stock returns and generate "
    "abnormal CAPM alpha."
)

# ----------------------------
# Tabs
# ----------------------------
tab_overview, tab_factor, tab_globe, tab_ticker = st.tabs(
    ["Overview", "Factor Results (CAPM)", "3D Globe", "Ticker Lookup"]
)

# ----------------------------
# Overview Tab
# ----------------------------
with tab_overview:
    st.header("Project Overview")

    st.markdown(
        """
        We construct a firm–month panel combining:

        - Headquarters latitude/longitude  
        - VIIRS nighttime light radiance and its monthly change (ΔLight)  
        - Monthly stock returns for S&P 500 firms  
        - Fama–French factor data  

        Each month, firms are sorted into deciles based on ΔLight. We then compute
        the next-month excess returns for each decile and form a **High − Low**
        portfolio (top ΔLight decile minus bottom decile).  

        Our core empirical test is whether this High − Low portfolio earns a
        statistically significant **CAPM alpha**, indicating that luminosity-based
        information has predictive power beyond simple market exposure.
        """
    )

    if df_panel.empty:
        st.warning(
            "No panel data found yet. Run the data-building scripts "
            "(get_factors.py, get_returns.py, build_nightlights_signal.py, "
            "build_panel.py) to populate `data_processed/firm_month_panel.csv`."
        )
    else:
        st.success("Firm–month panel loaded successfully.")
        st.write("Preview of the merged panel:")
        st.dataframe(df_panel.head())

# ----------------------------
# Factor Results (CAPM) Tab
# ----------------------------
with tab_factor:
    st.header("CAPM Table 1 — ΔLight-Sorted Portfolios")

    if df_panel.empty:
        st.warning("Panel data not loaded. Cannot compute CAPM results.")
    else:
        table = load_capm_table()
        if table.empty:
            st.warning("CAPM table is empty or could not be computed.")
        else:
            st.markdown(
                """
                For each ΔLight-sorted portfolio (deciles and the High−Low spread),
                we estimate the CAPM regression:

                \\[
                r_{p,t} - r_{f,t} = \\alpha_p + \\beta_p (Mkt - RF)_t + \\varepsilon_{p,t}
                \\]

                The key statistic of interest is **α (CAPM_alpha)** for the High−Low
                portfolio, along with its t-statistic. A positive and significant α
                suggests that the night-lights signal qualifies as an asset-pricing anomaly.
                """
            )

            st.subheader("CAPM Alpha, t-Statistic, and Beta by Portfolio")
            st.dataframe(table.style.format({"CAPM_alpha": "{:.4f}", "t_stat": "{:.2f}", "beta": "{:.2f}"}))

# ----------------------------
# 3D Globe Tab
# ----------------------------
with tab_globe:
    st.header("3D Globe — Headquarters & Nighttime Lights")

    if df_panel.empty:
        st.warning("Panel data not loaded. Cannot render HQ locations.")
    else:
        if not {"lat", "lon"}.issubset(df_panel.columns):
            st.warning(
                "Latitude/longitude not found in the panel. "
                "Ensure `sp500_hq.csv` has lat/lon and that lights_panel.csv "
                "propagates them into the merged panel."
            )
        else:
            st.markdown(
                """
                The globe below shows a subset of firm headquarters as points on an
                orthographic projection. A more advanced version could color or size
                points by average ΔLight, recent change, or other firm characteristics.
                """
            )

            # Use one row per ticker for the globe view
            hq_sample = (
                df_panel
                .dropna(subset=["lat", "lon"])
                .drop_duplicates(subset=["ticker"])[["ticker", "lat", "lon"]]
            )

            # If you want to color by something, you could merge in avg light_change
            fig = px.scatter_geo(
                hq_sample,
                lat="lat",
                lon="lon",
                hover_name="ticker",
                projection="orthographic"
            )
            fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                paper_bgcolor="#050509",
                geo=dict(
                    showland=True,
                    landcolor="rgb(10,10,40)",
                    showocean=True,
                    oceancolor="rgb(5,5,25)",
                    showcountries=True,
                )
            )
            st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Ticker Lookup Tab
# ----------------------------
with tab_ticker:
    st.header("Ticker Lookup — ΔLight and Returns")

    if df_panel.empty:
        st.warning("Panel data not loaded. Cannot show ticker-level details.")
    else:
        tickers = sorted(df_panel["ticker"].dropna().unique().tolist())
        if not tickers:
            st.warning("No tickers found in panel dataset.")
        else:
            selected = st.selectbox("Select a ticker:", tickers, index=0)

            sub = (
                df_panel[df_panel["ticker"] == selected]
                .sort_values("date")
                .set_index("date")
            )

            st.subheader(f"ΔLight and Excess Return Over Time — {selected}")

            cols_to_plot = []
            if "light_change" in sub.columns:
                cols_to_plot.append("light_change")
            if "ret_excess" in sub.columns:
                cols_to_plot.append("ret_excess")

            if cols_to_plot:
                st.line_chart(sub[cols_to_plot])
            else:
                st.write("No plottable columns found for this ticker.")

            st.write("Raw data:")
            st.dataframe(sub.reset_index()[["date"] + cols_to_plot].tail(24))
