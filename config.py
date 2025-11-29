from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = PROJECT_ROOT / "data_raw"
DATA_PROCESSED = PROJECT_ROOT / "data_processed"

NIGHTLIGHTS_DIR = DATA_RAW / "nightlights"
HQ_DIR          = DATA_RAW / "hq"
RETURNS_DIR     = DATA_RAW / "returns"
FACTORS_DIR     = DATA_RAW / "factors"

FIRM_MONTH_PANEL = DATA_PROCESSED / "firm_month_panel.csv"
