import yfinance as yf
import pandas as pd
from pathlib import Path
from src.config import RETURNS_DIR, HQ_DIR

def get_monthly_returns():
    tickers = pd.read_csv(HQ_DIR / "sp500_hq.csv")["ticker"].tolist()

    data = yf.download(
        tickers,
        start="2013-01-01",
        end="2024-01-01",
        interval="1mo",
        auto_adjust=True,
        group_by="ticker"
    )

    out = []
    for t in tickers:
        df = data[t].reset_index()
        df["ticker"] = t
        df["ret"] = df["Close"].pct_change()
        df = df[["Date","ticker","Close","ret"]]
        out.append(df)

    final = pd.concat(out)
    final = final.dropna(subset=["ret"])

    RETURNS_DIR.mkdir(parents=True, exist_ok=True)
    final.to_csv(RETURNS_DIR / "monthly_returns.csv", index=False)
    print("Saved:", RETURNS_DIR / "monthly_returns.csv")


if __name__ == "__main__":
    get_monthly_returns()


