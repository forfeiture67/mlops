from torch import nn


class DenseBlock(nn.Module):
    def __init__(self, in_features, hidden):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(in_features, hidden), nn.ReLU())

    def forward(self, x):
        return self.net(x)


class DigitsClassifier(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        if hidden < 1:
            raise ValueError("hidden must be positive")
        self.net = nn.Sequential(DenseBlock(64, hidden), nn.Linear(hidden, 10))

    def forward(self, x):
        return self.net(x)
