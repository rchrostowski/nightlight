import pandas as pd
import yfinance as yf
from config import RETURNS_DIR

def load_sp500():
    tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    return tables[0]["Symbol"].tolist()

def download_returns():
    RETURNS_DIR.mkdir(parents=True, exist_ok=True)
    tickers = load_sp500()

    data = yf.download(
        tickers,
        start="2013-01-01",
        end="2024-12-31",
        interval="1mo",
        auto_adjust=True,
        progress=False
    )["Close"]

    df = data.pct_change().reset_index().melt(id_vars="Date", var_name="ticker", value_name="ret")
    df.rename(columns={"Date": "date"}, inplace=True)
    df.to_csv(RETURNS_DIR / "sp500_monthly_returns.csv", index=False)

if __name__ == "__main__":
    download_returns()

