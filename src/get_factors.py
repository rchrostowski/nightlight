import pandas as pd
from pandas_datareader import famafrench
from config import FACTORS_DIR

def download_factors():
    FACTORS_DIR.mkdir(parents=True, exist_ok=True)

    ff = famafrench.FamaFrenchReader(
        "F-F_Research_Data_5_Factors_2x3",
        start="2010"
    ).read()[0]

    ff.index = pd.to_datetime(ff.index, format="%Y%m")
    ff.to_csv(FACTORS_DIR / "ff_factors.csv")

if __name__ == "__main__":
    download_factors()

