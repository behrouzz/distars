import pandas as pd
from distars import gaia_distmat, n_neighbors


df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')
df = df[df['dist'].notnull()]

d = gaia_distmat(df, ['ra','dec','dist'])

df['n_0.1'] = n_neighbors(d, d_max=0.1)
df['n_0.2'] = n_neighbors(d, d_max=0.2)
df['n_0.3'] = n_neighbors(d, d_max=0.3)
df['n_0.4'] = n_neighbors(d, d_max=0.4)
df['n_0.5'] = n_neighbors(d, d_max=0.5)
df['n___1'] = n_neighbors(d, d_max=1)
df['n___2'] = n_neighbors(d, d_max=2)
df['n___3'] = n_neighbors(d, d_max=3)
df['n___4'] = n_neighbors(d, d_max=4)
df['n___5'] = n_neighbors(d, d_max=5)



cols = ['n_0.1', 'n_0.2', 'n_0.3', 'n_0.4', 'n_0.5',
        'n___1', 'n___2', 'n___3', 'n___4', 'n___5']


for col in cols:
    
    print(f"NEIGHBORHOOD IS DEFINED AS {col.split('_')[-1]} PC")
    print()
    aa = df[col].value_counts().to_frame('stars')
    aa.index.name = 'n_neighbors'
    aa['ratio'] = aa['stars'] / len(df)
    print(aa)
    print('-'*70)
