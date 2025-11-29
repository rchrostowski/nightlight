import pandas as pd
from pandas_datareader import famafrench
from src.config import FACTORS_DIR

def get_factors():
    ff = famafrench.FamaFrenchReader("F-F_Research_Data_Factors", start="2013").read()[0]
    ff = ff.reset_index().rename(columns={"Date": "date"})
    FACTORS_DIR.mkdir(parents=True, exist_ok=True)
    outpath = FACTORS_DIR / "ff_factors.csv"
    ff.to_csv(outpath, index=False)
    print(f"Saved {outpath}")

if __name__ == "__main__":
    get_factors()


