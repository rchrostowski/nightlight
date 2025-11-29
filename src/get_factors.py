import pandas as pd
from pandas_datareader import famafrench
from pathlib import Path
from src.config import FACTORS_DIR

def get_factors():
    ff = famafrench.FamaFrenchReader("F-F_Research_Data_Factors", start="2010").read()[0]
    ff = ff.reset_index().rename(columns={"Date":"date"})
    FACTORS_DIR.mkdir(parents=True, exist_ok=True)
    ff.to_csv(FACTORS_DIR / "ff_factors.csv", index=False)
    print("Saved:", FACTORS_DIR / "ff_factors.csv")

if __name__ == "__main__":
    get_factors()


