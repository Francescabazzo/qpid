import pandas as pd
import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cdist

deformation_exps = [(1/5), (1/1.3), 1, 2, 5]

def get_matches(df1:pd.DataFrame, search:pd.DataFrame) -> list:
    # ---Preparazione (da modificare)---
    unnecessary = ["name", "bio", "gender", "gender_other", "age_flag_other",
                   "age_radius_other", "distance_flag_other", "distance_km_other",
                   "same_interests"]
    df = df1.drop(columns=unnecessary)
    search = search.drop(columns=unnecessary)

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

    importants = ['attractiveness_important', 'sincerity_important',
                  'intelligence_important', 'funniness_important',
                  'ambition_important']
    characteristic_weights = search[importants].to_numpy(dtype=np.uint8)[0]

    search = search.drop(columns=(list(df.filter(regex=".*other$")) + list(df.filter(regex=".*important$"))))
    search.iloc[:, 4:9] = 1

    IDs = df["ID"].to_list()
    IDs.append(search.iloc[0,0])
    IDs = np.array(IDs, dtype=np.uint32)
    df = df.drop(columns=(["ID"] + list(df.filter(regex='.*other$')) + list(df.filter(regex='.*important$'))))
    search = search.drop(columns=["ID"])
    search = search.to_numpy()[0]
    X = df.to_numpy()
    X = np.vstack((X,search))

    # ---Variable deformation---
    for cnt, i in enumerate(range(3,8)):
        X[:-1,i] = np.int64(np.float_power((11-X[:-1,i]), deformation_exps[characteristic_weights[cnt]-1]))

    # ---Clustering---
    clustering = HDBSCAN(min_cluster_size=6, n_jobs=-1, store_centers="centroid", allow_single_cluster=True)
    clustering.fit(X[:,3:23])

    # re-assign noisy points
    centroids = clustering.centroids_
    noisy = X[clustering.labels_ == -1]
    noisy = noisy[:,3:23]
    distmat = cdist(noisy, centroids)
    idxs = np.argmin(distmat, axis=1)
    clustering.labels_[clustering.labels_ == -1] = idxs

    # filtering
    X = X[clustering.labels_ == clustering.labels_[-1]]
    IDs = IDs[clustering.labels_ == clustering.labels_[-1]]

    # ---Nearest Neighbors---
    nn = NearestNeighbors(n_jobs=-1)
    nn.fit(X[:-1])
    idxs = nn.kneighbors(X[-1].reshape(1,-1), return_distance=False, n_neighbors=5)
    
    """# ---Calculate Scores---
    # Variable de-deformation
    for cnt, i in enumerate(range(3,8)):
        X[:-1,i] = 11-np.float_power((X[:-1,i]), 1/deformation_exps[characteristic_weights[cnt]-1])

    scores = np.absolute(X[idxs[0]]-X[-1])[:,3:]
    scores[:,5:] = 10-scores[:,5:]
    score_weights = np.ones(scores.shape[1])
    score_weights[:5] = characteristic_weights
    scores = np.average(scores, axis=1, weights=score_weights)*10"""

    # ---Result---
    return IDs[idxs[0]]#, scores

def calculate_scores(candidates:pd.DataFrame, search:pd.DataFrame) -> np.ndarray:
    c = candidates.to_numpy()
    s = search.to_numpy()
    scores = np.absolute(c[:,7:7+20]-s[np.r_[33:33+5, 39:39+15]])
    scores[:,:5] = c[:,7:7+5]
    scores[:,5:] = 10-scores[:,5:]
    score_weights = np.ones(scores.shape[1])
    score_weights[:5] = s[33:33+5]
    scores = np.average(scores, axis=1, weights=score_weights)*10
    return scores