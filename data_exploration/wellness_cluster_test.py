import sklearn.cluster as cluster
import pandas as pd
from matplotlib import pyplot as plt


def find_kmeans(mat, k, first, second):
    km = cluster.KMeans(n_clusters=k)
    km.fit(mat)

    # Plot sse against k
    plt.figure(figsize=(6, 6))
    plt.xlabel('Metric: ' + first)
    plt.ylabel('Metric: ' + second)
    plt.scatter(mat[:, 0], mat[:, 1], c=km.labels_, cmap='rainbow')
    plt.show()


# Read csv in
df = pd.read_csv('../data_preparation/cleaned/time_series_normalized_wellness_menstruation.csv')

# Specify what things you want
df = df[["normFatigue", "normSleepQuality"]]

# values, num clusters, axis labelsg
find_kmeans(df.values, 2, "normFatigue", "normSleepQuality")