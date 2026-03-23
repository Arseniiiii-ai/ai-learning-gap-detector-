import torch

def build_tensor(encoded_sequences):
    tensor_data = []
    for student, seq in encoded_sequences.items():
        tensor_seq = torch.tensor(seq, dtype=torch.float32)
        tensor_data.append(tensor_seq)
    return tensor_data