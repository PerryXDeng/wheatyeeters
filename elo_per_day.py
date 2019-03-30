import numpy as np
import pandas as pd


def join_cols():

    # Reads in csv files to be manipulated
    dfg = pd.read_csv('data_preparation/data/games_ranked.csv')

    # Creates the new dataframe where each date is a unique column, and gets the number of dates
    unique_dates = pd.DataFrame(dfg["Date"].unique()).to_numpy()
    unique_rows = unique_dates.shape[0]
    daily_elos = np.array(unique_rows).astype(float)
    print(unique_rows)

    # Creates two numpy arrays to perform some operations on
    dates = dfg["Date"].to_numpy()
    e_change = dfg["eloChangeAdjusted"].to_numpy()
    rows = dates.shape()[0]

    # sums up the elo change on a given day and then exports it to a unique .csv file
    x = 0
    for i in range(0, rows):
        if not (dates[i] == unique_dates[x]):
            x = x + 1
        daily_elos[x] = daily_elos[x] + e_change[i]

    # Creates a new dataframe from the two unique date array and the daily elo change array
    df_dec = pd.DataFrame()
    df_dec["Date"] = unique_dates
    df_dec["DailyElo"] = daily_elos
    print(df_dec)

