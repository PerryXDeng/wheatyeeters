import pandas as pd

# read in CSV
df = pd.read_csv('cleaned/wellness.csv')

# print out column uniques
print(df["Illness"].unique())

# make dictionary of unique values and their associated values
illness = {'No': 0, 'Slightly Off': 0.5, 'Yes': 1}

# iterate through new column vectorize
df["IllnessNum"] = [illness[item] for item in df["Illness"]]

df.to_csv('cleaned/wellness.csv')

print(df["Illness"])
print(df["IllnessNum"])
