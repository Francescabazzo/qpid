import pandas as pd
import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cdist
import sys
sys.path.append('./utils')
from logger import log

def get_matches(df1:pd.DataFrame, search:pd.DataFrame) -> list:
    deformation_exps = [(1/5), (1/1.3), 1, 2, 5]
    is_distance_important = bool(search['distance_flag_other'].values[0])
    log(f"get_matches(): working with {df1.shape[0]} candidates, is_distance_important: {is_distance_important}")
    unnecessary = ["email", "name", "bio", "gender", "gender_other", "age_flag_other",
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

    log(f"get_matches(): candidates after clustering: {X.shape[0]-1}")

    # ---Nearest Neighbors---
    nn = NearestNeighbors(n_jobs=-1)
    selected_features = np.r_[0:23] if is_distance_important else np.r_[0,3:23]
    nn.fit(X[:-1, selected_features])
    idxs = nn.kneighbors(X[-1, selected_features].reshape(1,-1), return_distance=False, n_neighbors=5)

    # ---Result---
    return IDs[idxs[0]]

def calculate_scores(candidates:pd.DataFrame, search:pd.DataFrame) -> np.ndarray:
    # some reference indexes (numpy notation):
    # 8:13 => attractiveness, sincerity, intelligence, ambition
    # 13:28 => personal interests
    # 34:39 => importance of attractivenes, ...
    # 40:55 => searched interests
    log(f"calculate_scores(): calculating scores for {candidates.shape[0]} candidates")
    c = candidates.to_numpy()
    s = search.to_numpy()[0]
    scores = np.absolute(c[:,8:8+20]-s[np.r_[34:34+5, 40:40+15]])
    scores[:,:5] = c[:,8:8+5]
    scores[:,5:] = 10-scores[:,5:]
    score_weights = np.ones(scores.shape[1])
    score_weights[:5] = s[34:34+5]
    scores = np.average(scores, axis=1, weights=score_weights)*10
    return scores