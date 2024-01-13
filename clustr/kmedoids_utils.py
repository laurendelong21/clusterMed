import os.path as osp
from typing import List
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from clustr.utils import dict_to_json
from collections import OrderedDict


def calculate_kmedoids(data_mat,
                       min_k: int = 1,
                       max_k: int = 10):
    """Gets an array of costs per K
    :param data_mat: the numpy array containing the sample features
    :param min_k: the minimum k clusters to test
    :param max_k: the maximum k clusters to test
    """
    cost = OrderedDict()
    sil_scores = OrderedDict()
    for cluster in range(min_k, max_k+1):
        cobj = KMedoids(n_clusters=cluster, random_state=0, metric='cosine').fit(data_mat)
        print('Cluster initiation: {}'.format(cluster))
        labels = cobj.labels_
        cost[cluster] = cobj.inertia_
        try:
            sil_scores[cluster] = silhouette_score(data_mat, labels, metric='hamming')
        except ValueError:
            sil_scores[cluster] = -1

    return cost, sil_scores


def fit_kmedoids(data_mat,
                 out_folder: str,
                 cgrps: List[str],
                 k: int = 10):
    """
    Fits KMedoids model to data
    :param data_mat: the numpy array containing the sample features
    :param out_folder: the folder to which the figure files should be written.
    :param cgrps: an array of the condition groups being clustered
    :param k: the number k clusters
    :returns: the KMedoids model and the corresponding cluster labels
    """
    cobj = KMedoids(n_clusters=k, random_state=None, metric='cosine').fit(data_mat)
    labels = cobj.labels_
    db_score = davies_bouldin_score(data_mat, labels)
    ch_score = calinski_harabasz_score(data_mat, labels)
    sil_score = silhouette_score(data_mat, labels, metric='hamming')
    dict_to_json({'silhouette': sil_score,
        'davies_boulden': db_score,
        'calinski_harabasz': ch_score},
        osp.join(out_folder, 'scores.json'))
    # write centroids to file
    centroid_comorbidities = {}
    for count, cntrd in enumerate(cobj.cluster_centers_):
        centroid_comorbidities[count] = []
        for count2, m in enumerate(cntrd):
            if m == 1:
                centroid_comorbidities[count].append(cgrps[count2])
    dict_to_json(centroid_comorbidities, osp.join(out_folder, 'centroids.json'))
    return cobj, labels

