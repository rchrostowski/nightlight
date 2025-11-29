import yfinance as yf
import pandas as pd
from src.config import HQ_DIR, RETURNS_DIR

def get_monthly_returns():
    tickers = pd.read_csv(HQ_DIR / "sp500_hq.csv")["ticker"].tolist()

    data = yf.download(
        tickers,
        start="2013-01-01",
        end="2024-01-01",
        interval="1mo",
        auto_adjust=True,
        group_by="ticker",
        progress=False,
    )

    out = []
    for t in tickers:
        df = data[t].reset_index()
        df["ticker"] = t
        df["ret"] = df["Close"].pct_change()
        df = df[["Date", "ticker", "Close", "ret"]]
        out.append(df)

    final = pd.concat(out, ignore_index=True)
    final = final.dropna(subset=["ret"])

    RETURNS_DIR.mkdir(parents=True, exist_ok=True)
    outpath = RETURNS_DIR / "monthly_returns.csv"
    final.to_csv(outpath, index=False)
    print(f"Saved {outpath}")

if __name__ == "__main__":
    get_monthly_returns()



