import numpy as np
import pandas as pd
from hypatie.transform import angular_separation, sph2car
import pickle
from distars import dist_array, plx2car, nearest_pairs


df = pd.read_csv('data/The_Persian_1deg.csv')
df = plx2car(df, col_names=['ra','dec','plx_value'])

d = dist_array(df[['x','y','z']].values)

pairs, dists = nearest_pairs(d, below=1)

for i in range(len(pairs)):
    ind1, ind2 = pairs[i]
    print(list(df.iloc[[ind1,ind2]]['main_id']), ':', dists[i])


#Gaia DR3 6482236359934227456
#Gaia DR3 6482236261151268864
