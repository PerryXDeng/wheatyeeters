import pandas as pd

# read in CSV
df = pd.read_csv('cleaned/dirty_wellness_na.csv')


def vectorize_mult(column, dictionary, file=None):
    newCol = column + "Num"
    df[newCol] = df[column].map(dictionary)
    if file is not None:
        df.to_csv('cleaned/{}.csv'.format(file))

