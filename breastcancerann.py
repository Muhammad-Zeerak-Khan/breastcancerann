# -*- coding: utf-8 -*-
"""BreastCancerAnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i3_cwsOWUp5XInewmKJsr9hmsRMJZnxj
"""

import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from torch import nn, optim
import torch.nn.functional as F
import seaborn as sns
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer()
 df = pd.DataFrame(data = data.data,columns = data.feature_names)
 df['target'] = data.target
 df.head()

df['target'].value_counts()

X = df.drop('target',axis=1)
y = df['target']
X,y

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =0.2, random_state= 42)

X_train.shape

X_train = torch.from_numpy(X_train.to_numpy()).float()
y_train = torch.squeeze(torch.from_numpy(y_train.to_numpy()).float())


X_test = torch.from_numpy(X_test.to_numpy()).float()
y_test = torch.squeeze(torch.from_numpy(y_test.to_numpy()).float())

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

class Net(nn.Module):
  def __init__(self, n_features):
    super(Net,self).__init__()
    self.fc1 = nn.Linear(n_features, 80)
    self.fc2 = nn.Linear(80,50)
    self.fc3= nn.Linear(50,35)
    self.fc4 = nn.Linear(35,15)
    self.fc5 = nn.Linear(15,5)
    self.fc6 = nn.Linear(5,1)

  def forward(self, x):
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = F.relu(self.fc3(x))
    x = F.relu(self.fc4(x))
    x = F.relu(self.fc5(x))
    return torch.sigmoid(self.fc6(x))

net = Net(X_train.shape[1])

criterion = nn.BCELoss()

optimizer = optim.Adam(net.parameters(), lr = 0.0005)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device

X_train = X_train.to(device)
y_train = y_train.to(device)

X_test = X_test.to(device)
y_test = y_test.to(device)

net = net.to(device)

criterion = criterion.to(device)

def calculate_accuracy(y_true, y_pred):
  predicted = y_pred.ge(0.5).view(-1)
  return (y_true == predicted).sum().float() / len(y_true)

def round_tensor(t, decimal_places = 3):
  return round(t.item(), decimal_places)

for epoch in range(1000):
  
  y_pred = net(X_train)

  y_pred = torch.squeeze(y_pred)
  train_loss = criterion(y_pred, y_train)

  if epoch % 100 == 0:
    train_acc = calculate_accuracy(y_train, y_pred)

    y_test_pred = net(X_test)
    y_test_pred = torch.squeeze(y_test_pred)

    test_loss = criterion(y_test_pred, y_test)

    test_acc =calculate_accuracy(y_test, y_test_pred)
    print(
        f"""epoch {epoch}
        Train set - Loss: {round_tensor(train_loss)}, accuracy:{round_tensor(train_acc)}
        Test set - Loss: {round_tensor(test_loss)}, accuracy:{round_tensor(test_acc)}
        """
    )
    optimizer.zero_grad()
    train_loss.backward()
    optimizer.step()

X_test.shape

y_test.shape

y_pred = net(X_test)

y_pred = y_pred.ge(.5).view(-1).cpu()
y_pred

classes = ['True','False']

y_pred = net(X_test)

y_pred = y_pred.ge(.5).view(-1).cpu()
y_test = y_test.cpu()

print(classification_report(y_test, y_pred, target_names=classes))

