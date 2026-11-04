import pandas as pd
from pathlib import Path
import nltk 
from nltk.corpus import stopwords

nltk.download("stopwords")

df = pd.read_csv("data/raw/reddit.csv").rename(columns={"clean_comment": "text", "category": "label"})
df = df[["text", "label"]].dropna()

df["text"] = df["text"].str.lower()
# filtre les lien (http, https, www)
df["text"] = df["text"].str.replace(r"https?://\S+|www\.\S+", " ", regex=True)   
# filtre les mentions (@username, u/username, r/subreddit)
df["text"] = df["text"].str.replace(r"@\w+|u/\w+|r/\w+", " ", regex=True)        
# filtre les caractères spéciaux 
df["text"] = df["text"].str.replace(r"[^a-z0-9\s]", " ", regex=True)               

stop = set(stopwords.words("english"))
df["text"] = df["text"].apply(lambda t: " ".join(w for w in t.split() if w not in stop))

df.to_csv("data/processed/clean.csv", index=False)