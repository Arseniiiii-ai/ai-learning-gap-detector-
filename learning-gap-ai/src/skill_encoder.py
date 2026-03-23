import pandas as pd

def build_skill_map(df):
    df = df.dropna(subset=["skill_id"])
    df["skill_id"] = df["skill_id"].astype(int)
    skills = df["skill_id"].unique()
    skill_map = {skill: i for i, skill in enumerate(skills)}
    return skill_map

def build_skill_lookup(df):
    lookup = {}
    for _, row in df.iterrows():
        if pd.notna(row["skill_id"]) and pd.notna(row["skill_name"]):
            lookup[int(row["skill_id"])] = row["skill_name"]
    return lookup

if __name__ == "__main__":
    df = pd.read_csv("data/assistments.csv", encoding="latin-1", low_memory=False)
    skill_map = build_skill_map(df)
    print("Number of skills:", len(skill_map))
    print("Example mapping:")
    for k, v in list(skill_map.items())[:10]:
        print(k, "→", v)