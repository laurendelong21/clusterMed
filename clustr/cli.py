import click
import logging
import os.path as osp
from memory_profiler import profile
from clustr.constants import PROCESSED_DATA
from clustr.constants import HIER_AGG_RESULTS, AGG_MEN, AGG_WOMEN
from clustr.constants import LCA_RESULTS, LCA_MEN, LCA_WOMEN
from clustr.constants import KMEDOIDS_RESULTS, KMEDOIDS_MEN, KMEDOIDS_WOMEN
from clustr.constants import KMODES_RESULTS, KMODES_MEN, KMODES_WOMEN
from clustr.utils import get_data, plot_morbidity_dist
from clustr.hier_agg_utils import get_agg_clusters, plot_dendrogram
from clustr.lca_utils import select_lca_model, get_lca_clusters
from clustr.kmedoids_utils import fit_kmedoids
from clustr.kmodes_utils import fit_kmodes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@click.group()
def cli():
    """Entry method for the CLI."""
    pass


@profile
@cli.command()
@click.option("-g", "--gender", type=str, default=None,
              help="denotes whether to take full data (None), only 'men', or only 'women'")
@click.option("-o", "--outfl", type=str, default=None,
              help="the file name to which the resulting file with cluster labels should be written")
@click.option("-m", "--metric", type=str, default='hamming',
              help="the metric to be used for clustering")
@click.option("-l", "--linkage", type=str, default='complete',
              help="the type of linkage to be used for clustering")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
def agg(gender: str,
        outfl: str,
        metric: str = 'hamming',
        linkage: str = 'complete',
        sample_frac: float = 1,
        drop_healthy: bool = False):
    """Hierarchical agglomerative clustering from command line
    :param gender: None, 'men', or 'women' denotes whether to take full data, only men, or only women.
    :param outfl: the file location at which the updated file with cluster labels should be saved
    :param metric: the metric type used for clustering; default is hamming distance
    :param linkage: linkage method; default is complete
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    """
    df, mat, pat_ids, labs, cgrps = get_data(sample_frac, drop_healthy, gender)
    if gender == 'men':
        foldr = AGG_MEN
    elif gender == 'women':
        foldr = AGG_WOMEN
    else:
        foldr = HIER_AGG_RESULTS
    model, labels = get_agg_clusters(mat, foldr, metric, linkage)
    plot_dendrogram(mat, foldr, metric, linkage)
    df['aggl_cluster_labels'] = labels
    df.to_csv(osp.join(foldr, outfl), sep='\t')
    plot_morbidity_dist(df, 'aggl_cluster_labels', foldr, 'agglomerative_hierarchical')


@cli.command()
@click.option("-g", "--gender", type=str, default=None,
              help="denotes whether to take full data (None), only 'men', or only 'women'")
@click.option("-mi", "--min_k", type=int, default=2,
              help="the minimum number k clusters to investigate")
@click.option("-ma", "--max_k", type=int, default=10,
              help="the maximum number k clusters to investigate")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
def lcaselect(gender: str,
              min_k: int = 2,
              max_k: int = 10,
              sample_frac: float = 1,
              drop_healthy: bool = False
              ):
    """Helps facilitate model selection for LCA using BIC criterion
    :param gender: None, 'men', or 'women' denotes whether to take full data, only men, or only women.
    :param min_k: the minimum number k clusters to investigate
    :param max_k: the maximum number k clusters to investigate
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    """
    df, mat, pat_ids, labs, cgrps = get_data(sample_frac, drop_healthy, gender)
    if gender == 'men':
        foldr = LCA_MEN
    elif gender == 'women':
        foldr = LCA_WOMEN
    else:
        foldr = LCA_RESULTS
    select_lca_model(mat, foldr, min_k, max_k)


@cli.command()
@click.option("-g", "--gender", type=str, default=None,
              help="denotes whether to take full data (None), only 'men', or only 'women'")
@click.option("-o", "--outfl", type=str, default=None,
              help="the file name to which the resulting file with cluster labels should be written")
@click.option("-k", "--kclusters", type=int, default=10,
              help="k clusters")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
def lca(gender: str,
        outfl: str,
        kclusters: int = 10,
        sample_frac: float = 1,
        drop_healthy: bool = False):
    """Performs LCA clustering
    :param gender: None, 'men', or 'women' denotes whether to take full data, only men, or only women.
    :param outfl: the file location at which the updated file with cluster labels should be saved
    :param kclusters: the number k clusters
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    """
    df, mat, pat_ids, labs, cgrps = get_data(sample_frac, drop_healthy, gender)
    if gender == 'men':
        foldr = LCA_MEN
    elif gender == 'women':
        foldr = LCA_WOMEN
    else:
        foldr = LCA_RESULTS
    model, labels = get_lca_clusters(mat, foldr, kclusters)
    df['lca_cluster_labels'] = labels
    df.to_csv(osp.join(foldr, outfl), sep='\t')
    plot_morbidity_dist(df, 'lca_cluster_labels', foldr, 'latent_class_analysis')


@cli.command()
@click.option("-g", "--gender", type=str, default=None,
              help="denotes whether to take full data (None), only 'men', or only 'women'")
@click.option("-o", "--outfl", type=str, default=None,
              help="the file name to which the resulting file with cluster labels should be written")
@click.option("-k", "--kclusters", type=int, default=10,
              help="k clusters")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
def kmedoids(gender: str,
             outfl: str,
             kclusters: int = 10,
             sample_frac: float = 1,
             drop_healthy: bool = False):
    """Performs KMedoids clustering
    :param gender: None, 'men', or 'women' denotes whether to take full data, only men, or only women.
    :param outfl: the file location at which the updated file with cluster labels should be saved
    :param kclusters: the number k clusters
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    """
    df, mat, pat_ids, labs, cgrps = get_data(sample_frac, drop_healthy, gender)
    if gender == 'men':
        foldr = KMEDOIDS_MEN
    elif gender == 'women':
        foldr = KMEDOIDS_WOMEN
    else:
        foldr = KMEDOIDS_RESULTS
    model, labels = fit_kmedoids(mat, foldr, cgrps, kclusters)
    df['kmedoids_cluster_labels'] = labels
    df.to_csv(osp.join(foldr, outfl), sep='\t')
    plot_morbidity_dist(df, 'kmedoids_cluster_labels', foldr, 'kmedoids')


@cli.command()
@click.option("-g", "--gender", type=str, default=None,
              help="denotes whether to take full data (None), only 'men', or only 'women'")
@click.option("-o", "--outfl", type=str, default=None,
              help="the file name to which the resulting file with cluster labels should be written")
@click.option("-k", "--kclusters", type=int, default=10,
              help="k clusters")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
def kmodes(gender: str,
           outfl: str,
           kclusters: int = 10,
           sample_frac: float = 1,
           drop_healthy: bool = False):
    """Performs KModes clustering
    :param gender: None, 'men', or 'women' denotes whether to take full data, only men, or only women.
    :param outfl: the file location at which the updated file with cluster labels should be saved
    :param kclusters: the number k clusters
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    """
    df, mat, pat_ids, labs, cgrps = get_data(sample_frac, drop_healthy, gender)
    if gender == 'men':
        foldr = KMODES_MEN
    elif gender == 'women':
        foldr = KMODES_WOMEN
    else:
        foldr = KMODES_RESULTS
    model, labels = fit_kmodes(mat, foldr, cgrps, kclusters)
    df['kmodes_cluster_labels'] = labels
    df.to_csv(osp.join(foldr, outfl), sep='\t')
    plot_morbidity_dist(df, 'kmodes_cluster_labels', foldr, 'kmodes')
