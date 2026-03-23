import torch 
from models.dkt_model import DKTModel

def load_model(num_skills):
    model = DKTModel(input_size = num_skills * 2)
    model.load_state_dict(torch.load("models/dkt_model.pth"))
    model.eval()
    return model 

def predict_student_knowledge(model, encoded_sequences, num_skills):
    knowledge = {}
    for student, seq in encoded_sequences.items():
        inputs = []
        for skill, correct in seq:
            vector = torch.zeros(num_skills * 2)
            index = skill + correct * num_skills
            vector[index] = 1
            inputs.append(vector)
            
        if len(inputs) == 0:
            continue
        
        X = torch.stack(inputs).unsqueeze(0)
        
        with torch.no_grad():
            preds = model(X)
            
        knowledge[student] = preds[0, -1].tolist()
        
    return knowledge 