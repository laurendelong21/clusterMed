import pandas as pd
import matplotlib.pyplot as plt
# Use the theme of ggplot
plt.style.use('ggplot')


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


def get_data(datafl, sample_frac=1):
    """Gets the data and returns it as a numpy matrix without the depression column.
    :param datafl: the path for the data file to read the data in
    :param sample_frac: the fraction of the data to be sampled; default is 1, so all the data is used
    :returns: numpy matrix of features, depression labels, feature column names
    """
    df = pd.read_csv(datafl, sep='\t', index_col=0)
    # Subset the data if necessary
    df = df.sample(frac=sample_frac, random_state=1)
    # Take out depression column
    labs = df['Depression']
    df.drop(['Depression'], axis=1, inplace=True)
    # Get column names (condition groups)
    cgrps = df.columns
    # Convert dataframe to matrix
    mat = df.to_numpy()
    return mat, labs, cgrps
