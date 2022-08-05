import click
import logging
import os.path as osp
import pandas as pd
from clustr.constants import PROCESSED_DATA, HIER_AGG_RESULTS, LCA_RESULTS
from clustr.utils import get_data, plot_morbidity_dist
from clustr.hier_agg_utils import get_agg_clusters, plot_dendrogram
from clustr.lca_utils import select_lca_model, get_lca_clusters

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@click.group()
def cli():
    """Entry method for the CLI."""
    pass


@cli.command()
@click.option("-d", "--datafl", type=str, default=None,
              help="the file name containing the data")
@click.option("-o", "--outfl", type=str, default=None,
              help="the file name to which the resulting file with cluster labels should be written")
@click.option("-do", "--dendro_outfl", type=str, default=None,
              help="the file name to which the dendrogram should be written")
@click.option("-m", "--metric", type=str, default='hamming',
              help="the metric to be used for clustering")
@click.option("-l", "--linkage", type=str, default='complete',
              help="the type of linkage to be used for clustering")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
def agg(datafl: str,
        outfl: str,
        dendro_outfl: str,
        metric: str = 'hamming',
        linkage: str = 'complete',
        sample_frac: float = 1,
        drop_healthy: bool = False):
    """Hierarchical agglomerative clustering from command line
    :param datafl: the path for the data file to read the data in
    :param outfl: the file location at which the updated file with cluster labels should be saved
    :param dendro_outfl: the file location at which the dendrogram picture should be saved
    :param metric: the metric type used for clustering; default is hamming distance
    :param linkage: linkage method; default is complete
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    """
    df, mat, pat_ids, labs, cgrps = get_data(osp.join(PROCESSED_DATA, datafl), sample_frac, drop_healthy)
    model, labels = get_agg_clusters(mat, metric, linkage)
    plot_dendrogram(mat, dendro_outfl, metric, linkage)
    df['aggl_cluster_labels'] = labels
    df.to_csv(osp.join(HIER_AGG_RESULTS, outfl), sep='\t')
    plot_morbidity_dist(df, labels, HIER_AGG_RESULTS, 'agglomerative_hierarchical')


@cli.command()
@click.option("-d", "--datafl", type=str, default=None,
              help="the file name containing the data")
@click.option("-mi", "--min_k", type=int, default=2,
              help="the minimum number k clusters to investigate")
@click.option("-ma", "--max_k", type=int, default=10,
              help="the maximum number k clusters to investigate")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
def lcaselect(datafl: str,
              min_k: int = 2,
              max_k: int = 10,
              sample_frac: float = 1,
              drop_healthy: bool = False
              ):
    """Helps facilitate model selection for LCA using BIC criterion
    :param datafl: the path for the data file to read the data in
    :param min_k: the minimum number k clusters to investigate
    :param max_k: the maximum number k clusters to investigate
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    """
    df, mat, pat_ids, labs, cgrps = get_data(osp.join(PROCESSED_DATA, datafl), sample_frac, drop_healthy)
    select_lca_model(mat, min_k, max_k)


@cli.command()
@click.option("-d", "--datafl", type=str, default=None,
              help="the file name containing the data")
@click.option("-o", "--outfl", type=str, default=None,
              help="the file name to which the resulting file with cluster labels should be written")
@click.option("-k", "--kclusters", type=int, default=10,
              help="k clusters")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
def lca(datafl: str,
        outfl: str,
        kclusters: int = 10,
        sample_frac: float = 1,
        drop_healthy: bool = False):
    """Performs LCA clustering
    :param datafl: the path for the data file to read the data in
    :param outfl: the file location at which the updated file with cluster labels should be saved
    :param kclusters: the number k clusters
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    """
    df, mat, pat_ids, labs, cgrps = get_data(osp.join(PROCESSED_DATA, datafl), sample_frac, drop_healthy)
    model, labels = get_lca_clusters(mat, kclusters)
    df['lca_cluster_labels'] = labels
    df.to_csv(osp.join(LCA_RESULTS, outfl), sep='\t')
