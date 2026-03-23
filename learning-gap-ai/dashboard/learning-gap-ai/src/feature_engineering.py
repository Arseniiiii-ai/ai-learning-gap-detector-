import pandas as pd

def build_features(df):
    features = df.groupby(["user_id", "skill_id"]).agg(
        accuracy=("correct", "mean"),
        avg_time=("ms_first_response", "mean"),
        attempts=("attempt_count", "mean")
    ).reset_index()
    features["accuracy"] = features["accuracy"].round(2)
    features["avg_time"] = features["avg_time"].astype(int)
    return features


if __name__ == "__main__":
    df = pd.read_csv("data/assistments.csv", encoding="latin-1", low_memory=False)
    df = df.dropna()
    features = build_features(df)
    print(features.head())