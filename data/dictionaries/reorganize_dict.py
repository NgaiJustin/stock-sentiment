# +
# download from https://sraf.nd.edu/loughranmcdonald-master-dictionary/

import pandas as pd
# -

df = pd.read_csv('lmm_dict.csv')

relavant_cols = df[(df['Word Proportion']) > 1e-7][['Word', 'Positive', 'Negative', 'Uncertainty']]
relavant_cols['Positive'] = (relavant_cols['Positive'] > 0)
relavant_cols['Negative'] = (relavant_cols['Negative'] > 0)
relavant_cols['Uncertainty'] = (relavant_cols['Uncertainty'] > 0)

reindexed = relavant_cols.set_index('Word')

reindexed.to_parquet('reformatted_masterdict.parquet')


