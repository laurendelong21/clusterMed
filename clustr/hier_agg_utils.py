from sklearn.cluster import AgglomerativeClustering
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
    model.fit(ssd.squareform(ssd.pdist(data_mat, metric=metric)))
    labels = model.labels_
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
