import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.utils.multiclass import unique_labels
from matplotlib import pyplot as plt
from sklearn.metrics import *


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

    one_hot = [0, 0, 0, 0]
    one_hot[index] = 1
    return one_hot


def plot_confusion_matrix(y_true, y_pred, classes, cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    title = "Confusion Matrix"

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


def get_trainset(batch_size, dataset, k, n0, x_columns, y_columns):
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

    randn_1 = np.random.randint(1, 5200)
    x = torch.FloatTensor(x)
    y = torch.LongTensor(y)
    if batch_size:
        x = x.narrow(0, randn_1, 125)
        y = y.narrow(0, randn_1, 125)
    return x, y


def time_series_sigmoid_classification(steps, dataset, k, n0, x_columns, y_columns, labels):
    net = Net(4)
    optimizer = optim.Adam(net.parameters(), lr=.03)
    loss = nn.CrossEntropyLoss()

    x, y = get_trainset(False, dataset, k, n0, x_columns, y_columns)
    accuracy(net, x, y)

    for step in range(steps):
        optimizer.zero_grad()

        x, y = get_trainset(True, dataset, k, n0, x_columns, y_columns)
        pred = net(x)
        net_loss = loss(pred, torch.max(y, 1)[1])
        net_loss.backward()
        optimizer.step()

        print("Loss at Step {}: {}".format(step, net_loss))

    x, y = get_trainset(False, dataset, k, n0, x_columns, y_columns)
    accuracy(net, x, y)


def accuracy(net, x, y):
    pred = net(x)
    pred = pred.detach().numpy()
    for row in range(len(pred)):
        pred[row] = get_argmax(pred[row])

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
    torch.save(net, "model_higher_lr.ckpt")
    return pred, y


def cm_plot(classes, dataset, k, n0, x_columns, y_columns):
    model = torch.load('model.ckpt')
    x, y = get_trainset(True, dataset, k, n0, x_columns, y_columns)
    pred = model(x)
    pred = pred.detach().numpy()
    for row in range(len(pred)):
        pred[row] = get_argmax(pred[row])

    print('F1: {}'.format(f1_score(y, pred > .5, average='micro')))
    plot_confusion_matrix(y, pred, classes)


def main():
    filename = "personal.csv"
    df = pd.read_csv(filename)
    x = ["day", "playerID", "fatigueSliding", "fatigueNorm", "sleepHoursSliding", "sleepQuality"]
    y = ["day", "playerID", "BestOutOfMyselfAbsolutely", "BestOutOfMyselfSomewhat", "BestOutOfMyselfNotAtAll",
         "BestOutOfMyselfUnknown"]
    # time_series_sigmoid_classification(50, df, 0, 30, x, y, y)
    cm_plot(
        ["BestOutOfMyselfAbsolutely", "BestOutOfMyselfSomewhat", "BestOutOfMyselfNotAtAll", "BestOutOfMyselfUnknown"],
        df, 0, 30, x, y)


if __name__ == '__main__':
    main()
