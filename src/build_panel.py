import pandas as pd
from config import RETURNS_DIR, FACTORS_DIR, DATA_PROCESSED, FIRM_MONTH_PANEL

def build():
    rets = pd.read_csv(RETURNS_DIR / "sp500_monthly_returns.csv", parse_dates=["date"])
    ff = pd.read_csv(FACTORS_DIR / "ff_factors.csv", parse_dates=["Unnamed: 0"]).rename(columns={"Unnamed: 0":"date"})
    lights = pd.read_csv(DATA_PROCESSED / "lights_panel.csv", parse_dates=["date"])

    for c in ff.columns:
        if c != "date":
            ff[c] = ff[c] / 100

    df = (
        rets.merge(lights, on=["ticker", "date"], how="inner")
            .merge(ff, on="date", how="inner")
    )
    df["ret_excess"] = df["ret"] - df["RF"]
    df.to_csv(FIRM_MONTH_PANEL, index=False)

if __name__ == "__main__":
    build()

