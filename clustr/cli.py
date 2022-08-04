import click
import logging
import os.path as osp
import pandas as pd
from clustr.constants import PROCESSED_DATA, HIER_AGG_RESULTS
from clustr.utils import get_data, plot_morbidity_dist
from clustr.hier_agg_utils import get_agg_clusters, plot_dendrogram

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
    # plot_morbidity_dist(df, labels, HIER_AGG_RESULTS, 'agglomerative_hierarchical')
