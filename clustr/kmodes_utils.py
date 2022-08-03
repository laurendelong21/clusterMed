from kmodes.kmodes import KModes
# Import module for data visualization
from plotnine import *
import plotnine
# Data visualization with matplotlib
import matplotlib.pyplot as plt
# Use the theme of ggplot
plt.style.use('ggplot')


def calculate_kmodes(dfMatrix, max_k=10, distance_metric='Huang'):
    """Gets an array of costs per K"""
    cost = []
    for cluster in range(1, max_k):
        kmodes = KModes(n_jobs=-1, n_clusters=cluster, init=distance_metric, random_state=0)
        kmodes.fit_predict(dfMatrix)
        cost.append(kmodes.cost_)
        print('Cluster initiation: {}'.format(cluster))

    return cost


def plot_ks(cost, max_k=10):
    """Plots the respective costs per K"""
    df_cost = pd.DataFrame({'Cluster': range(1, max_k), 'Cost': cost})# Data viz
    plotnine.options.figure_size = (8, 4.8)
    (
        ggplot(data = df_cost)+
        geom_line(aes(x = 'Cluster',
                      y = 'Cost'))+
        geom_point(aes(x = 'Cluster'kmodes,
                       y = 'Cost'))+
        geom_label(aes(x = 'Cluster',
                       y = 'Cost',
                       label = 'Cluster'),
                   size = max_k,
                   nudge_y = 1000) +
        labs(title = 'Optimal number of cluster with Elbow Method')+
        xlab('Number of Clusters k')+
        ylab('Cost')+
        theme_minimal()
    )


