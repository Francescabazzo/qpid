import pandas as pd
import numpy as np
from sklearn.preprocessing import robust_scale
from sklearn.cluster import HDBSCAN
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cdist

exps = [(1/5), (1/1.3), 1, 1.3, 5]

# ---Preparazione (da modificare)---
df1 = pd.read_csv("dataset.csv")
df = df1[0:8637]
df = df.drop(columns=["gender", "age_interval", "gender_text", "gender_partner_text"])

search = df.sample()

search["age"] = search["age_o"]
weights = search.iloc[:, 2:7].to_numpy()[0]
weights[weights > 4] = 4
search = search.drop(columns=[
    "attractive_important", "sincere_important", "intellicence_important",
    "funny_important", "ambtition_important", "age_o"
    ])
search.iloc[:, 2:7] = 0

df = df.drop(index=search.iloc[0, 0])
IDs = df["ID"].to_list()
IDs.append(search.iloc[0,0])
IDs = np.array(IDs)
df = df.drop(columns=[
    "attractive_important", "sincere_important", "intellicence_important",
    "funny_important", "ambtition_important", "age_o", "ID"
])
search = search.drop(columns=["ID"])
search = search.to_numpy()[0]

X = df.to_numpy()
X = np.vstack((X,search))

# ---Clustering---
clustering = HDBSCAN(min_cluster_size=5, n_jobs=-1, store_centers="medoid", allow_single_cluster=True)
clustering.fit(X[:, np.r_[0, 6:26]])

medoids = clustering.medoids_
noisy = X[clustering.labels_ == -1]
noisy = noisy[:,np.r_[0,6:26]]
distmat = cdist(noisy, medoids)
idxs = np.argmin(distmat, axis=1)
clustering.labels_[clustering.labels_ == -1] = idxs

X = X[clustering.labels_ == clustering.labels_[-1]]
IDs = IDs[clustering.labels_ == clustering.labels_[-1]]

# ---Deformazione variabili---
for i in range(1,6):
    X[:,i] = np.int64(np.float_power((11-X[:,i]), exps[int(weights[i-1])]))
X[-1,:] = 0

# ---Scaling---
X = robust_scale(X)

# ---Nearest Neighbors---
nn = NearestNeighbors(n_jobs=-1)
nn.fit(X[:-1])
dsts, idxs = nn.kneighbors(X[-1].reshape(1,-1), return_distance=True)

# ---Result---
result = IDs[idxs[0]]

with pd.option_context('display.max_columns', None):
    print("ID punto di ricerca:",IDs[-1])
    print("ID dei punti simili:",IDs[idxs[0]])
    print("Punto di ricerca:",df1[df1["ID"] == IDs[-1]])
    for i in range(idxs.shape[1]):
        print(f"{i+1}° punto più simile:",df1[df1["ID"] == IDs[idxs[0,i]]])