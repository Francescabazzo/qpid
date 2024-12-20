import pandas as pd
import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cdist

def get_matches(df1:pd.DataFrame, search:pd.DataFrame) -> list:
    exps = [(1/5), (1/1.3), 1, 2, 5]

    # ---Preparazione (da modificare)---
    df = df1.drop(columns=["name", "bio", "gender", "gender_other", "age_flag_other",
                           "age_radius_other", "distance_flag_other", "distance_km_other",
                           "same_interests"])

    search["age"] = search["age_other"]
    search["sports"] = search["sports_other"]
    search["tv_sports"] = search["tv_sports_other"]
    search["exercise"] = search["exercise_other"]
    search["dining"] = search["dining_other"]
    search["hiking"] = search["hiking_other"]
    search["gaming"] = search["gaming_other"]
    search["clubbing"] = search["clubbing_other"]
    search["reading"] = search["reading_other"]
    search["tv"] = search["tv_other"]
    search["theater"] = search["theater_other"]
    search["movies"] = search["movies_other"]
    search["music"] = search["music_other"]
    search["shopping"] = search["shopping_other"]
    search["yoga"] = search["yoga_other"]
    weights = search[['attractiveness_important', 'sincerity_important',
                        'intelligence_important', 'funniness_important',
                        'ambition_important']].to_numpy(dtype=np.uint8)[0]

    search = search.drop(columns=(["age_other"] + list(df.filter(regex='.*other$')) + list(df.filter(regex='.*important$'))))
    search.iloc[:, 4:9] = 0

    df = df[df["ID"] != search.iloc[0, 0]]
    IDs = df["ID"].to_list()
    IDs.append(search.iloc[0,0])
    IDs = np.array(IDs)
    df = df.drop(columns=(["age_other", "ID"] + list(df.filter(regex='.*other$')) + list(df.filter(regex='.*important$'))))
    search = search.drop(columns=["ID"])
    search = search.to_numpy()[0]
    X = df.to_numpy()
    X = np.vstack((X,search))

    # ---Clustering---
    clustering = HDBSCAN(min_cluster_size=6, n_jobs=-1, store_centers="centroid", allow_single_cluster=True)
    clustering.fit(X[:, np.r_[5:8, 9:23]])

    # re-assign noisy points
    centroids = clustering.centroids_
    noisy = X[clustering.labels_ == -1]
    noisy = noisy[:,np.r_[5:8, 9:23]]
    distmat = cdist(noisy, centroids)
    idxs = np.argmin(distmat, axis=1)
    clustering.labels_[clustering.labels_ == -1] = idxs

    # filtering
    X = X[clustering.labels_ == clustering.labels_[-1]]
    IDs = IDs[clustering.labels_ == clustering.labels_[-1]]

    # ---Variable deformation---
    for cnt, i in enumerate(range(4,9)):
        X[:-1,i] = np.int64(np.float_power((11-X[:-1,i]), exps[weights[cnt]-1]))

    # ---Nearest Neighbors---
    nn = NearestNeighbors(n_jobs=-1)
    nn.fit(X)
    idxs = nn.kneighbors(X[-1].reshape(1,-1), return_distance=False, n_neighbors=6)

    # ---Result---
    return IDs[idxs[0, 1:]]