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
example_stock_data['time'] = example_stock_data['Date']
example_stock_data = example_stock_data.set_index('time')

example_sentiment_dir = "../data/out/sentiment"
example_sentiment_data = []
for path in pathlib.Path(example_sentiment_dir).iterdir():
    if path.is_file() and path.suffix == ".parquet":
        df = pd.read_parquet(path)
        example_sentiment_data.append(df)
        df["time"] = pd.to_datetime(df["time"], format="mixed")

example_sentiment_data = pd.concat(example_sentiment_data).set_index('time').sort_index()

example_stock_data = example_stock_data[(pd.Timestamp("2016-01-01 00:00:00") <= example_stock_data['Date']) & (example_stock_data['Date'] <= pd.Timestamp("2017-01-01 00:00:00"))]

example_sentiment_data
example_stock_data

# +
import heapq

class SentimentStore:
    def __init__(self, tolerance):
        self.latest_sentiments = {}
        self.tolerance = tolerance
    
    def put_sentiment(self, stock, timestamp, sentiment_tuple):
        self.latest_sentiments[stock] = (timestamp, sentiment_tuple)
    
    def get_sentiment(self, stock, ts):
        if stock in self.latest_sentiments:
            timestamp, s_t = self.latest_sentiments[stock]
            if ts - timestamp <= self.tolerance:
                return s_t
        return None


class StockController:
    def __init__(self, stock_names, stock_data, sentiment_data):
        self.sentiment_store = SentimentStore(pd.Timedelta("1h"))
        self.stocks = stock_names
        self.dfs = []
        # self.rev_stocks = {}
        for i, stock in enumerate(self.stocks):
            self.dfs.append(sentiment_data[stock].iterrows())
            self.dfs.append(stock_data[stock].iterrows())
            # self.rev_stocks[stock] = i
        self.ptrs = [0 for _ in self.dfs]
        self.heap = []
        for i, df in enumerate(self.dfs):
            time, row = next(df)
            self.heap.append((time, i, row))
        heapq.heapify(self.heap)
    
    def run(self):
        
        left_rows = []
        right_rows = []
        stocks = []
        
        while self.heap:
            ts, idx, row = heapq.heappop(self.heap)
            stock = self.stocks[idx // 2]
            self.ptrs[idx] += 1

            if idx % 2 == 0:  # is a sentiment record
                self.sentiment_store.put_sentiment(stock, ts, row)
            else:  # is a stock record
                sent = self.sentiment_store.get_sentiment(stock, ts)
                if sent is not None:
                    left_rows.append(row)
                    right_rows.append(sent)
                    stocks.append(stock)

            next_time, next_row = next(self.dfs[idx], (None, None))
            if next_row is not None:
                heapq.heappush(self.heap, (next_time, idx, next_row))
        
        return stocks, left_rows, right_rows


# -

sc = StockController(['AAPL'], {"AAPL": example_stock_data}, {"AAPL": example_sentiment_data})
stocks, left_rows, right_rows = sc.run()

pd.concat(
    [pd.Series(stocks), pd.DataFrame.from_records(left_rows), pd.DataFrame.from_records(right_rows)],
    axis=1
)
