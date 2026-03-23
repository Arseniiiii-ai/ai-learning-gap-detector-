import pandas as pd
from src.skill_encoder import build_skill_map

def load_assistments(path):
    df = pd.read_csv(path, encoding="latin-1", low_memory=False)
    df = df[["user_id", "skill_id", "skill_name", "correct"]]
    df = df.dropna(subset=["skill_id"])
    df = df.dropna(subset=["skill_name"])
    df["skill_id"] = df["skill_id"].astype(int)

    return df

def build_sequences(df):
    sequences = {}
    for _, row in df.iterrows():
        user = row["user_id"]
        if user not in sequences:
            sequences[user] = []
        sequences[user].append((row["skill_id"], row["correct"]))

    return sequences

def encode_sequences(sequences, skill_map):
    encoded = {}
    for student, answers in sequences.items():
        encoded[student] = []
        for skill, correct in answers:
            skill_id = skill_map.get(skill)
            if skill_id is not None:
                encoded[student].append((skill_id, correct))
    return encoded

if __name__ == "__main__":
    df = load_assistments("data/assistments.csv")
    sequences = build_sequences(df)
    skill_map = build_skill_map(df)
    encoded = encode_sequences(sequences, skill_map)
    
    for student, seq in list(encoded.items())[:3]:
        print("Student:", student)
        print("Encoded:", seq[:10])
        print()
