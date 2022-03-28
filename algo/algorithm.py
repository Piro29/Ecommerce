# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:27:24 2020

@author: PoSiTiVe
"""

from pandas import read_csv, merge
from numpy import arange
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


df = read_csv("D:/python/ecommerce/algo/data.csv")
df["n"] = 1
table = df.pivot_table(index=["user_id"], columns=["category"], values="n")
table = table.fillna(0).reset_index()
cols = table.columns[1:]
cluster = KMeans(n_clusters=5)
table["cluster"] = cluster.fit_predict(table[table.columns[2:]])
pca = PCA(n_components=5)
table['x'] = pca.fit_transform(table[cols])[:, 0]
table['y'] = pca.fit_transform(table[cols])[:, 1]
table = table.reset_index()
customer_clusters = table[["user_id", "cluster", "x", "y"]]
final = merge(df, customer_clusters)
user_data = table[["user_id", "cluster"]]

x = table['x']
y = table['y']

plt.plot(x, y, linestyle='none', label="stars", color="green",
         marker="*")

user_data.to_csv("D:/python/ecommerce/algo/user_cluster.csv" , index = False)


cluster_no=user_data[(user_data['user_id'] == 34)].iloc[0]['cluster']