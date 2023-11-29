from kmodes.kmodes import KModes
from kmodes.util.dissim import jaccard_dissim_label
from typing import List
import os.path as osp
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from clustr.utils import dict_to_json
import matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict


def calculate_kmodes(dfMatrix,
                     min_k=1,
                     max_k=10,
                     distance_metric='Huang'):
    """Gets an array of costs per K"""
    cost = OrderedDict()
    sil_scores = OrderedDict()
    for cluster in range(min_k, max_k+1):
        print('Cluster initiation: {}'.format(cluster))
        kmodes = KModes(n_jobs=-1, n_clusters=cluster, init=distance_metric, cat_dissim=jaccard_dissim_label,
                         n_init=1, random_state=0)
        kmodes.fit_predict(dfMatrix)
        labels = kmodes.labels_
        cost[cluster] = kmodes.cost_
        try:
            sil_scores[cluster] = silhouette_score(dfMatrix, labels, metric='jaccard')
        except ValueError:
            sil_scores[cluster] = -1

    return cost, sil_scores


def fit_kmodes(data_mat,
               out_folder: str,
               cgrps: List[str],
               k: int = 10):
    """Fits KModes model to data
    :param data_mat: the numpy array containing the sample features
    :param out_folder: the folder to which the figure files should be written.
    :param cgrps: an array of the condition groups being clustered
    :param k: the number k clusters
    :returns: the KModes model and the corresponding cluster labels
    """
    kmodes = KModes(n_jobs=-1, n_clusters=k, cat_dissim=jaccard_dissim_label,
                    init='Huang', random_state=0, n_init=1)
    kmodes.fit_predict(data_mat)
    labels = kmodes.labels_
    db_score = davies_bouldin_score(data_mat, labels)
    ch_score = calinski_harabasz_score(data_mat, labels)
    sil_score = silhouette_score(data_mat, labels, metric='jaccard')
    dict_to_json({'silhouette': sil_score,
        'davies_boulden': db_score,
        'calinski_harabasz': ch_score},
        osp.join(out_folder, 'scores.json'))
    # write centroids to file
    centroid_comorbidities = {}
    for count, cntrd in enumerate(kmodes.cluster_centroids_):
        centroid_comorbidities[count] = []
        for count2, m in enumerate(cntrd):
            if m == 1:
                centroid_comorbidities[count].append(cgrps[count2])
    dict_to_json(centroid_comorbidities, osp.join(out_folder, 'centroids.json'))
    return kmodes, labels
