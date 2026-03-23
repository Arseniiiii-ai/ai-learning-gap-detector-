import sys
import os 
import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader, TensorDataset 
from src.dkt_data_prep import load_assistments, build_sequences, encode_sequences
from src.skill_encoder import build_skill_map
from src.dkt_dataset import build_dkt_dataset
from models.dkt_model import DKTModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def train():
    
    print("Loading dataset")
    
    df = load_assistments("data/assistments.csv")
    sequences = build_sequences(df)
    skill_map = build_skill_map(df)
    encoded = encode_sequences(sequences, skill_map)
    num_skills = len(skill_map)

    X, y = build_dkt_dataset(encoded, num_skills)
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size = 256, shuffle = True)
    model = DKTModel(input_size=num_skills * 2)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 5

    for epoch in range(epochs):
        total_loss = 0
        for batch_X, batch_y in dataloader:
            batch_X = batch_X.unsqueeze(1)
            optimizer.zero_grad()
            outputs = model(batch_X).squeeze()
            loss = criterion(outputs[:,0], batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {total_loss:.4f}")
    torch.save(model.state_dict(), "models/dkt_model.pth")
    print("Model saved")
    
if __name__ == "__main__":
    train()
            
