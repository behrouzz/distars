import numpy as np
import pandas as pd
from hypatie.transform import angular_separation, sph2car
import pickle
from distars import dist_array, plx2car, nearest_pairs


df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')
df = df[df['dist'].notnull()]

pos_sph = df[['ra', 'dec', 'dist']].values
pos_car = sph2car(pos_sph)
df['x'], df['y'], df['z'] = pos_car.T

d = dist_array(df[['x','y','z']].values)

pairs, dists = nearest_pairs(d, below=0.5)

for i in range(len(pairs)):
    ind1, ind2 = pairs[i]
    print(list(df.iloc[[ind1,ind2]]['source_id']), ':', dists[i])

