from sklearn_extra.cluster import KMedoids


def calculate_kmedoids(dfMatrix, max_k=10):
    """Gets an array of costs per K"""
    cost = []
    for cluster in range(1, max_k):
        try:
            cobj = KMedoids(n_clusters=cluster, random_state=0, metric='cosine').fit(dfMatrix)
            cost.append(cobj.inertia_)
            print('Cluster initiation: {}'.format(cluster))
        except:
            break

    return cost