import pandas as pd
from nltk import tokenize
from tqdm.notebook import tqdm
from pathlib import Path

# +
data_root = Path('../data/')
articles_path = data_root / "news-data" / "all-the-news" / "year-2016-month-1.0.parquet"
dictionary_path = data_root / "news-data" / "sentiment-dictionaries" / "master_dict.parquet"

articles = pd.read_parquet(articles_path)
dictionary = pd.read_parquet(dictionary_path)


# -

def silly_dict_sentiment(article):
    tokens = tokenize.word_tokenize(article)
    positive_count = 0
    negative_count = 0
    uncertain_count = 0
    count = 0
    for token in tokens:
        token = token.upper()
        if token in dictionary.index:
            count += 1
            positive_count += dictionary.loc[token]['Positive']
            negative_count += dictionary.loc[token]['Negative']
            uncertain_count += dictionary.loc[token]['Uncertainty']
    return positive_count / count, negative_count / count, uncertain_count / count
