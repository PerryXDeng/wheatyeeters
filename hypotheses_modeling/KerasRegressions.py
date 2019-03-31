import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score


def r2_(y, pred):
  ybar = np.sum(y) / len(y)
  ssreg = np.sum((pred - ybar)**2)
  sstot = np.sum((y - ybar)**2)
  return ssreg/sstot


def time_series_sigmoid_classification(dataset, k, n0, x_columns, y_columns):
  inp = dataset[x_columns]
  out = dataset[y_columns]
  col = "day"
  x = []
  y = []
  input_shape = 0
  output_shape = 0
  for player in out["playerID"].unique():
    XPlayer = inp[inp["playerID"] == player]
    YPlayer = out[out["playerID"] == player]
    for day in YPlayer[col][n0 - 1:]:
      prev = day - k
      xprev = XPlayer[XPlayer[col] == prev].drop(columns=[col, "playerID"]).to_numpy()
      if xprev.shape[0] != 1:
        continue
      else:
        xprev = xprev[0, :]
      yt = YPlayer[YPlayer[col] == day].drop(columns=[col, "playerID"]).to_numpy()[0, :]
      if input_shape == 0:
        input_shape = xprev.shape[0]
      else:
        if input_shape != xprev.shape[0]:
          print("INCONSISTENT INPUT DIMENSION")
          exit(2)
      if output_shape == 0:
        output_shape = yt.shape[0]
      else:
        if output_shape != yt.shape[0]:
          print("INCONSISTENT OUTPUT DIMENSION")
          exit(2)
      x.append(xprev)
      y.append(yt)
  x = np.array(x)
  y = np.array(y)
  model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=[input_shape]),
    tf.keras.layers.Dense(output_shape, activation=tf.nn.softmax)
  ])
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy', 'categorical_accuracy'])
  model.fit(x, y, epochs=50)
  loss, accuracy = model.evaluate(x, y)
  print(loss, accuracy)
  return model.get_weights()


def time_series_dnn_classification(dataset, k, n0, x_columns, y_columns):
  inp = dataset[x_columns]
  out = dataset[y_columns]
  col = "day"
  x = []
  y = []
  input_shape = 0
  output_shape = 0
  for player in out["playerID"].unique():
    XPlayer = inp[inp["playerID"] == player]
    YPlayer = out[out["playerID"] == player]
    for day in YPlayer[col][n0 - 1:]:
      prev = day - k
      xprev = XPlayer[XPlayer[col] == prev].drop(columns=[col, "playerID"]).to_numpy()
      if xprev.shape[0] != 1:
        continue
      else:
        xprev = xprev[0, :]
      yt = YPlayer[YPlayer[col] == day].drop(columns=[col, "playerID"]).to_numpy()[0, :]
      if input_shape == 0:
        input_shape = xprev.shape[0]
      else:
        if input_shape != xprev.shape[0]:
          print("INCONSISTENT INPUT DIMENSION")
          exit(2)
      if output_shape == 0:
        output_shape = yt.shape[0]
      else:
        if output_shape != yt.shape[0]:
          print("INCONSISTENT OUTPUT DIMENSION")
          exit(2)
      x.append(xprev)
      y.append(yt)
  x = np.array(x)
  y = np.array(y)
  model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, input_dim=input_shape,activation=tf.nn.softmax),
    tf.keras.layers.Dense(output_shape, input_dim=32, activation=tf.nn.softmax)
  ])
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy', 'categorical_accuracy'])
  print(output_shape)
  model.fit(x, y, epochs=50)
  loss, accuracy = model.evaluate(x, y)
  print(x.shape)
  print(y.shape)
  print(loss, accuracy)
  return model.get_weights()

def time_series_linear_regression(dataset, k, n0, x_columns, y_columns):
  inp = dataset[x_columns]
  out = dataset[y_columns]
  col = "day"
  x = []
  y = []
  input_shape = 0
  output_shape = 0
  for player in out["playerID"].unique():
    XPlayer = inp[inp["playerID"] == player]
    YPlayer = out[out["playerID"] == player]
    for day in YPlayer[col][n0 - 1:]:
      prev = day - k
      xprev = XPlayer[XPlayer[col] == prev].drop(columns=[col, "playerID"]).to_numpy()
      if xprev.shape[0] != 1:
        continue
      else:
        xprev = xprev[0, :]
      yt = YPlayer[YPlayer[col] == day].drop(columns=[col, "playerID"]).to_numpy()[0, :]
      if input_shape == 0:
        input_shape = xprev.shape[0]
      else:
        if input_shape != xprev.shape[0]:
          print("INCONSISTENT INPUT DIMENSION")
          exit(2)
      if output_shape == 0:
        output_shape = yt.shape[0]
      else:
        if output_shape != yt.shape[0]:
          print("INCONSISTENT OUTPUT DIMENSION")
          exit(2)
      x.append(xprev)
      y.append(yt)
  x = np.array(x)
  y = np.array(y)
  model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=[input_shape]),
    tf.keras.layers.Dense(output_shape)
  ])
  model.compile(optimizer='adam', loss='mean_squared_error', metrics=[tf.keras.metrics.mean_squared_error])
  model.fit(x, y, epochs=50, verbose=2)
  pred = model.predict(x)
  r2 = r2_(y, pred)
  hard_pred = model.predict(x[0])
  hard_out = np.matmul(x[0], [0.03589787, -0.03472298, 0.24109702, -0.10143519]) - 0.890594
  print(hard_pred, hard_out, y[0])
  return r2, model.get_weights()


def time_series_dnn_regressions(dataset, k, n0, x_columns, y_columns):
  inp = dataset[x_columns]
  out = dataset[y_columns]
  col = "day"
  x = []
  y = []
  input_shape = 0
  output_shape = 0
  for player in out["playerID"].unique():
    XPlayer = inp[inp["playerID"] == player]
    YPlayer = out[out["playerID"] == player]
    for day in YPlayer[col][n0 - 1:]:
      prev = day - k
      xprev = XPlayer[XPlayer[col] == prev].drop(columns=[col, "playerID"]).to_numpy()
      if xprev.shape[0] != 1:
        continue
      else:
        xprev = xprev[0, :]
      yt = YPlayer[YPlayer[col] == day].drop(columns=[col, "playerID"]).to_numpy()[0, :]
      if input_shape == 0:
        input_shape = xprev.shape[0]
      else:
        if input_shape != xprev.shape[0]:
          print("INCONSISTENT INPUT DIMENSION")
          exit(2)
      if output_shape == 0:
        output_shape = yt.shape[0]
      else:
        if output_shape != yt.shape[0]:
          print("INCONSISTENT OUTPUT DIMENSION")
          exit(2)
      x.append(xprev)
      y.append(yt)
  x = np.array(x)
  y = np.array(y)
  model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=[input_shape]),
    tf.keras.layers.Dense(32, activation=tf.nn.softmax),
    tf.keras.layers.Dense(output_shape)
  ])
  model.compile(optimizer='adam', loss='mean_squared_error', metrics=[tf.keras.metrics.mean_squared_error])
  model.fit(x, y, epochs=100, verbose=2)
  loss, accuracy = model.evaluate(x, y)
  pred = model.predict(x)
  r2 = r2_(y, pred)
  return r2, model.get_weights()


def main():
  filename = "personal.csv"
  df = pd.read_csv(filename)
  x = ["day", "playerID", "sleepHoursSliding", "sleepHours", "sleepQuality", "acuteChronicRatio"]
  y = ["day", "playerID", "fatigueNorm"]
  k = 0
  n0 = 30
  r2, weights =  time_series_linear_regression(df, k, n0, x, y)
  print("r2")
  print(r2)
  print("weights")
  print(weights)


if __name__ == "__main__":
  main()
