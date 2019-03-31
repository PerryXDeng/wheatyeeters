from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
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


def standard_lr(x, y):
  # Standard linear regression formula, gives back params and r2
  regr = linear_model.LinearRegression()
  regr.fit(x, y)
  predictions = regr.predict(x)
  mse = mean_squared_error(y, predictions) / (len(y) - 2)
  r2 = r2_score(y, predictions)
  return regr.intercept_, regr.coef_, r2, mse


def poly_regression(x, y, degree):
  # Polynomial regression with nth degree, gives back rmse and r2
  polynomial_features = PolynomialFeatures(degree=degree)
  x_poly = polynomial_features.fit_transform(x)

  model = linear_model.LinearRegression()
  model.fit(x_poly, y)
  y_poly_pred = model.predict(x_poly)

  rmse = np.sqrt(mean_squared_error(y, y_poly_pred))
  r2 = r2_score(y, y_poly_pred)
  return rmse, r2


def main():
  file = open("ryan_regressions.txt", 'w')
  player = pd.read_csv("../data_preparation/cleaned/personal.csv", index_col=0)

  for name, value in player.iteritems():
    if name == "day":
      continue

    for j in range(1, 17):
      ply = player[player['playerID'] == j]
      x = ply[['fatigueNorm', 'day']]
      y = ply[name]

      lr = standard_lr(x, y)
      poly = poly_regression(x, y, 3)
      if .9 > lr[2] > .4 or .9 > poly[1] > .4:
        file.write("Player {} for {}\n".format(j, name))
        file.write("{}\n".format(lr))
        file.write("{}\n\n".format(poly))


if __name__ == "__main__":
  main()
