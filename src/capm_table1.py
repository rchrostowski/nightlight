import pandas as pd
import statsmodels.api as sm
from config import FIRM_MONTH_PANEL

def capm_table():
    df = pd.read_csv(FIRM_MONTH_PANEL, parse_dates=["date"])

    df = df.dropna(subset=["light_change"])
    df["decile"] = df.groupby("date")["light_change"].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates="drop") + 1)
    df["ret_excess_fwd"] = df.groupby("ticker")["ret_excess"].shift(-1)

    port = df.dropna(subset=["ret_excess_fwd"]).groupby(["date", "decile"])["ret_excess_fwd"].mean().unstack()
    port["HighLow"] = port[10] - port[1]

    ff = df[["date", "Mkt-RF"]].drop_duplicates().set_index("date")
    reg_df = port.join(ff, how="inner")

    results = []
    for col in port.columns:
        y = reg_df[col]
        X = sm.add_constant(reg_df["Mkt-RF"])
        model = sm.OLS(y, X, missing="drop").fit()
        results.append([col, model.params["const"], model.tvalues["const"], model.params["Mkt-RF"]])

    return pd.DataFrame(results, columns=["Portfolio", "CAPM_alpha", "t_stat", "beta"])

if __name__ == "__main__":
    print(capm_table())

