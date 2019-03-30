from sklearn import linear_model
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score


def k_days_into_future_regression(X, y, k, n0):
  """
  linear regression that returns the fitted weights as well as metrics
  :param X: x timeseries dataframe (very clean, no unamed columns), multidimensional rows
  :param y: y timeseries dataframe (very clean, no unamed columns), scalar rows
  :param k: days predicting in advance
  :param n0: ignoring the first n0 days
  :return: intercept, slopes, correlation, mean squared error
  """
  col = "TimeSinceAugFirst"
  inp = []
  out = []
  for day in y[col][n0 - 1:]:
    prev = day - k
    xprev = X[X[col] == prev].drop(columns=[col]).to_numpy()
    if xprev.shape[0] != 1:
      continue
    else:
      xprev = xprev[0, :]
    yt = y[y[col] == day].drop(columns=[col]).to_numpy()[0, :]
    inp.append(xprev)
    out.append(yt)
  regr = linear_model.LinearRegression()
  regr.fit(inp, out)
  predictions = regr.predict(inp)
  mse = mean_squared_error(out, predictions)/(len(out) - 2)
  r2 = r2_score(out, predictions)
  return regr.intercept_, regr.coef_, r2, mse


def main():
  fatigueSums = pd.read_csv("fatigue_total_sum.csv")
  performance = pd.read_csv("../data_preparation/cleaned/expSmoothWorkAndFatigueData.csv", index_col=0).drop(columns=["totalWork", "averageWorkLoad", "smoothedFatigueData"])
  print(k_days_into_future_regression(fatigueSums, performance, 0, 1))


if __name__ == "__main__":
  main()
