import torch
import torch.nn as nn


class DKTModel(nn.Module):
    def __init__(self, input_size, hidden_size=100):
        super(DKTModel, self).__init__()
        self.rnn = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_size, input_size // 2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.rnn(x)
        out = self.fc(out)
        out = self.sigmoid(out)

        return out