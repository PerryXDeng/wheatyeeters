import pandas as pd
import numpy as np


def start_end_times(filename):
  df = pd.read_csv(filename)
  columnname = "Date"
  dt = pd.to_datetime(df[columnname], format="%Y-%m-%d")
  print()
  print(filename)
  print("min")
  print(dt.min())
  print("max")
  print(dt.max())
  return dt.min()


def timeframes():
  start_end_times("data/rpe.csv")
  start_end_times("data/games.csv")
  start_end_times("data/wellness.csv")


def normalize_time_series(filename, start):
  df = pd.read_csv(filename)
  columnname = "Date"
  dt = pd.to_datetime(df[columnname], format="%Y-%m-%d")
  df["TimeSinceAugFirst"] = (dt - start).dt.days
  df.to_csv("cleaned/time_series_" + filename)


start = start_end_times("data/rpe.csv")
normalize_time_series("cleaned/rpe.csv", start)
