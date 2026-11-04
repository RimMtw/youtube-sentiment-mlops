import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import resample


def equilibre(df):
    n = df["label"].value_counts().min()
    return df.groupby("label").sample(n=n, random_state=42)

df = pd.read_csv("data/processed/clean.csv").dropna()
df_equi = equilibre(df)

def split(df):
    return train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])

train, test = split(df_equi)
train.to_csv("data/processed/train.csv", index=False)
test.to_csv("data/processed/test.csv", index=False)
print("Train :\n", train["label"].value_counts())
print("Test :\n", test["label"].value_counts())