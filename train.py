import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import numpy as np
import requests
from sklearn.model_selection import train_test_split
from getPlaylistMetrics import getMetrics

def train_model(token, playlist_id): 
  class Model(nn.Module):

    def __init__(self, in_nodes=5, h1=20, h2=20, out_nodes=4):
      super().__init__()
      self.fc1 = nn.Linear(in_nodes, h1)
      self.fc2 = nn.Linear(h1, h2)
      self.out = nn.Linear(h2, out_nodes)

    def forward(self, x):
      x = F.relu(self.fc1(x))
      x = F.relu(self.fc2(x))
      x = F.relu(x)
      return self.out(x)
    
  model = Model()
  torch.manual_seed(47)

  ## get training playlist 
  moodUrl = 'C:/Users/benwa/OneDrive/Desktop/Book1.xlsx'
  df = pd.read_excel(moodUrl)
  df = df.drop(1, axis=1)

  headers = {
    'Authorization': f'Bearer {token}',
  }

  ## initialize the rest of the dataframe
  for i in range(5):
    df[i + 1] = 0.0

  metrics = getMetrics(playlist_id, headers)

  print(df.shape) 
  print(len(metrics))
  print(len(metrics[0]))

  for i in range(len(df)):
    for j in range(5): 
      df.iat[i, j + 1] = metrics[i][j]

  df[0] = df[0].replace('Hype', 0.0)
  df[0] = df[0].replace('Happy', 1.0)
  df[0] = df[0].replace('Chill', 2.0)
  df[0] = df[0].replace('Sad', 3.0)

  ## seperate inputs from outputs
  X = df.drop(0, axis=1).astype(np.float32)
  X = X.values.astype(np.float32)
  y = df[0].astype(np.float32)
  y = y.values.astype(np.float32)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=47)

  ## convert X features to float tensors 
  X_train = torch.FloatTensor(X_train)
  X_test = torch.FloatTensor(X_test)

  ## convert Y labels to tensors 
  y_train = torch.LongTensor(y_train)
  y_test = torch.LongTensor(y_test)

  ## set criteron to measure the error, optomizer, and learning rate 
  criterion = nn.CrossEntropyLoss()
  optimizer = torch.optim.Adam(model.parameters(), lr =0.001)

  ## train model 
  epochs = 100
  losses = []

  for i in range(epochs):
    # go forward and get a predicition
    y_pred = model.forward(X_train)
    
    # measure the error and keep track
    loss = criterion(y_pred, y_train)
    losses.append(loss.detach().numpy())

    ## print every 10 epoch 
    if i % 10 == 0:
      print(f'Epoch: {i} and loss: {loss}')

    ## back propogation - fine tune the weights 
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        y_pred = model(X_test)
        y_pred_prob = F.softmax(y_pred, dim=1)  # Convert logits to probabilities
        y_pred_class = torch.argmax(y_pred_prob, dim=1)  # Get the predicted classes

    # Print expected and predicted values
    print("\nExpected vs Predicted Values:")
    for true_label, predicted_label in zip(y_test.numpy(), y_pred_class.numpy()):
        print(f"Expected: {int(true_label)}, Predicted: {int(predicted_label)}")
