import pandas as pd

# read in CSV
df = pd.read_csv('cleaned/wellness.csv')


def vectorize_mult(column, dictionary, file=None):
    newCol = column + "Num"
    df[newCol] = df[column].map(dictionary)
    if file is not None:
        df.to_csv('cleaned/{}.csv'.format(file))


vectorize_mult("USGMeasurement", {"No": 0, "Yes": 1}, "wellness")

"""
for i, value in df["TrainingReadiness"].iteritems():
    if pd.notna(value):
        value = value.split("%")[0]
        value = float(value) * (1/100)
        value = round(value, 2)
        df.set_value(i, "TrainingReadinessNum", value)

        print(value)


df.to_csv('cleaned/{}.csv'.format("wellness"))
"""