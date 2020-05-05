import pandas as pd

from sklearn.cluster import KMeans
from sklearn.linear_model import LassoLarsIC


def compute_clusters(df, method='kmeans', k=2, return_score=False):
    df = df.fillna(0)

    columns = [col for col in df.columns if col != 'PatientID']

    x = df[columns].values

    if method == 'kmeans':
        kmeans = KMeans(n_clusters=k, random_state=3)
        kmeans = kmeans.fit(x)
        clusters = kmeans.predict(x)
    else:
        raise ValueError('Invalid method.')

    result = pd.concat([df[['PatientID']].reset_index(drop=True), pd.DataFrame(clusters, columns=['Cluster'])], axis=1)
    if return_score:
        return result, estimate_variance(method, kmeans, x)  # compute_bic(x, clusters)
    else:
        return result


import numpy as np
from scipy.spatial.distance import cdist, pdist


# Taken from Caban code shared from Peter
def estimate_variance(cluster_alg, model, x):
    if cluster_alg == 'agglomerative':
        return model.n_leaves_
    elif cluster_alg == 'spectral':
        return 1

    k_euclid = cdist(x, model.cluster_centers_, 'euclidean')
    dist = np.min(k_euclid, axis=1)

    # Total within-cluster sum of squares
    wcss = sum(dist ** 2)

    # The total sum of squares
    tss = sum(pdist(x) ** 2) / x.shape[0]

    # The between-cluster sum of squares
    bss = tss - wcss

    return bss / tss * 100


def compute_bic(x, clusters):
    # Compute the BIC
    model_bic = LassoLarsIC(criterion='bic')
    model_bic.fit(x, clusters)

    return model_bic.alpha_

    # Compute the AIC
    # model_aic = LassoLarsIC(criterion='aic')
    # model_aic.fit(sub_x, model.labels_)

    # Compute the estimated variance for the elbow method
    # variance = estimate_variance(cluster_alg, model, sub_x)
