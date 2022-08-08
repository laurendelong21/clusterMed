import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Use the theme of ggplot
plt.style.use('ggplot')
from typing import List, Dict, Any
import json
import os.path as osp
from scipy.stats import fisher_exact


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


def generate_contingency_table(df: pd.DataFrame,
                               condition: str,
                               labels_col: str,
                               cluster_no: int):
    """Generates a 2x2 contingency table (numpy array) of the people who are in a cluster vs. not in
    that cluster and the people suffering from a condition v. not suffering from that condition.
    :param df: the dataframe being operated upon
    :param condition: the name of the condition being considered
    :param labels_col: the column name containing the cluster labels
    :param cluster_no: the number of the cluster in question
    """
    # select those within the cluster
    clust = df.loc[df[labels_col] == cluster_no]
    # people in the cluster with the condition
    clust_cond = clust[condition].sum()
    # people in the cluster w/o the condition
    clust_no_cond = len(clust) - clust_cond
    # the rest of the people with the condition
    tot_cond = df[condition].sum() - clust_cond
    # the rest of the people without the condition
    tot_no_cond = len(df) - tot_cond - clust_no_cond
    cont_table = np.array([[clust_cond, clust_no_cond],
                           [tot_cond, tot_no_cond]])
    return cont_table


def find_fischers_coefficients(df: pd.DataFrame,
                               labels_col: str,
                               cgrps: List[str],
                               outfl: str,
                               output_type: str = 'json'):
    """Finds a Fischer's Exact Test p value for each condition and each cluster label
    to assess whether each condition is overrepresented in each cluster"""
    coeffs = {}
    for clust in df[labels_col].unique():
        coeffs[clust] = {}
        for cond in cgrps:
            cot_tab = generate_contingency_table(df,
                                                 cond,
                                                 labels_col,
                                                 clust)
            oddsr, p = fisher_exact(cot_tab, alternative='two-sided')
            coeffs[clust][cond] = p
    if output_type == 'json':
        dict_to_json(coeffs, outfl)
    elif output_type == 'df':
        pd.DataFrame(coeffs).to_csv(outfl, sep='\t')

    return coeffs


def plot_freqs(df: pd.DataFrame,
               cgrps: List[str],
               labels_col: str,
               cluster_no: int,
               out_folder: str,
               pvalue_dict=None):
    """Plots and generates figures for the frequencies and adjusted relative frequencies of each condition
    in the specified cluster. If pvalue_dict is passed from the Fischer's test, then only plots
    those conditions which are significantly under- or over- represented.
    :param df: the dataframe being operated upon
    :param cgrps: the list of condition groups
    :param labels_col: the column name containing the cluster labels
    :param cluster_no: the cluster number to select
    :param out_folder: the folder to which the figure files should be written.
    :param pvalue_dict: the dictionary of dictionaries containing {cluster number: {condition: pvalue}}
            if None, then all frequencies will be plotted.
    """
    adj, freqs = get_adjusted_cluster_conds(df, cgrps, labels_col, cluster_no)
    if pvalue_dict:
        freqs = freqs[[cond for cond, pval in pvalue_dict[cluster_no].items() if pval < 0.05]]
        adj = adj[[cond for cond, pval in pvalue_dict[cluster_no].items()if pval < 0.05]]
    freqs.plot.bar()
    plt.yticks(rotation=90)
    plt.ylabel("Frequency")
    plt.savefig(osp.join(out_folder, "frequencies.png"), dpi=300, bbox_inches='tight')
    adj.plot.bar()
    plt.yticks(rotation=90)
    plt.ylabel("Adjusted Relative Frequency")
    plt.savefig(osp.join(out_folder, "adj_frequencies.png"), dpi=300, bbox_inches='tight')
    # TODO: get the pvalues or **s somehow represented on this plot


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
    bin_no = max(df['tot_conditions']) + 1
    ax = df.plot.hist(column="tot_conditions", by=cluster_labels, range=[1, bin_no], bins=bin_no*2,
                      align='mid', figsize=(10, 40))
    plt.xticks(np.arange(1, bin_no, 1))
    plt.xlabel("Number of conditions")
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
    return df, mat, pat_ids, labs, cgrps

