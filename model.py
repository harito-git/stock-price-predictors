import torch
import torch.nn as nn
import torch.optim as optim

class StockPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(5, 10)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(10, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

class StockModel:
    def __init__(self):
        self.model = StockPredictor()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.loss_fn = nn.MSELoss()

    def predict(self, recent_prices):
        self.model.eval()
        with torch.no_grad():
            x = torch.tensor([recent_prices], dtype=torch.float32)
            return self.model(x).item()

    def train_step(self, inputs, targets):
        self.model.train()
        self.optimizer.zero_grad()
        outputs = self.model(inputs)
        loss = self.loss_fn(outputs, targets)
        loss.backward()
        self.optimizer.step()
        return loss.item()
