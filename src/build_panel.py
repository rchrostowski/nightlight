import pandas as pd
from src.config import (
    HQ_DIR,
    RETURNS_DIR,
    FACTORS_DIR,
    DATA_PROCESSED,
    FIRM_MONTH_PANEL,
)

def build_panel():
    hq = pd.read_csv(HQ_DIR / "sp500_hq.csv")
    rets = pd.read_csv(RETURNS_DIR / "monthly_returns.csv")
    ff = pd.read_csv(FACTORS_DIR / "ff_factors.csv")

    rets = rets.rename(columns={"Date": "date"})
    rets["date"] = pd.to_datetime(rets["date"])
    ff["date"] = pd.to_datetime(ff["date"])

    # Merge HQ (lat/lon) into returns
    panel = rets.merge(hq, on="ticker", how="left")

    # Merge FF factors by date
    panel = panel.merge(ff, on="date", how="left")

    # Compute excess return and placeholder light_change (for now)
    if "RF" in panel.columns:
        panel["ret_excess"] = panel["ret"] - panel["RF"]
    else:
        panel["ret_excess"] = panel["ret"]

    # TEMP: fake ΔLight so the dashboard works
    panel["light_change"] = 0.03  # placeholder until we wire real VIIRS data

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    panel.to_csv(FIRM_MONTH_PANEL, index=False)
    print(f"Saved {FIRM_MONTH_PANEL}")

if __name__ == "__main__":
    build_panel()


