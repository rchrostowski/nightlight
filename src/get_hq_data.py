import pandas as pd
from pathlib import Path
from src.config import HQ_DIR

"""
get_hq_data.py

Simple helper script to create a headquarters file (sp500_hq.csv)
with a small set of firms and hard-coded latitude/longitude values.

In a more advanced version, this could scrape SEC EDGAR or another source.
For now, this is enough to test the pipeline and map visuals.
"""

def write_sample_hq():
    HQ_DIR.mkdir(parents=True, exist_ok=True)

    data = [
        # ticker, company,          lat,       lon
        ("AAPL", "Apple Inc.",      37.3349,  -122.0090),
        ("MSFT", "Microsoft Corp.", 47.6396,  -122.1281),
        ("AMZN", "Amazon.com Inc.", 47.6229,  -122.3373),
        ("GOOGL","Alphabet Inc.",   37.4220,  -122.0841),
        ("META","Meta Platforms",   37.4848,  -122.1484),
        ("TSLA","Tesla Inc.",       37.3947,  -122.1503),
        ("NVDA","NVIDIA Corp.",     37.3706,  -121.9624),
        ("JPM", "JPMorgan Chase",   40.7128,  -74.0060),
        ("WMT", "Walmart Inc.",     36.3729,  -94.2080),
        ("XOM", "Exxon Mobil",      29.7604,  -95.3698),
    ]

    df = pd.DataFrame(data, columns=["ticker", "company", "lat", "lon"])
    outpath = HQ_DIR / "sp500_hq.csv"
    df.to_csv(outpath, index=False)
    print(f"Wrote sample HQ data to {outpath}")

if __name__ == "__main__":
    write_sample_hq()

