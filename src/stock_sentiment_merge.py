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


# Time the merge operation
time_start = time.time()
merged_data = example_stock_data
for ex_sent_df in example_sentiment_data:
    merged_data = pd.merge_asof(
        merged_data,
        ex_sent_df,
        left_on="Date",
        right_on="time",
        direction="nearest",
    )


start = "2016-01-01"
end = "2016-02-01"

# print all entries from start to end
print(merged_data[(merged_data["Date"] >= start) & (merged_data["Date"] <= end)])

time_end = time.time()
print(
    f"Time to merge: {time_end - time_start} seconds for entries from {start} to {end}"
)
