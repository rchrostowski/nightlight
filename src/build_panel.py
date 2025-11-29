import pandas as pd
from pathlib import Path
from src.config import (
    HQ_DIR,
    RETURNS_DIR,
    FACTORS_DIR,
    DATA_PROCESSED,
)

def build_panel():
    hq = pd.read_csv(HQ_DIR / "sp500_hq.csv")
    rets = pd.read_csv(RETURNS_DIR / "monthly_returns.csv")
    ff = pd.read_csv(FACTORS_DIR / "ff_factors.csv")

    rets = rets.rename(columns={"Date":"date"})
    rets["date"] = pd.to_datetime(rets["date"])
    ff["date"] = pd.to_datetime(ff["date"])

    # Merge HQ → returns
    final = rets.merge(hq, on="ticker", how="left")

    # Merge factors
    final = final.merge(ff, on="date", how="left")

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_csv(DATA_PROCESSED / "firm_month_panel.csv", index=False)

    print("Saved:", DATA_PROCESSED / "firm_month_panel.csv")

if __name__ == "__main__":
    build_panel()


