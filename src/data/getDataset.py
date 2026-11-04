import pandas as pd
from pathlib import Path

url="https://raw.githubusercontent.com/Himanshu-1703/reddit-sentiment-analysis/refs/heads/main/data/reddit.csv"
output=Path("data/raw/reddit.csv")

dataset=pd.read_csv(url)
dataset.to_csv(output, index=False)
print("nbr de lignes dans le dataset:", len(dataset))
print("categories :", dataset['category'].value_counts())