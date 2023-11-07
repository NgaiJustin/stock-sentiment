# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
from pathlib import Path

# +
data_root = Path('../data/')
articles_path = data_root / "news-data" / "all-the-news" / "year-2016-month-1.0.parquet"

articles = pd.read_parquet(articles_path)
sid = SentimentIntensityAnalyzer()


# -

def nltk_sentiment(article):
    d = sid.polarity_scores(article)
    return d['pos'], d['neg'], d['neu']


