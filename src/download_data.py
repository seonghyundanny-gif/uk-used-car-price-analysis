"""Download the Kaggle dataset into data/raw (public dataset, no login needed).

    python src/download_data.py
"""
import shutil
from pathlib import Path

import kagglehub

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

if __name__ == "__main__":
    src = Path(kagglehub.dataset_download("adityadesai13/used-car-dataset-ford-and-mercedes"))
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.csv"):
        shutil.copy(f, RAW_DIR / f.name)
    print("Saved to", RAW_DIR)
