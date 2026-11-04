import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))


def nettoyer(texte: str) -> str:
    texte = texte.lower()
    texte = re.sub(r"https?://\S+|www\.\S+", " ", texte)    
    texte = re.sub(r"@\w+|u/\w+|r/\w+", " ", texte)         
    texte = re.sub(r"[^a-z0-9\s]", " ", texte)              
    return " ".join(w for w in texte.split() if w not in stop_words)