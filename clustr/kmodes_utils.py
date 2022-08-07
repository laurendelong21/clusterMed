from kmodes.kmodes import KModes
from clustr.constants import KMODES_RESULTS
import os.path as osp
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from clustr.utils import dict_to_json
# Import module for data visualization
from plotnine import *
import plotnine
# Data visualization with matplotlib
import matplotlib.pyplot as plt
import pandas as pd
# Use the theme of ggplot
plt.style.use('ggplot')


def calculate_kmodes(dfMatrix, max_k=10, distance_metric='Huang'):
    """Gets an array of costs per K"""
    cost = []
    for cluster in range(1, max_k):
        kmodes = KModes(n_jobs=-1, n_clusters=cluster, init=distance_metric, random_state=0)
        kmodes.fit_predict(dfMatrix)
        cost.append(kmodes.cost_)
        print('Cluster initiation: {}'.format(cluster))

    return cost


def plot_ks(cost, max_k=10):
    """Plots the respective costs per K"""
    df_cost = pd.DataFrame({'Cluster': range(1, max_k), 'Cost': cost})  # Data viz
    plotnine.options.figure_size = (8, 4.8)
    (
            ggplot(data=df_cost) +
            geom_line(aes(x='Cluster',
                          y='Cost')) +
            geom_point(aes(x='Cluster',
                           y='Cost')) +
            geom_label(aes(x='Cluster',
                           y='Cost',
                           label='Cluster'),
                       size=max_k,
                       nudge_y=1000) +
            labs(title='Optimal number of clusters for K Modes method') +
            xlab('Number of Clusters k') +
            ylab('Cost') +
            theme_minimal()
    )


def fit_kmodes(data_mat,
               cgrps,
               k: int = 10):
    """TODO"""
    kmodes = KModes(n_jobs=-1, n_clusters=k, init='Huang', random_state=0)
    kmodes.fit_predict(data_mat)
    labels = kmodes.labels_
    db_score = davies_bouldin_score(data_mat, labels)
    ch_score = calinski_harabasz_score(data_mat, labels)
    dict_to_json({  # 'silhouette': sil_score,
        'davies_boulden': db_score,
        'calinski_harabasz': ch_score},
        osp.join(KMODES_RESULTS, 'scores.json'))
    # write centroids to file
    centroid_comorbidities = {}
    for count, cntrd in enumerate(kmodes.cluster_centroids_):
        centroid_comorbidities[count] = []
        for count2, m in enumerate(cntrd):
            if m == 1:
                centroid_comorbidities[count].append(cgrps[count2])
    dict_to_json(centroid_comorbidities, osp.join(KMODES_RESULTS, 'centroids.json'))
    return kmodes, labels
