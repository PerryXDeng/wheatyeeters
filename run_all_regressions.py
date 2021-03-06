from sklearn import linear_model
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures


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
  x = x.reshape(-1, 1)
  y = y.reshape(-1, 1)
  regr = linear_model.LinearRegression()
  regr.fit(x, y)
  predictions = regr.predict(x)
  mse = mean_squared_error(y, predictions) / (len(y) - 2)
  r2 = r2_score(y, predictions)
  return regr.intercept_, regr.coef_, r2, mse


def poly_regression(x, y, degree):

  # Reshapes the models to be able to run regression on them
  x = x.reshape(-1, 1)
  y = y.reshape(-1, 1)

  # Polynomial regression with nth degree, gives back rmse and r2
  polynomial_features = PolynomialFeatures(degree=degree)
  x_poly = polynomial_features.fit_transform(x)

  model = linear_model.LinearRegression()
  model.fit(x_poly, y)
  y_poly_pred = model.predict(x_poly)

  rmse = np.sqrt(mean_squared_error(y, y_poly_pred))
  r2 = r2_score(y, y_poly_pred)
  return rmse, r2


def run_all_polynomials():
    # Reads in the neccessary csv file
    df = pd.read_csv('data_preparation/cleaned/personal.csv')
    regr = linear_model.LinearRegression()
    print("xVal, yVal, degree, r2, rmse")
    for i in range(3, 14):
        for j in range(1, 14 - i):
            mat = df[[df.columns[i], df.columns[i + j]]].values
            for d in range(1, 6):
                rmse, r2 = poly_regression(mat[:, 0], mat[:, 1], d)
                plt.figure(figsize=(6, 6))
                plt.xlabel(df.columns[i])
                plt.ylabel(df.columns[i + j])
                plt.title('r2: ' + str(r2) + 'degree: ' + str(d))
                plt.scatter(mat[:, 0], mat[:, 1])
                plt.savefig('personal_regression_info/' + df.columns[i] + '_vs_' + df.columns[i + j] + '_' + str(d) + '_degree.png')
                print(df.columns[i] + ', ' + df.columns[i + j] + ', ' + str(d) + ', ' + str(r2) + ', ' + str(rmse))
                plt.close()


# run_all_linears()
run_all_polynomials()
