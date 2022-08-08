import click
import logging
import os.path as osp
from memory_profiler import profile
import pandas as pd
from clustr.constants import PROCESSED_DATA, HIER_AGG_RESULTS, LCA_RESULTS, KMEDOIDS_RESULTS, KMODES_RESULTS
from clustr.utils import get_data, plot_morbidity_dist
from clustr.hier_agg_utils import get_agg_clusters, plot_dendrogram


@profile
def test_agg1():
    """TODO"""
    df, mat, pat_ids, labs, cgrps = get_data(osp.join(PROCESSED_DATA, 'gp_mmorbs.tsv'), 0.01, True)
    model, labels = get_agg_clusters(mat, 'hamming', 'complete')
    df['aggl_cluster_labels'] = labels
    df.to_csv(osp.join(HIER_AGG_RESULTS, 'gp_labs.tsv'), sep='\t')


@profile
def test_agg2():
    """TODO"""
    df, mat, pat_ids, labs, cgrps = get_data(osp.join(PROCESSED_DATA, 'gp_mmorbs.tsv'), 0.25, True)
    model, labels = get_agg_clusters(mat, 'hamming', 'complete')
    df['aggl_cluster_labels'] = labels
    df.to_csv(osp.join(HIER_AGG_RESULTS, 'gp_labs.tsv'), sep='\t')


@profile
def test_agg3():
    """TODO"""
    df, mat, pat_ids, labs, cgrps = get_data(osp.join(PROCESSED_DATA, 'gp_mmorbs.tsv'), 1, True)
    model, labels = get_agg_clusters(mat, 'hamming', 'complete')
    df['aggl_cluster_labels'] = labels
    df.to_csv(osp.join(HIER_AGG_RESULTS, 'gp_labs.tsv'), sep='\t')


if __name__ == '__main__':
    test_agg1()
    test_agg2()
    test_agg3()
