import click
import logging
import os
import os.path as osp
from memory_profiler import profile
from clustr.constants import PROCESSED_DATA
from clustr.constants import HIER_AGG_RESULTS, AGG_MEN, AGG_WOMEN
from clustr.constants import LCA_RESULTS, LCA_MEN, LCA_WOMEN
from clustr.constants import KMEDOIDS_RESULTS, KMEDOIDS_MEN, KMEDOIDS_WOMEN
from clustr.constants import KMODES_RESULTS, KMODES_MEN, KMODES_WOMEN
from clustr.utils import get_data, plot_ks, plot_morbidity_dist, dict_to_json
from clustr.hier_agg_utils import get_agg_clusters, plot_dendrogram
from clustr.lca_utils import select_lca_model, get_lca_clusters
from clustr.kmedoids_utils import calculate_kmedoids, fit_kmedoids
from clustr.kmodes_utils import calculate_kmodes, fit_kmodes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@click.group()
def cli():
    """Entry method for the CLI."""
    pass


@profile
@cli.command()
@click.option("-i", "--infile", type=str, default=None,
              help="the input filepath; recommended to store within the 'data' directory")
@click.option("-b", "--subdir", type=str, default=None,
              help="denotes a subdirectory to create and write to, such as 'women'")
@click.option("-m", "--metric", type=str, default='hamming',
              help="the metric to be used for clustering")
@click.option("-l", "--linkage", type=str, default='complete',
              help="the type of linkage to be used for clustering")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
@click.option("-c", "--coi", type=str, default=None,
              help="the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis")
def agg(infile: str,
        subdir: str,
        metric: str = 'hamming',
        linkage: str = 'complete',
        sample_frac: float = 1,
        drop_healthy: bool = False,
        coi=None):
    """Hierarchical agglomerative clustering from command line
    :param infile: the input filepath; recommended to store within the 'data' directory
    :param subdir: denotes a subdirectory to create and write
    :param metric: the metric type used for clustering; default is hamming distance
    :param linkage: linkage method; default is complete
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions,
    :param coi: the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis
    """
    df, mat, _, _, _ = get_data(infile, sample_frac, drop_healthy, coi)
    foldr = osp.join(HIER_AGG_RESULTS, subdir) if subdir else HIER_AGG_RESULTS
    os.makedirs(foldr, exist_ok=True)
    _, labels = get_agg_clusters(mat, foldr, metric, linkage)
    plot_dendrogram(mat, foldr, metric, linkage)
    df['aggl_cluster_labels'] = labels
    df.to_csv(osp.join(foldr, 'hier_agg_labels.tsv'), sep='\t')
    plot_morbidity_dist(df, 'aggl_cluster_labels', foldr, 'agglomerative_hierarchical')


@cli.command()
@click.option("-i", "--infile", type=str, default=None,
              help="the input filepath; recommended to store within the 'data' directory")
@click.option("-b", "--subdir", type=str, default=None,
              help="denotes a subdirectory to create and write to, such as 'women'")
@click.option("-mi", "--min_k", type=int, default=2,
              help="the minimum number k clusters to investigate")
@click.option("-ma", "--max_k", type=int, default=10,
              help="the maximum number k clusters to investigate")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
@click.option("-c", "--coi", type=str, default=None,
              help="the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis")
def lcaselect(infile: str,
              subdir: str,
              min_k: int = 2,
              max_k: int = 10,
              sample_frac: float = 1,
              drop_healthy: bool = False,
              coi=None
              ):
    """Helps facilitate model selection for LCA using BIC criterion
    :param infile: the input filepath; recommended to store within the 'data' directory
    :param subdir: denotes a subdirectory to create and write
    :param min_k: the minimum number k clusters to investigate
    :param max_k: the maximum number k clusters to investigate
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    :param coi: the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis
    """
    _, mat, _, _, _ = get_data(infile, sample_frac, drop_healthy, coi)
    foldr = osp.join(LCA_RESULTS, subdir) if subdir else LCA_RESULTS
    os.makedirs(foldr, exist_ok=True)
    bics = select_lca_model(mat, foldr, min_k, max_k)
    dict_to_json(bics, osp.join(foldr, 'bics.json'))


@cli.command()
@click.option("-i", "--infile", type=str, default=None,
              help="the input filepath; recommended to store within the 'data' directory")
@click.option("-b", "--subdir", type=str, default=None,
              help="denotes a subdirectory to create and write to, such as 'women'")
@click.option("-r", "--repetitions", type=int, default=1,
              help="number of times to run the clustering method")
@click.option("-k", "--kclusters", type=int, default=10,
              help="k clusters")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
@click.option("-c", "--coi", type=str, default=None,
              help="the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis")
def lca(infile: str,
        subdir: str,
        repetitions: int = 1,
        kclusters: int = 10,
        sample_frac: float = 1,
        drop_healthy: bool = False,
        coi=None):
    """Performs LCA clustering
    :param infile: the input filepath; recommended to store within the 'data' directory
    :param subdir: denotes a subdirectory to create and write
    :param repetitions: number of times to run the clustering method
    :param kclusters: the number k clusters
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions,
    :param coi: the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis
    """
    df, mat, _, _, _ = get_data(infile, sample_frac, drop_healthy, coi)
    foldr = osp.join(LCA_RESULTS, subdir) if subdir else LCA_RESULTS
    
    # do r number of times:
    for i in range(repetitions):
        if repetitions != 1:
            subfolder = osp.join(foldr, f'run_{i}')
        else:
            subfolder = foldr
        
        os.makedirs(subfolder, exist_ok=True)
        _, labels = get_lca_clusters(mat, subfolder, kclusters)
        df['lca_cluster_labels'] = labels
        df.to_csv(osp.join(subfolder, 'lca_cluster_labels.tsv'), sep='\t')
        plot_morbidity_dist(df, 'lca_cluster_labels', subfolder, 'latent_class_analysis')


@cli.command()
@click.option("-i", "--infile", type=str, default=None,
              help="the input filepath; recommended to store within the 'data' directory")
@click.option("-b", "--subdir", type=str, default=None,
              help="denotes a subdirectory to create and write to, such as 'women'")
@click.option("-mi", "--min_k", type=int, default=2,
              help="the minimum number k clusters to investigate")
@click.option("-ma", "--max_k", type=int, default=10,
              help="the maximum number k clusters to investigate")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
@click.option("-c", "--coi", type=str, default=None,
              help="the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis")
def kmeselect(infile: str,
              subdir: str,
              min_k: int = 2,
              max_k: int = 10,
              sample_frac: float = 1,
              drop_healthy: bool = False,
              coi: str = None
              ):
    """Helps facilitate model selection for k-medoids using silhouette score
    :param infile: the input filepath; recommended to store within the 'data' directory
    :param subdir: denotes a subdirectory to create and write
    :param min_k: the minimum number k clusters to investigate
    :param max_k: the maximum number k clusters to investigate
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    :param coi: the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis
    """
    _, mat, _, _, _ = get_data(infile, sample_frac, drop_healthy, coi)
    foldr = osp.join(KMEDOIDS_RESULTS, subdir) if subdir else KMEDOIDS_RESULTS
    os.makedirs(foldr, exist_ok=True)
    costs, sil_scores = calculate_kmedoids(mat, min_k, max_k)
    dict_to_json(dict(costs), osp.join(foldr, 'costs.json'))
    dict_to_json(dict(sil_scores), osp.join(foldr, 'sil_scores.json'))
    plot_ks(list(costs.values()), foldr, 'costs', min_k, max_k)
    plot_ks(list(sil_scores.values()), foldr, 'silhouette', min_k, max_k)


@cli.command()
@click.option("-i", "--infile", type=str, default=None,
              help="the input filepath; recommended to store within the 'data' directory")
@click.option("-b", "--subdir", type=str, default=None,
              help="denotes a subdirectory to create and write to, such as 'women'")
@click.option("-k", "--kclusters", type=int, default=10,
              help="k clusters")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
@click.option("-c", "--coi", type=str, default=None,
              help="the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis")
def kmedoids(infile: str,
             subdir: str,
             kclusters: int = 10,
             sample_frac: float = 1,
             drop_healthy: bool = False,
             coi: str = None):
    """Performs KMedoids clustering
    :param infile: the input filepath; recommended to store within the 'data' directory
    :param subdir: denotes a subdirectory to create and write
    :param kclusters: the number k clusters
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    :param coi: the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis
    """
    df, mat, _, _, cgrps = get_data(infile, sample_frac, drop_healthy, coi)
    foldr = osp.join(KMEDOIDS_RESULTS, subdir) if subdir else KMEDOIDS_RESULTS

    os.makedirs(foldr, exist_ok=True)

    _, labels = fit_kmedoids(mat, foldr, cgrps, kclusters)
    df['kmedoids_cluster_labels'] = labels
    df.to_csv(osp.join(foldr, 'kmedoids_cluster_labels.tsv'), sep='\t')
    plot_morbidity_dist(df, 'kmedoids_cluster_labels', foldr, 'kmedoids')


@cli.command()
@click.option("-i", "--infile", type=str, default=None,
              help="the input filepath; recommended to store within the 'data' directory")
@click.option("-b", "--subdir", type=str, default=None,
              help="denotes a subdirectory to create and write to, such as 'women'")
@click.option("-mi", "--min_k", type=int, default=2,
              help="the minimum number k clusters to investigate")
@click.option("-ma", "--max_k", type=int, default=10,
              help="the maximum number k clusters to investigate")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
@click.option("-c", "--coi", type=str, default=None,
              help="the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis")
def kmoselect(infile: str,
              subdir: str,
              min_k: int = 2,
              max_k: int = 10,
              sample_frac: float = 1,
              drop_healthy: bool = False,
              coi: str = None
              ):
    """Helps facilitate model selection for k-modes using silhouette score
    :param infile: the input filepath; recommended to store within the 'data' directory
    :param subdir: denotes a subdirectory to create and write
    :param min_k: the minimum number k clusters to investigate
    :param max_k: the maximum number k clusters to investigate
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    :param coi: the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis
    """
    _, mat, _, _, _ = get_data(infile, sample_frac, drop_healthy, coi)
    foldr = osp.join(KMODES_RESULTS, subdir) if subdir else KMODES_RESULTS
    os.makedirs(foldr, exist_ok=True)
    costs, sil_scores = calculate_kmodes(mat, min_k, max_k)
    dict_to_json(dict(costs), osp.join(foldr, 'costs.json'))
    dict_to_json(dict(sil_scores), osp.join(foldr, 'sil_scores.json'))
    plot_ks(list(costs.values()), foldr, 'costs', min_k, max_k)
    plot_ks(list(sil_scores.values()), foldr, 'silhouette', min_k, max_k)


@cli.command()
@click.option("-i", "--infile", type=str, default=None,
              help="the input filepath; recommended to store within the 'data' directory")
@click.option("-b", "--subdir", type=str, default=None,
              help="denotes a subdirectory to create and write to, such as 'women'")
@click.option("-r", "--repetitions", type=int, default=1,
              help="number of times to run the clustering method")
@click.option("-k", "--kclusters", type=int, default=10,
              help="k clusters")
@click.option("-s", "--sample_frac", type=float, default=1,
              help="the fraction of the dataset to use")
@click.option("-dh", "--drop_healthy", type=bool, default=False,
              help="whether to drop those who have no conditions")
@click.option("-c", "--coi", type=str, default=None,
              help="the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis")
def kmodes(infile: str,
           subdir: str,
           repetitions: int = 1,
           kclusters: int = 10,
           sample_frac: float = 1,
           drop_healthy: bool = False,
           coi: str = None):
    """Performs KModes clustering
    :param infile: the input filepath; recommended to store within the 'data' directory
    :param subdir: denotes a subdirectory to create and write
    :param repetitions: number of times to run the clustering method
    :param kclusters: the number k clusters
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    :param coi: the name of some condition of interest (e.g. 'Depression') which is taken out of the analysis
    """
    df, mat, _, _, cgrps = get_data(infile, sample_frac, drop_healthy, coi)
    foldr = osp.join(KMODES_RESULTS, subdir) if subdir else KMODES_RESULTS

    # do r number of times:
    for i in range(repetitions):
        if repetitions != 1:
            subfolder = osp.join(foldr, f'run_{i}')
        else:
            subfolder = foldr
            
        os.makedirs(subfolder, exist_ok=True)

        model, labels = fit_kmodes(mat, subfolder, cgrps, kclusters)
        df['kmodes_cluster_labels'] = labels
        df.to_csv(osp.join(subfolder, 'kmodes_cluster_labels.tsv'), sep='\t')
        plot_morbidity_dist(df, 'kmodes_cluster_labels', subfolder, 'kmodes')
