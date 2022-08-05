import pandas as pd
import matplotlib.pyplot as plt
# Use the theme of ggplot
plt.style.use('ggplot')
from typing import List, Dict, Any
import json
import os.path as osp


def dict_to_json(d: Dict[Any, Any],
                 filename: str):
    """Writes a dictionary to json file"""
    with open(filename, "w") as outfile:
        json.dump(d, outfile)


def get_top_cluster_conds(df: pd.DataFrame,
                          cgrps: List[str],
                          cluster_labels: str,
                          cluster_no: int):
    """Gets the condition frequencies for a certain cluster
    :param df: the dataframe being operated upon
    :param cgrps: the list of condition groups
    :param cluster_labels: the column name containing the cluster labels
    :param cluster_no: the cluster number to select"""
    clstr = df.loc[df[cluster_labels] == cluster_no]
    clus_morbs = clstr[cgrps].sum().sort_values(ascending=False)
    return clus_morbs


def get_adjusted_cluster_conds(df: pd.DataFrame,
                               cgrps: List[str],
                               cluster_labels: str,
                               cluster_no: int):
    """Gets the adjusted relative condition frequencies for a certain cluster
    :param df: the dataframe being operated upon
    :param cgrps: the list of condition groups
    :param cluster_labels: the column name containing the cluster labels
    :param cluster_no: the cluster number to select"""
    clus_morbs = get_top_cluster_conds(cluster_labels, cluster_no)
    clus_freqs = clus_morbs.div(df[cluster_labels].value_counts()[cluster_no])
    morb_freqs = df[cgrps].sum().sort_values(ascending=False).div(len(df))
    adj_freqs = clus_freqs.div(morb_freqs).sort_values(ascending=False)
    return adj_freqs, clus_morbs


# TODO: plotting function for adjusted values


def plot_morbidity_dist(df: pd.DataFrame,
                        cluster_labels: str,
                        outfolder: str,
                        clustering_method: str):
    """Plots the distributions of conditions per patient for each cluster
    :param df: the dataframe being operated upon (must contain tot_conditions column)
    :param cluster_labels: the column name containing the cluster labels
    :param outfolder: the folder to which the files should be written
    :param clustering_method: the clustering method used
    :returns: None; Outputs files to file location
    """
    # Individual Histograms
    assert type(df) == pd.DataFrame
    ax = df.plot.hist(column="tot_conditions", by=cluster_labels, figsize=(10, 30))
    plt.savefig(osp.join(outfolder, f'{clustering_method}_histograms.png'), dpi=300, bbox_inches='tight')
    # Boxplot for comparison
    boxplot = df.boxplot(column="tot_conditions", by=cluster_labels)
    plt.ylabel("Total conditions per patient")
    plt.xlabel("Cluster labels")
    plt.title("Distribution of the number of conditions in each cluster")
    plt.suptitle("")
    plt.savefig(osp.join(outfolder, f'{clustering_method}_boxplot.png'), dpi=300, bbox_inches='tight')


def plot_depression(df: pd.DataFrame,
                    labels_column: str,
                    depression_column: str,
                    clustering_method: str):
    """Plots depression breakdown per cluster"""
    labs = df[labels_column].unique()
    labs.sort()
    counts = df[[labels_column, depression_column]].groupby(
        [depression_column, labels_column]).value_counts().unstack(fill_value=0).stack()
    plt.bar(labs, counts[1], bottom=None, color='blue', label='Depression')
    plt.bar(labs, counts[0], bottom=counts[1], color='pink', label='No Depression')
    plt.legend()
    plt.xlabel(f'{clustering_method} Cluster Labels')
    plt.ylabel('Number in each cluster')
    # TODO: savefig
    # TODO: add percentages


def get_data(datafl: str,
             sample_frac: float = 1,
             drop_healthy: bool = False):
    """Gets the data and returns it as a numpy matrix without the depression column.
    :param datafl: the path for the data file to read the data in
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    :returns: dataframe of the data,
                numpy matrix of features,
                patient ids,
                depression labels, &
                feature column names
    """
    df = pd.read_csv(datafl, sep='\t', index_col=0)
    # Subset the data if necessary
    df = df.sample(frac=sample_frac, random_state=1)
    # Get patient IDs
    pat_ids = list(df.index)
    # Take out depression column
    labs = df['Depression']
    df.drop(['Depression'], axis=1, inplace=True)
    # Drop those with no multimorbidities if drop_healthy==True
    if drop_healthy:
        df = df.loc[df.sum(numeric_only=True, axis=1) != 0]
    # Get column names (condition groups)
    cgrps = list(df.columns)
    # Convert dataframe to matrix
    mat = df.to_numpy()
    # Get total conditions column for later
    df['tot_conditions'] = df[cgrps].sum(numeric_only=True, axis=1)
    return pd.DataFrame(df), mat, pat_ids, labs, cgrps

