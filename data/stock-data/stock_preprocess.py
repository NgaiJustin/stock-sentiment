from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List
from random import randint
from tqdm import tqdm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.seterr(divide="ignore", invalid="ignore")

flux_dir = "./flux"
etf_dir = "./ETFs"
stocks_dir = "./Stocks"


@dataclass
class Entry:
    Date: datetime
    Open: float
    High: float
    Low: float
    Close: float
    Volume: int
    OpenInt: int


def bounded_random_walk(
    length: int,
    lower_bound: float,
    upper_bound: float,
    start: float,
    end: float,
    std=1,
):
    assert lower_bound <= start and lower_bound <= end
    assert start <= upper_bound and end <= upper_bound

    bounds = upper_bound - lower_bound

    rand = (std * (np.random.random(length) - 0.5)).cumsum()
    rand_trend = np.linspace(rand[0], rand[-1], length)
    rand_deltas = rand - rand_trend
    rand_deltas /= np.max([1, (rand_deltas.max() - rand_deltas.min()) / bounds])

    trend_line = np.linspace(start, end, length)
    upper_bound_delta = upper_bound - trend_line
    lower_bound_delta = lower_bound - trend_line

    upper_slips_mask = (rand_deltas - upper_bound_delta) >= 0
    upper_deltas = rand_deltas - upper_bound_delta
    rand_deltas[upper_slips_mask] = (upper_bound_delta - upper_deltas)[upper_slips_mask]

    lower_slips_mask = (lower_bound_delta - rand_deltas) >= 0
    lower_deltas = lower_bound_delta - rand_deltas
    rand_deltas[lower_slips_mask] = (lower_bound_delta + lower_deltas)[lower_slips_mask]

    return trend_line + rand_deltas


def flux(entry: Entry) -> List[Entry]:
    n = 480

    # Generate 480 entries for each day in a random walk fashion
    entries = []

    # Generate price trend from random walk
    price_trend = bounded_random_walk(
        length=n,
        lower_bound=entry.Low,
        upper_bound=entry.High,
        start=entry.Open,
        end=entry.Close,
    )

    # Partition volume into 480 random pieces
    a = entry.Volume

    volume_trend: List[int] = []

    cum_entries = [0, a]
    for _ in range(n - 1):
        cum_entries.append(randint(0, a))
    cum_entries.sort()

    for i in range(len(cum_entries) - 1):
        volume_trend.append(cum_entries[i + 1] - cum_entries[i])

    assert sum(volume_trend) == entry.Volume
    assert len(volume_trend) == len(price_trend)

    # Set base date
    base_date: datetime = entry.Date

    base_date.replace(hour=9, minute=00)

    for i in range(n):
        small_delta, big_delta = sorted(np.random.random((2,)) * 0.01)

        open = price_trend[i] - small_delta
        high = price_trend[i] + big_delta
        low = price_trend[i] - big_delta
        close = price_trend[i] + small_delta

        # 3 d.p. rounding
        open = round(open, 4)
        high = round(high, 4)
        low = round(low, 4)
        close = round(close, 4)

        entries.append(
            Entry(
                Date=base_date.replace(hour=9 + i // 60, minute=i % 60),
                Open=open,
                High=high,
                Low=low,
                Close=close,
                Volume=volume_trend[i],
                OpenInt=entry.OpenInt,
            )
        )

    return entries


def process_txt(dir_path: Path):
    for file_path in dir_path.iterdir():
        if file_path.suffix != ".txt":
            continue

        df = pd.read_csv(file_path, parse_dates=["Date"])
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

        flux_entries = []
        # iterate over all entries in df
        for _, row in tqdm(df.iterrows(), total=df.shape[0]):
            entry = Entry(
                Date=datetime.strptime(row["Date"], "%Y-%m-%d"),
                Open=row["Open"],
                High=row["High"],
                Low=row["Low"],
                Close=row["Close"],
                Volume=row["Volume"],
                OpenInt=row["OpenInt"],
            )
            flux_entries += flux(entry)

        id = file_path.stem[:-3]
        df_flux = pd.DataFrame(flux_entries)
        df_flux.to_csv(file_path.parent / f"{id}.csv", index=False)


process_txt(Path(flux_dir))

# # Visualize random walk
# random_walk = bounded_random_walk(480, 23.946, 24.333, 23.95, 24.000)
# plt.plot(random_walk)
# plt.show()
