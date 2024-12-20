import pandas as pd
import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cdist

exps = [(1/5), (1/1.3), 1, 2, 5]

# ---Preparazione (da modificare)---
df1 = pd.read_csv("dataset.csv")
df = df1.drop(columns=["age_flag", "age_radius", "interest_flag", "gender",
                       "distance_km", "gender_text", "gender_partner_text",
                       "gender_partner", "gender_partner_him", "gender_partner_her", "gender_partner_them"])
search = df.sample()

search["age"] = search["age_o"]
search["sports"] = search["sports_partner"]
search["tvsports"] = search["tvsports_partner"]
search["exercise"] = search["exercise_partner"]
search["dining"] = search["dining_partner"]
search["hiking"] = search["hiking_partner"]
search["gaming"] = search["gaming_partner"]
search["clubbing"] = search["clubbing_partner"]
search["reading"] = search["reading_partner"]
search["tv"] = search["tv_partner"]
search["theater"] = search["theater_partner"]
search["movies"] = search["movies_partner"]
search["music"] = search["music_partner"]
search["shopping"] = search["shopping_partner"]
search["yoga"] = search["yoga_partner"]
weights = search[['attractive_important', 'sincere_important',
                  'intelligence_important', 'funny_important',
                  'ambition_important']].to_numpy(dtype=np.uint8)[0]

search = search.drop(columns=(["age_o"] + list(df.filter(regex='.*partner$')) + list(df.filter(regex='.*important$'))))
search.iloc[:, 16:21] = 0

df = df[df["ID"] != search.iloc[0, 0]]
IDs = df["ID"].to_list()
IDs.append(search.iloc[0,0])
IDs = np.array(IDs)
df = df.drop(columns=(["age_o", "ID"] + list(df.filter(regex='.*partner$')) + list(df.filter(regex='.*important$'))))
search = search.drop(columns=["ID"])
search = search.to_numpy()[0]
X = df.to_numpy()
X = np.vstack((X,search))

# ---Clustering---
clustering = HDBSCAN(min_cluster_size=6, n_jobs=-1, store_centers="centroid", allow_single_cluster=True)
clustering.fit(X[:, np.r_[0:15, 20:23]])

# re-assign noisy points
centroids = clustering.centroids_
noisy = X[clustering.labels_ == -1]
noisy = noisy[:,np.r_[0:15, 20:23]]
distmat = cdist(noisy, centroids)
idxs = np.argmin(distmat, axis=1)
clustering.labels_[clustering.labels_ == -1] = idxs

# filtering
X = X[clustering.labels_ == clustering.labels_[-1]]
IDs = IDs[clustering.labels_ == clustering.labels_[-1]]

# ---Variable deformation---
for cnt, i in enumerate(range(15,20)):
    X[:-1,i] = np.int64(np.float_power((11-X[:-1,i]), exps[weights[cnt]-1]))

# ---Nearest Neighbors---
nn = NearestNeighbors(n_jobs=-1)
nn.fit(X)
dsts, idxs = nn.kneighbors(X[-1].reshape(1,-1), return_distance=True, n_neighbors=6)

# ---Result---
with pd.option_context('display.max_columns', None):
    print("ID punto di ricerca:",IDs[-1])
    print("ID dei punti simili:",IDs[idxs[0, 1:]])
    print("Punto di ricerca:",df1[df1["ID"] == IDs[-1]])
    for i in range(1, idxs.shape[1]):
        print(f"{i}° punto più simile:",df1[df1["ID"] == IDs[idxs[0,i]]])