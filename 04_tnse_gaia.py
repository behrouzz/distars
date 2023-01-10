import numpy as np
import pandas as pd
from hypatie.transform import sph2car
from sklearn.manifold import TSNE
import plotly.graph_objects as go
from distars import plx2car, create_hovertext


df = pd.read_csv('data/The_Persian_1deg_gaia3.csv')
df = df[df['dist'].notnull()]
pos_sph = df[['ra', 'dec', 'dist']].values
pos_car = sph2car(pos_sph)
df['x'], df['y'], df['z'] = pos_car.T

pos2d = TSNE(n_components=2,
             learning_rate='auto',
             init='random',
             perplexity=3).fit_transform(df[['x','y','z']].values)

x, y = pos2d.T

data = go.Scatter(
    x=x, y=y,
    #mode='markers',
    mode='markers',#+text',
    #hovertext=create_hovertext(df),
    hoverinfo='text',
    text=df['source_id'],
    textposition="bottom right",
                  )

fig = go.Figure(data=data)

fig.update_layout(title='', height=800, width=800)

fig.write_html("data/file.html")
