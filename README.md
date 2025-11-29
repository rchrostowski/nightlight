# Night Lights, Local Economic Activity, and Stock Returns  
FIN 377 – Project Repository  
By Ryan Chrostowski, Kosta Kalavruzos, Adil Alybaev  

## Overview  
This project tests whether monthly changes in nighttime satellite radiance around firm headquarters (ΔLight) predict next-month stock returns.  

We build:  
- A firm-month panel of radiance × returns × factors  
- Portfolios sorted on ΔLight  
- CAPM / FF3 regressions (Table 1 style)  
- A Streamlit dashboard with a 3D globe visualization  

## Repository Structure  
nightlights-project/
│
├─ README.md
│
├─ requirements.txt
│
├─ data_raw/
│   ├─ nightlights/              # put .tif files here manually
│   ├─ hq/
│   │    └─ sp500_hq.csv
│   ├─ returns/
│   └─ factors/
│
├─ data_processed/
│   └─ firm_month_panel.csv
│
├─ src/
│   ├─ config.py
│   ├─ get_factors.py
│   ├─ get_returns.py
│   ├─ get_hq_data.py
│   ├─ build_nightlights_signal.py
│   ├─ build_panel.py
│   └─ capm_table1.py
│
└─ notebooks/
    ├─ 01_explore_hq_and_lights.ipynb
    ├─ 02_signal_and_portfolios.ipynb
    └─ 03_capm_table1.ipynb

