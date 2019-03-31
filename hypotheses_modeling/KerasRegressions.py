import tensorflow as tf
import pandas as pd
import numpy as np


def time_series_sigmoid_classification(X, Y, k, n0, x_columns, y_columns):
  inp = X[x_columns]
  out = Y[y_columns]
  col = "day"
  x = []
  y = []
  input_shape = 0
  output_shape = 0
  for player in Y["playerID"].unique():
    XPlayer = inp[inp["playerID"] == player]
    YPlayer = out[out["playerID"] == player]
    for day in YPlayer[col][n0 - 1:]:
      prev = day - k
      xprev = XPlayer[XPlayer[col] == prev].drop(columns=[col]).to_numpy()
      if xprev.shape[0] != 1:
        continue
      else:
        xprev = xprev[0, :]
      yt = YPlayer[YPlayer[col] == day].drop(columns=[col]).to_numpy()[0, :]
      if input_shape == 0:
        input_shape = xprev.shape[0]
      else:
        if input_shape != xprev.shape[0]:
          print("INCONSISTENT INPUT DIMENSION")
          exit(2)
      if input_shape == 0:
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
    tf.keras.layers.Flatten(input_shape=input_shape),
    tf.keras.layers.Dense(output_shape, activation=tf.nn.softmax)
  ])
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy', 'categorical_accuracy'])
  model.fit(x, y, epochs=100)
  loss, accuracy = model.evaluate(x, y)
  print(loss, accuracy)
  return model.get_weights()


def time_series_dnn_classification(X, Y, k, n0, x_columns, y_columns):
  inp = X[x_columns]
  out = Y[y_columns]
  col = "day"
  x = []
  y = []
  input_shape = 0
  output_shape = 0
  for player in Y["playerID"].unique():
    XPlayer = inp[inp["playerID"] == player]
    YPlayer = out[out["playerID"] == player]
    for day in YPlayer[col][n0 - 1:]:
      prev = day - k
      xprev = XPlayer[XPlayer[col] == prev].drop(columns=[col]).to_numpy()
      if xprev.shape[0] != 1:
        continue
      else:
        xprev = xprev[0, :]
      yt = YPlayer[YPlayer[col] == day].drop(columns=[col]).to_numpy()[0, :]
      if input_shape == 0:
        input_shape = xprev.shape[0]
      else:
        if input_shape != xprev.shape[0]:
          print("INCONSISTENT INPUT DIMENSION")
          exit(2)
      if input_shape == 0:
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
    tf.keras.layers.Flatten(input_shape=input_shape),
    tf.keras.layers.Dense(32, activation=tf.nn.softmax),
    tf.keras.layers.Dense(output_shape, activation=tf.nn.softmax)
  ])
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy', 'categorical_accuracy'])
  model.fit(x, y, epochs=100)
  loss, accuracy = model.evaluate(x, y)
  print(loss, accuracy)
  return model.get_weights()

def time_series_linear_regression(X, Y, k, n0, x_columns, y_columns):
  inp = X[x_columns]
  out = Y[y_columns]
  col = "day"
  x = []
  y = []
  input_shape = 0
  output_shape = 0
  for player in Y["playerID"].unique():
    XPlayer = inp[inp["playerID"] == player]
    YPlayer = out[out["playerID"] == player]
    for day in YPlayer[col][n0 - 1:]:
      prev = day - k
      xprev = XPlayer[XPlayer[col] == prev].drop(columns=[col]).to_numpy()
      if xprev.shape[0] != 1:
        continue
      else:
        xprev = xprev[0, :]
      yt = YPlayer[YPlayer[col] == day].drop(columns=[col]).to_numpy()[0, :]
      if input_shape == 0:
        input_shape = xprev.shape[0]
      else:
        if input_shape != xprev.shape[0]:
          print("INCONSISTENT INPUT DIMENSION")
          exit(2)
      if input_shape == 0:
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
    tf.keras.layers.Flatten(input_shape=input_shape),
    tf.keras.layers.Dense(output_shape)
  ])
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy', 'categorical_accuracy'])
  model.fit(x, y, epochs=100)
  loss, accuracy = model.evaluate(x, y)
  print(loss, accuracy)
  return model.get_weights()


def time_series_dnn_regressions(X, Y, k, n0, x_columns, y_columns):
  inp = X[x_columns]
  out = Y[y_columns]
  col = "day"
  x = []
  y = []
  input_shape = 0
  output_shape = 0
  for player in Y["playerID"].unique():
    XPlayer = inp[inp["playerID"] == player]
    YPlayer = out[out["playerID"] == player]
    for day in YPlayer[col][n0 - 1:]:
      prev = day - k
      xprev = XPlayer[XPlayer[col] == prev].drop(columns=[col]).to_numpy()
      if xprev.shape[0] != 1:
        continue
      else:
        xprev = xprev[0, :]
      yt = YPlayer[YPlayer[col] == day].drop(columns=[col]).to_numpy()[0, :]
      if input_shape == 0:
        input_shape = xprev.shape[0]
      else:
        if input_shape != xprev.shape[0]:
          print("INCONSISTENT INPUT DIMENSION")
          exit(2)
      if input_shape == 0:
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
    tf.keras.layers.Flatten(input_shape=input_shape),
    tf.keras.layers.Dense(32, activation=tf.nn.softmax),
    tf.keras.layers.Dense(output_shape)
  ])
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy', 'categorical_accuracy'])
  model.fit(x, y, epochs=100)
  loss, accuracy = model.evaluate(x, y)
  print(loss, accuracy)
  return model.get_weights()
