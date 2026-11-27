"""Load, clean and engineer features for the UK used car dataset (Kaggle).

Source: https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes
Listings were scraped in 2020, so 2020 is used as the reference year for car age.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

# cclass.csv / focus.csv are subsets of merc.csv / ford.csv, and the
# "unclean" files are messy duplicates, so only the 9 brand files are used.
BRAND_FILES = {
    "Audi": "audi.csv",
    "BMW": "bmw.csv",
    "Ford": "ford.csv",
    "Hyundai": "hyundi.csv",
    "Mercedes": "merc.csv",
    "Skoda": "skoda.csv",
    "Toyota": "toyota.csv",
    "Vauxhall": "vauxhall.csv",
    "Volkswagen": "vw.csv",
}
REFERENCE_YEAR = 2020


def load_raw(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Concatenate the brand files into one DataFrame with a `brand` column."""
    frames = []
    for brand, fname in BRAND_FILES.items():
        df = pd.read_csv(raw_dir / fname)
        df = df.rename(columns={"tax(£)": "tax"})
        df["brand"] = brand
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["model"] = df["model"].str.strip()
    return df


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop duplicates and implausible rows. Returns (clean_df, log of each step)."""
    log = [("raw", len(df))]

    df = df.drop_duplicates()
    log.append(("drop exact duplicates", len(df)))

    df = df.dropna(subset=["price", "year", "mileage", "brand"])
    log.append(("drop missing key fields", len(df)))

    df = df[df["year"].between(1990, REFERENCE_YEAR)]  # e.g. a typo year of 2060
    log.append(("year in 1990-2020", len(df)))

    df = df[(df["price"] > 0) & (df["mileage"] > 0)]
    log.append(("price > 0 and mileage > 0", len(df)))

    lo, hi = df["price"].quantile([0.005, 0.995])
    df = df[df["price"].between(lo, hi)]
    log.append(("trim price to 0.5-99.5 percentile", len(df)))

    df = add_features(df)
    hi_am = df["annual_mileage"].quantile(0.995)
    df = df[df["annual_mileage"] <= hi_am]
    log.append(("trim annual mileage at 99.5 percentile", len(df)))

    return df.reset_index(drop=True), pd.DataFrame(log, columns=["step", "rows"])


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add age, annual mileage, log price and mileage in thousands."""
    df = df.copy()
    df["age"] = REFERENCE_YEAR - df["year"]
    # A car registered in 2020 has been on the road for under a year: use 1
    # in the denominator so annual mileage is defined for it.
    df["annual_mileage"] = df["mileage"] / df["age"].clip(lower=1)
    df["mileage_k"] = df["mileage"] / 1000
    df["annual_mileage_k"] = df["annual_mileage"] / 1000
    df["log_price"] = np.log(df["price"])
    return df


def pct_effect(beta: float) -> float:
    """Convert a log-price coefficient to a percent change in price."""
    return (np.exp(beta) - 1) * 100
