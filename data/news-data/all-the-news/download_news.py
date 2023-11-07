# +
# https://components.one/datasets/all-the-news-2-news-articles-dataset

import polars as pl
from tqdm.notebook import tqdm
# -

# download and unzip
df = pl.scan_csv('all-the-news-2-1.csv')

df.columns

groups = df.select(["year", "month"]).unique()

year_months = groups.unique().collect().sort(["year", "month"])

for year, month in tqdm(list(year_months.iter_rows())):
    df.filter(
        (pl.col("year") == year) & (pl.col("month") == month)
    ).collect().write_parquet(f'filtered/year-{year}-month-{month}.parquet')



