import numpy as np
import pandas as pd
from hypatie.transform import sph2car
from distars import distmat, nearest_pairs


df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')
df = df[df['dist'].notnull()]

pos_sph = df[['ra', 'dec', 'dist']].values
pos_car = sph2car(pos_sph)
df['x'], df['y'], df['z'] = pos_car.T

d = distmat(df[['x','y','z']].values, diag_zero=False)

pairs, dists = nearest_pairs(d, below=0.4)

for i in range(len(pairs)):
    ind1, ind2 = pairs[i]
    print(list(df.iloc[[ind1,ind2]]['source_id']), ':', dists[i])
