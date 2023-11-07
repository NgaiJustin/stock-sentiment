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

# +
articles = pd.read_parquet('filtered/year-2016-month-1.0.parquet')
sid = SentimentIntensityAnalyzer()

sentiments = []
for article in tqdm(list(articles.iloc[:100].itertuples())):
    sentiments.append(sid.polarity_scores(article.article))
sentiments
# -

articles.head()

articles['date'].describe()


