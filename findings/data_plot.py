from matplotlib import pyplot as plt
import pandas as pd


def plot_xy(x, y):
    plt.scatter(x, y)
    plt.xlabel(x.name)
    plt.ylabel(y.name)
    plt.show()


wellness = pd.read_csv('../data_preparation/data/wellness.csv')
plot_xy(wellness['Fatigue'], wellness['SleepHours'])
