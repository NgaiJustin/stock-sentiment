import pandas as pd
from nltk import tokenize
from tqdm.notebook import tqdm

articles = pd.read_parquet('filtered/year-2016-month-1.0.parquet')
dictionary = pd.read_parquet('../dictionaries/reformatted_masterdict.parquet')

# +
sentiments = []

for article in tqdm(list(articles.iloc[:100].itertuples())):
    tokens = tokenize.word_tokenize(article.article)
    positive_count = 0
    negative_count = 0
    uncertain_count = 0
    count = 0
    for token in tokens:
        token = token.upper()
        count += 1
        if token in dictionary.index:
            positive_count += dictionary.loc[token]['Positive']
            negative_count += dictionary.loc[token]['Negative']
            uncertain_count += dictionary.loc[token]['Uncertainty']
    sentiments.append((count, positive_count, negative_count, uncertain_count))
# -
sentiments


