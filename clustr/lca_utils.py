from scipy import stats
from clustr.lca import LCA
from clustr.utils import dict_to_json
import os.path as osp
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from collections import OrderedDict


def select_lca_model(data_mat,
                     out_folder: str,
                     min_k: int = 2,
                     max_k: int = 10):
    """Generates a plot of BIC per k number of clusters for model selection"""
    ks = [k for k in range(min_k, max_k + 1)]
    bics = OrderedDict()
    for k in ks:
        lca = LCA(n_components=k, tol=10e-4, max_iter=1000)
        lca.fit(data_mat)
        bics[k] = lca.bic
    # Plot the BIC per K
    ks = list(bics.keys())
    bic_values = list(bics.values())
    _, ax = plt.subplots(figsize=(15, 5))
    ax.plot(ks, bic_values, linewidth=3)
    ax.grid(True)
    ax.set_title("Model Selection Using BIC")
    ax.set_xlabel("k clusters")
    ax.set_ylabel("Bayesian Information Criterion (BIC)")
    plt.savefig(osp.join(out_folder, 'model_selection.png'), dpi=300, bbox_inches='tight')

    return dict(bics)


def get_lca_clusters(data_mat,
                     out_folder: str,
                     k: int = 10):
    """Generates clustering results with LCA
    :param data_mat: the numpy array containing the sample features
    :param out_folder: the folder to which the figure files should be written.
    :param k: the number k clusters
    """
    lca = LCA(n_components=k, tol=10e-4, max_iter=1000)
    lca.fit(data_mat)
    labels = lca.predict(data_mat)
    db_score = davies_bouldin_score(data_mat, labels)
    ch_score = calinski_harabasz_score(data_mat, labels)
    sil_score = silhouette_score(data_mat, labels, metric='hamming')
    dict_to_json({'silhouette': sil_score,
                  'davies_boulden': db_score,
                  'calinski_harabasz': ch_score},
                 osp.join(out_folder, 'scores.json'))
    # TODO: use lca.predict_proba(data_mat) to get probabilities as well?
    return lca, labels
