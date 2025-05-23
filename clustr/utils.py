# Data visualization with matplotlib
import matplotlib.pyplot as plt
import pandas as pd
# Use the theme of ggplot
#plt.style.use('ggplot')
import numpy as np
from typing import List, Dict, Any
import json
import os.path as osp
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests
from clustr.startup import logger


def dict_to_json(d: Dict[Any, Any],
                 filename: str):
    """Writes a dictionary to json file"""
    with open(filename, "w") as outfile:
        json.dump(d, outfile)


def get_top_cluster_conds(df: pd.DataFrame,
                          conditions: List[str],
                          labels_column: str,
                          cluster_no: int):
    """Gets the condition frequencies for a certain cluster
    :param df: the dataframe being operated upon
    :param conditions: the list of conditions; often the column names
    :param labels_column: the column name containing the cluster labels
    :param cluster_no: the cluster number to select"""
    clstr = df.loc[df[labels_column] == cluster_no]
    cluster_counts = clstr[conditions].sum().sort_values(ascending=False)
    return cluster_counts


def get_adjusted_cluster_conds(df: pd.DataFrame,
                               conditions: List[str],
                               labels_column: str,
                               cluster_no: int):
    """Gets the adjusted relative condition frequencies (ARFs) and prevalences for a certain cluster;
        returns them as dictionaries
    :param df: the dataframe being operated upon
    :param conditions: the list of conditions; often the column names
    :param labels_column: the column name containing the cluster labels
    :param cluster_no: the cluster number to select"""
    cluster_counts = get_top_cluster_conds(df, conditions, labels_column, cluster_no)
    cluster_prevalences = cluster_counts.div(df[labels_column].value_counts()[cluster_no])  # relative freqs within cluster
    cohort_prevalences = df[conditions].sum().sort_values(ascending=False).div(len(df))  # relative freqs in the whole cohort
    arfs = cluster_prevalences.div(cohort_prevalences).sort_values(ascending=False)
    return dict(arfs), dict(cluster_prevalences)


def get_arfs_prevalences(df: pd.DataFrame,
                         labels_column: str,
                         conditions: List[str]):
    """Gets the adjusted relative condition frequencies (ARFs) and prevalences for each cluster;
        returns them as dictionaries
    :param df: the dataframe being operated upon
    :param conditions: the list of conditions; often the column names
    :param labels_column: the column name containing the cluster labels
    :param cluster_no: the cluster number to select"""
    arfs_dict = {}  # to store the ARF values
    prevs_dict = {}  # to store the prevalences relative to each cluster

    cohort_prevalences = df[conditions].sum().sort_values(ascending=False).div(len(df))  # relative freqs in the whole cohort

    for clust in df[labels_column].unique():
        cluster_counts = get_top_cluster_conds(df, conditions, labels_column, clust)  # counts of each condition within cluster
        cluster_prevalences = cluster_counts.div(df[labels_column].value_counts()[clust])  # relative freqs within cluster
        arfs = cluster_prevalences.div(cohort_prevalences).sort_values(ascending=False)

        arfs_dict[clust] = dict(arfs)
        prevs_dict[clust] = dict(cluster_prevalences)

    return arfs_dict, prevs_dict


def generate_contingency_table(df: pd.DataFrame,
                               condition: str,
                               labels_column: str,
                               cluster_no: int):
    """Generates a 2x2 contingency table (numpy array) of the people who are in a cluster vs. not in
    that cluster and the people suffering from a condition v. not suffering from that condition.
    :param df: the dataframe being operated upon
    :param condition: the name of the condition being considered
    :param labels_column: the column name containing the cluster labels
    :param cluster_no: the number of the cluster in question
    """
    # select those within the cluster
    clust = df.loc[df[labels_column] == cluster_no]
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


def get_fischers_coefficients(df: pd.DataFrame,
                               labels_column: str,
                               conditions: List[str],
                               alpha: float = 0.05):
    """Finds a Fischer's Exact Test p value for each condition and each cluster label
    to assess whether each condition is overrepresented in each cluster
    Returns two dictionaries: one is the p values, and one is the p values adjusted for Bonferonni and
    alpha of 0.05"""
    coeffs = {}  # to store the p-values
    adj_coeffs = {}  # to store the Bonferonni adjusted p-values
    for clust in df[labels_column].unique():  # for each cluster number,
        coeffs[clust] = {}
        adj_coeffs[clust] = {}
        conds = []
        pvals = []
        for cond in conditions:
            cot_tab = generate_contingency_table(df,
                                                 cond,
                                                 labels_column,
                                                 clust)
            _, p = fisher_exact(cot_tab, alternative='two-sided')
            conds.append(cond)
            pvals.append(p)
            coeffs[clust][cond] = p
        _, adj_pvals, _, _ = multipletests(pvals, alpha, 'bonferroni')  # bonferroni correction of p-values
        for c, a in zip(conds, adj_pvals):
            adj_coeffs[clust][c] = a

    return coeffs, adj_coeffs


def plot_freqs(df: pd.DataFrame,
               cgrps: List[str],
               labels_col: str,
               cluster_no: int,
               out_folder: str,
               pvalue_dict=None,
               yaxis_norm=None):
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
    :param yaxis_norm: the max number of the y axis to which the plot should be scaled to
    """
    adj, freqs = get_adjusted_cluster_conds(df, cgrps, labels_col, cluster_no)
    if pvalue_dict:
        freqs = freqs[[cond for cond, pval in pvalue_dict[cluster_no].items() if pval < 0.05]]
        adj = adj[[cond for cond, pval in pvalue_dict[cluster_no].items() if pval < 0.05]]
    #freqs.plot.bar()
    #plt.yticks(rotation=90)
    #plt.ylabel("Frequency")
    #plt.savefig(osp.join(out_folder, f"cluster_{cluster_no}_frequencies.png"), dpi=300, bbox_inches='tight')
    adj.sort_values(ascending=False).plot.bar(figsize=(15, 10), color="darkblue")
    if yaxis_norm:
        plt.ylim([0, yaxis_norm])
    plt.yticks(rotation=90)
    plt.ylabel("Adjusted Relative Frequency")
    plt.axhline(y=1, color='darkred', linestyle='-')
    plt.savefig(osp.join(out_folder, f"cluster_{cluster_no}_adj_frequencies.png"), dpi=300, bbox_inches='tight')
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


def plot_ks(cost,
            out_folder,
            metric='costs',
            min_k=1,
            max_k=10):
    """Plots the respective costs per K"""
    df_cost = pd.DataFrame.from_dict(cost, orient='index', columns=['Cost'])
    df_cost.reset_index(inplace=True)
    df_cost.columns = ['Cluster', 'Cost']
    num_ks = max_k - min_k
    plt.figure(figsize=(int(num_ks * 8 / 9), 4.8))
    plt.plot(df_cost['Cluster'], df_cost['Cost'], marker='o', linestyle='-')
    plt.scatter(df_cost['Cluster'], df_cost['Cost'])
    for i, txt in enumerate(df_cost['Cluster']):
        plt.annotate(txt, (df_cost['Cluster'][i], df_cost['Cost'][i]+1000), size=max_k)
    plt.title('Optimal number of Clusters')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel(f'{metric}')
    plt.savefig(osp.join(out_folder, f'model_selection_{metric}.png'), dpi=300)
    plt.close()



def get_data(input_file,
             sample_frac: float = 1,
             drop_healthy: bool = False,
             coi=None):
    """Gets the data and returns it as a numpy matrix without the depression column.
    :param input_file: the file containing the data, in which columns are conditions, 
            rows are patients, and values are binary
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :param drop_healthy: boolean value indicating whether to drop those with no conditions
    :param coi: the conditions of interest; these columns are removed from the data for clustering
                and stored/returned separately; if None, all conditions are used.
                Should be a string or a list of strings (List[str])
    :returns: dataframe of the data,
                numpy matrix of features,
                patient ids,
                the excluded condition values, &
                condition names
    """
    logger.info(f'Processing data from {input_file}...')
    df = pd.read_csv(input_file, sep='\t', index_col=0)
    # Subset the data if necessary
    df = df.sample(frac=sample_frac, random_state=1)
    # Get patient IDs
    pat_ids = list(df.index)
    # Take out excluded condition(s) of interest
    exclusions = None
    if coi:
        exclusions = df[coi]
        coi = [coi] if type(coi) != list else coi  ##  if coi is a string, make it a list
        df.drop(coi, axis=1, inplace=True)
    # Drop those with no multimorbidities if drop_healthy==True
    if drop_healthy:
        df = df.loc[df.sum(numeric_only=True, axis=1) != 0]
    # Get column names (conditions)
    cgrps = list(df.columns)
    # Convert dataframe to matrix
    mat = df.to_numpy()
    # Get total conditions column for later
    df['tot_conditions'] = df[cgrps].sum(numeric_only=True, axis=1)
    logger.info(f'Finished processing data from {input_file}.')
    return df, mat, pat_ids, exclusions, cgrps


def map_to_scale(arf):
    """Maps ARF value to a scaled value to show magnitude better"""
    scaled_arf = 2 * (arf - 1) / (arf + 1)
    return scaled_arf


def get_bubble_heatmap_input(values_dict,
                             pvalue_dict,
                             alpha: float = 0.05,
                             arf_scaling = False):
    """Formats values so the user can make a bubble heatmap.
    :param values_dict: the dictionary of dictionaries containing {cluster ID: {condition: value}},
        where value can be prevalences or ARF values
    :param pvalue_dict: the dictionary of dictionaries containing {cluster ID: {condition: pvalue}}; the user should
        decide whether to use adjusted or regular p-values
    :param alpha: the pvalue threshold for significance; anything >= to pvalue is omitted
    :param arf_scaling: boolean value indicating whether to scale the values_dict for better visualization (recommended if they are ARFs)
    """
    assert set(values_dict.keys()) == set(pvalue_dict.keys()), "The keys of the values_dict and pvalue_dict must match"
    
    heatmap_data = pd.DataFrame(values_dict)

    # get the masks to omit the non-significant values
    heatmap_masks = {key: dict() for key in values_dict.keys()}
    for cluster, val in values_dict.items():
        for condition in val:
            if pvalue_dict[cluster][condition] >= alpha:
                heatmap_masks[cluster][condition] = True
            else:
                heatmap_masks[cluster][condition] = False
    heatmap_masks = pd.DataFrame(heatmap_masks)

    # find the rows where all columns are true, drop them
    true_indices = heatmap_masks.all(axis=1)
    true_indices = list(true_indices.index[true_indices])
    heatmap_data.drop(true_indices, inplace=True)
    heatmap_masks.drop(true_indices, inplace=True)

    # scale if necessary
    if arf_scaling:
        heatmap_data = heatmap_data.applymap(map_to_scale)

    # Flatten the DataFrame
    result_df = heatmap_data.where(~heatmap_masks, np.nan)
    flattened_df = pd.melt(result_df.reset_index(), id_vars=['index'], var_name='cluster', value_name='values')
    flattened_df.rename(columns={'index': 'condition'}, inplace=True)
    flattened_df['abs_values'] = flattened_df['values'].map(lambda x: abs(x))  # get the absval for magnitude
    flattened_df['overrep'] = flattened_df['values'].map(lambda x: 1 if x > 0 else 0)  # over or under represented directionality

    return flattened_df
