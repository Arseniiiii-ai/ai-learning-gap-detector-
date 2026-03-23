import pandas as pd

def load_data(path):
    df = pd.read_csv(path, encoding = "latin-1", low_memory = False)
    df = df[["user_id", "skill_id", "correct"]]
    df = df.dropna()
    return df

def topic_accuracy(df):
    accuracy = df.groupby(["user_id", "skill_id"])["correct"].mean().reset_index()
    accuracy.rename(columns = {"correct": "accuracy"}, inplace = True)
    return accuracy

if __name__ == "__main__":
    df = load_data("data/assistments.csv")
    acc = topic_accuracy(df)
    print(acc.head())