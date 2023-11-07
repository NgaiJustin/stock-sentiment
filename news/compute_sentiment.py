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

# +
import random
import math
from pathlib import Path

import pandas as pd
from bitarray import bitarray
from nltk import tokenize
from tqdm.notebook import tqdm

from dict_analyze_news import silly_dict_sentiment
from nltk_analyze_news import nltk_sentiment

data_root = Path('../data/')
articles_path = data_root / "news-data" / "all-the-news" / "year-2016-month-1.0.parquet"
articles = pd.read_parquet(articles_path)
# -

articles

articles.sort_values('date', inplace=True)


# ## bloom filter implementation

class BloomFilter(object):
    def __init__(self, size, hash_count):
        """
        size: size of bit array
        hash_count: number of hash functions to use
        """
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.hash_param = []
        i=0
        while i<hash_count:
            a=random.randint(1,9999)
            b=random.randint(1,9999)
            p = self.generate_large_prime(30)
            self.hash_param.append((a,b,p))
            i+=1

    def generate_large_prime(self, bit_size):
        def is_prime(number):
            if number % 2 == 0:
                return False

            for i in range(3, int(math.sqrt(number)) + 1, 2):
                if number % i == 0:
                    return False
            return True
        
        random_number = 0
        while not is_prime(random_number):
            random_number = random.getrandbits(bit_size)
        return random_number


    def calculate_hash(self,item,hash_params):
        item_val = (hash_params[0]*item + hash_params[1])%hash_params[2]
        return item_val

    def add(self, item):
        """
        Add an item to the filter
        """
        for i in range(self.hash_count):
            index = self.calculate_hash(item, self.hash_param[i]) % self.size
            self.bit_array[index] = 1

    def lookup(self, item):
        """
        Check for existence of an item in filter
        """
        for i in range(self.hash_count):
            index = self.calculate_hash(item, self.hash_param[i]) % self.size
            if self.bit_array[index] == 0:
                return False 
        return True
    
    def clear(self):
        self.bit_array.clear()
        self.bit_array.fill(self.size)

    def __contains__(self, item):
        return self.lookup(item)

# +
ticker = 'AAPL'

out_path = data_root / "out" / "AAPL-2016-01-sentiment_updates.parquet"
out_path.parent.mkdir(parents=True, exist_ok=True)
keywords = ["Apple", "MacBook", "Macbook", "iPhone"]

records = []
sentiment_total = 0
for article in tqdm(list(articles.itertuples())[:10 ** 4]):
    words = set()
    if article.article:
        for token in tokenize.word_tokenize(article.article):
            words.add(token)
        for kword in keywords:
            if kword in words:
                silly_sentiment = silly_dict_sentiment(article.article)
                better_sentiment = nltk_sentiment(article.article)
                
                records.append((article.date, sentiment_total, *silly_sentiment, *better_sentiment))

                sentiment_total += better_sentiment[0]  # this is "future information"
                sentiment_total -= better_sentiment[1]
                break
# -

pd.DataFrame.from_records(records, columns=[
    'time', 'cumulative_sentiment', 'silly_pos', 'silly_neg',
    'silly_risk', 'better_pos', 'better_neg', 'better_neutral'
]).to_parquet(out_path)

# ## test performance

keywords = {
    'AAPL': ["Apple", "MacBook", "Macbook", "iPhone"],
    'JNJ': ["Covid-19", "vaccine", "Johnson"]
}

ans = 0
for article in tqdm(list(articles.itertuples())[:10 ** 4]):
    words = set()
    if article.article:
        for token in tokenize.word_tokenize(article.article):
            words.add(token)
        for ticker, kwords in keywords.items():
            for kword in kwords:
                if kword in words:
                    ans += 1
                    break
ans

ans = 0
for article in tqdm(list(articles.itertuples())[:10 ** 4]):
    bf = BloomFilter(2 ** 20, 5)
    if article.article:
        for token in tokenize.word_tokenize(article.article):
            bf.add(hash(token))
        for ticker, kwords in keywords.items():
            for kword in kwords:
                if hash(kword) in bf:
                    ans += 1
                    break
ans




