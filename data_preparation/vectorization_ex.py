import pandas as pd

# read in CSV
df = pd.read_csv('cleaned/dirty_wellness.csv')


def vectorize_mult(column, dictionary, file=None):
    """
    Handles vectorizing
    :param column:
    :param dictionary:
    :param file:
    :return:
    """
    newCol = column + "Num"
    df[newCol] = df[column].map(dictionary)
    if file is not None:
        df.to_csv('cleaned/{}.csv'.format(file))



vectorize_mult("USGMeasurement", {"No": 0, "Yes": 1}, "wellness")
