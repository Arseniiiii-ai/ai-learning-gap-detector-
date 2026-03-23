import torch
def build_dkt_dataset(encoded_sequences, num_skills):
    X = []
    y = []
    
    for student, seq in encoded_sequences.items():
        if len(seq) < 2:
            continue
        
        for i in range(len(seq) - 1):
            skill, correct = seq[i]
            next_skill, next_correct = seq[i + 1]
            input_vector = torch.zeros(num_skills * 2, dtype=torch.float32)
            index = skill + correct * num_skills
            if index < num_skills * 2:
                input_vector[index] = 1
                X.append(input_vector)
                y.append(next_correct)

    if len(X) == 0:
        raise ValueError("Dataset is empty after preprocessing")
    X = torch.stack(X)
    y = torch.tensor(y, dtype=torch.float32)

    return X, y