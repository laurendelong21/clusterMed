from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from clustr.utils import dict_to_json
from clustr.constants import HIER_AGG_RESULTS
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd
import matplotlib.pyplot as plt
import os.path as osp


def get_agg_clusters(data_mat,
                     metric: str = 'hamming',
                     linkage: str = 'complete'):
    """Gets the hierarchical agglomerative clustering results for a given matrix
    :param data_mat: the numpy array containing the sample features
    :param metric: the metric type used for clustering; default is hamming distance
    :param linkage: linkage method; default is complete
    """
    model = AgglomerativeClustering(n_clusters=10, affinity='precomputed', linkage=linkage)
    dist_mat = ssd.squareform(ssd.pdist(data_mat, metric=metric))
    model.fit(dist_mat)
    labels = model.labels_
    sil_score = silhouette_score(dist_mat, labels, metric='precomputed')
    db_score = davies_bouldin_score(dist_mat, labels)
    ch_score = calinski_harabasz_score(dist_mat, labels)
    dict_to_json({'silhouette': sil_score,
                  'davies_boulden': db_score,
                  'calinski_harabasz': ch_score},
                 osp.join(HIER_AGG_RESULTS, 'scores.json'))
    return model, labels


def plot_dendrogram(data_mat,
                    outfl,
                    metric: str = 'hamming',
                    linkage: str = 'complete'):
    """Plots and saves the corresponding dendrogram for the hierarchical agglomerative clustering
    :param data_mat: the numpy array containing the sample features
    :param outfl: the file name to which the dendrogram picture should be saved
    :param metric: the metric type used for clustering; default is hamming distance
    :param linkage: linkage method; default is complete
    """
    dendrogram = sch.dendrogram(sch.linkage(data_mat,
                                            metric=metric,
                                            method=linkage))
    plt.savefig(osp.join(HIER_AGG_RESULTS, outfl), dpi=300, bbox_inches='tight')
