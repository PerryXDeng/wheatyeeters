import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd


class Net(nn.Module):
    def __init__(self, input_shape):
        super().__init__()
        self.fc1 = nn.Linear(input_shape, 8)
        self.fc2 = nn.Linear(8, 4)

    def forward(self, x):
        x = torch.sigmoid(self.fc1(x))
        return self.fc2(x)


def get_argmax(array):
    max = 0
    index = 0
    for i in range(len(array)):
        if array[i] > max:
            max = array[i]
            index = i

    return [index]


def get_trainset(dataset, k, n0, x_columns, y_columns):
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

    x = torch.FloatTensor(x)
    y = torch.LongTensor(y)
    return x, y


def time_series_sigmoid_classification(steps, dataset, k, n0, x_columns, y_columns):
  net = Net(1)
  optimizer = optim.Adam(net.parameters(), lr=.001)
  loss = nn.CrossEntropyLoss()

  for step in range(steps):
      optimizer.zero_grad()

      x, y = get_trainset(dataset, k, n0, x_columns, y_columns)
      pred = net(x)
      net_loss = loss(pred, torch.max(y, 1)[1])
      net_loss.backward()
      optimizer.step()

      print("Loss at Step {}: {}".format(step, net_loss))

  x, y = get_trainset(dataset, k, n0, x_columns, y_columns)
  accuracy(net, x, y)


def accuracy(net, x, y):
    pred = net(x)
    pred = pred.detach().numpy()

    total = len(pred)
    correct = 0
    for i in range(len(pred)):
        equal = True
        for j in range(len(pred[i])):
            if pred[i][j] != y[i][j]:
                equal = False
        if equal:
            correct += 1

    accuracy = (correct / total) * 100
    print("Accuracy for set: {}%".format(accuracy))
    torch.save(net, "model.ckpt")


def main():
  filename = "personal.csv"
  df = pd.read_csv(filename)
  x = ["day", "playerID", "fatigueSliding"]
  y = ["day", "playerID", "BestOutOfMyselfAbsolutely", "BestOutOfMyselfSomewhat", "BestOutOfMyselfNotAtAll", "BestOutOfMyselfUnknown"]
  time_series_sigmoid_classification(100, df, 0, 30, x, y)


if __name__ == '__main__':
    main()
