from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from clustr.utils import dict_to_json
from clustr.startup import logger
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd
import matplotlib.pyplot as plt
import os.path as osp
import sys


sys.setrecursionlimit(100000)


def get_agg_clusters(data_mat,
                     out_folder: str,
                     metric: str = 'hamming',
                     linkage: str = 'complete'):
    """Gets the hierarchical agglomerative clustering results for a given matrix
    :param data_mat: the numpy array containing the sample features
    :param out_folder: the folder to which the figure files should be written.
    :param metric: the metric type used for clustering; default is hamming distance
    :param linkage: linkage method; default is complete
    """
    logger.info(f'Performing agglomerative hierarchical clustering with {linkage} linkage and the {metric} metric.')
    model = AgglomerativeClustering(n_clusters=10, affinity='precomputed', linkage=linkage)
    model.fit(ssd.squareform(ssd.pdist(data_mat, metric=metric)))
    labels = model.labels_
    sil_score = silhouette_score(data_mat, labels, metric='hamming')
    db_score = davies_bouldin_score(data_mat, labels)
    ch_score = calinski_harabasz_score(data_mat, labels)
    dict_to_json({'silhouette': sil_score,
                  'davies_boulden': db_score,
                  'calinski_harabasz': ch_score},
                 osp.join(out_folder, 'scores.json'))
    logger.info(f'Finished agglomerative hierarchical clustering with {linkage} linkage and the {metric} metric.')
    return model, labels


def plot_dendrogram(data_mat,
                    out_folder: str,
                    metric: str = 'hamming',
                    linkage: str = 'complete'):
    """Plots and saves the corresponding dendrogram for the hierarchical agglomerative clustering
    :param data_mat: the numpy array containing the sample features
    :param out_folder: the folder to which the figure files should be written.
    :param metric: the metric type used for clustering; default is hamming distance
    :param linkage: linkage method; default is complete
    """
    logger.info(f'Plotting the dendrogram for {linkage} linkage and the {metric} metric.')
    dendrogram = sch.dendrogram(sch.linkage(data_mat,
                                            metric=metric,
                                            method=linkage))
    plt.savefig(osp.join(out_folder, 'dendrogram.png'), dpi=300, bbox_inches='tight')
