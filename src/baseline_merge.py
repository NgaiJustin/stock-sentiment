# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import time
import pathlib

example_stock_data_path = "../data/out/aapl.csv"
example_stock_data = pd.read_csv(example_stock_data_path)
example_stock_data["Date"] = pd.to_datetime(example_stock_data["Date"], format="mixed")

example_sentiment_dir = "../data/out/sentiment"
example_sentiment_data = []
for path in pathlib.Path(example_sentiment_dir).iterdir():
    if path.is_file() and path.suffix == ".parquet":
        df = pd.read_parquet(path)
        example_sentiment_data.append(df)
        df["time"] = pd.to_datetime(df["time"], format="mixed")

example_sentiment_data = pd.concat(example_sentiment_data).set_index('time').sort_index()

merged_data = pd.merge_asof(
    example_stock_data,
    example_sentiment_data,
    left_on="Date",
    right_on="time",
    direction="backward",
    tolerance=pd.Timedelta("1h"),
)

merged_data[merged_data["cumulative_sentiment"].notna()]

list(example_sentiment_data.iterrows())[:2]


