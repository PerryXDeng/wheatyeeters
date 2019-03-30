import pandas as pd
import numpy as np


def vectorize_mult(column, dictionary, postfix, df, file=None):
  newCol = column + postfix
  df[newCol] = df[column].map(dictionary)
  if file is not None:
    df.to_csv('cleaned/{}.csv'.format(file))


csv = pd.read_csv("data/rpe.csv")
training = csv["Training"].unique()
session = csv["SessionType"].unique()
boms = csv["BestOutOfMyself"].unique()
print(training)
print(session)
print(boms)
vectorize_mult("Training", {"No": 0, "Yes": 1}, "", csv)

mapping = {"Mobility/Recovery": 1, "Game": 0, "Skills": 0, "Conditioning": 0,
           "Strength": 0, "Combat": 0, "Speed": 0, np.nan: 0}
vectorize_mult("SessionType", mapping, "Mobility/Recovery", csv)
mapping["Mobility/Recovery"] = 0
mapping["Game"] = 1
vectorize_mult("SessionType", mapping, "Game", csv)
mapping["Game"] = 0
mapping["Skills"] = 1
vectorize_mult("SessionType", mapping, "Skills", csv)
mapping["Skills"] = 0
mapping["Conditioning"] = 1
vectorize_mult("SessionType", mapping, "Conditioning", csv)
mapping["Conditioning"] = 0
mapping["Strength"] = 1
vectorize_mult("SessionType", mapping, "Strength", csv)
mapping["Strength"] = 0
mapping["Combat"] = 1
vectorize_mult("SessionType", mapping, "Combat", csv)
mapping["Combat"] = 0
mapping["Speed"] = 1
vectorize_mult("SessionType", mapping, "Speed", csv)
mapping["Speed"] = 0
mapping[np.nan] = 1
vectorize_mult("SessionType", mapping, "Unknown", csv)
mapping[np.nan] = 0

mapping = {"Not at all": 1, "Absolutely": 0, "Somewhat": 0, np.nan: 0}
vectorize_mult("BestOutOfMyself", mapping, "NotAtAll", csv)
mapping["Not at all"] = 0
mapping["Absolutely"] = 1
vectorize_mult("BestOutOfMyself", mapping, "Absolutely", csv)
mapping["Absolutely"] = 0
mapping["Somewhat"] = 1
vectorize_mult('BestOutOfMyself', mapping, "Somewhat", csv)
mapping["Somewhat"] = 0
mapping[np.nan] = 1
vectorize_mult('BestOutOfMyself', mapping, "Unknown", csv)
mapping[np.nan] = 0

csv.to_csv("cleaned/notnormalized_clean_rpe.csv")
