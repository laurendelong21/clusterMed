from scipy import stats
from clustr.lca import LCA
from clustr.constants import LCA_RESULTS
from clustr.utils import dict_to_json
import os.path as osp
import matplotlib.pyplot as plt
import scipy.spatial.distance as ssd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


def select_lca_model(data_mat,
                     min_k: int = 2,
                     max_k: int = 10):
    """Generates a plot of BIC per k number of clusters for model selection"""
    ks = [k for k in range(min_k, max_k + 1)]
    bics = []
    for k in ks:
        lca = LCA(n_components=k, tol=10e-4, max_iter=1000)
        lca.fit(data_mat)
        bics.append(lca.bic)
    # Plot the BIC per K
    _, ax = plt.subplots(figsize=(15, 5))
    ax.plot(ks, bics, linewidth=3)
    ax.grid(True)
    ax.set_title("Model Selection Using BIC")
    ax.set_xlabel("k clusters")
    ax.set_ylabel("Bayesian Information Criterion (BIC)")
    plt.savefig(osp.join(LCA_RESULTS, 'model_selection.png'), dpi=300, bbox_inches='tight')


def get_lca_clusters(data_mat,
                     k: int = 10,
                     metric: str = 'hamming'):
    """Generates clustering results with LCA"""
    lca = LCA(n_components=k, tol=10e-4, max_iter=1000)
    lca.fit(data_mat)
    labels = lca.predict(data_mat)
    #dist_mat = ssd.squareform(ssd.pdist(data_mat, metric=metric))
    #sil_score = silhouette_score(dist_mat, labels, metric='precomputed')
    db_score = davies_bouldin_score(data_mat, labels)
    ch_score = calinski_harabasz_score(data_mat, labels)
    dict_to_json({# 'silhouette': sil_score,
                  'davies_boulden': db_score,
                  'calinski_harabasz': ch_score},
                 osp.join(LCA_RESULTS, 'scores.json'))
    # TODO: use lca.predict_proba(data_mat) to get probabilities as well?
    return lca, labels
