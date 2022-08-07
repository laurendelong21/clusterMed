import os.path as osp
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from clustr.utils import dict_to_json
from clustr.constants import KMEDOIDS_RESULTS


def calculate_kmedoids(dfMatrix, max_k=10):
    """Gets an array of costs per K"""
    cost = []
    for cluster in range(1, max_k):
        try:
            cobj = KMedoids(n_clusters=cluster, random_state=0, metric='cosine').fit(dfMatrix)
            cost.append(cobj.inertia_)
            print('Cluster initiation: {}'.format(cluster))
        except:
            break

    return cost


def fit_kmedoids(data_mat,
                 cgrps,
                 k: int = 10):
    """TODO"""
    cobj = KMedoids(n_clusters=k, random_state=0, metric='cosine').fit(data_mat)
    labels = cobj.labels_
    db_score = davies_bouldin_score(data_mat, labels)
    ch_score = calinski_harabasz_score(data_mat, labels)
    dict_to_json({  # 'silhouette': sil_score,
        'davies_boulden': db_score,
        'calinski_harabasz': ch_score},
        osp.join(KMEDOIDS_RESULTS, 'scores.json'))
    # write centroids to file
    centroid_comorbidities = {}
    for count, cntrd in enumerate(cobj.cluster_centers_):
        centroid_comorbidities[count] = []
        for count2, m in enumerate(cntrd):
            if m == 1:
                centroid_comorbidities[count].append(cgrps[count2])
    dict_to_json(centroid_comorbidities, osp.join(KMEDOIDS_RESULTS, 'centroids.json'))
    return cobj, labels

