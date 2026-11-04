import joblib
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.schema import BatchRequest, BatchResponse, Prediction
from src.utils.prepros import nettoyer

ressources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    ressources["vectorizer"] = joblib.load("models/vectorizer.pkl")
    ressources["model"] = joblib.load("models/model.pkl")
    yield
    ressources.clear()


app = FastAPI(title="YouTube Sentiment API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": "model" in ressources}


@app.post("/predict_batch", response_model=BatchResponse)
def predict_batch(requete: BatchRequest):
    if "model" not in ressources:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    try:
        textes = [nettoyer(c) for c in requete.comments]
        X = ressources["vectorizer"].transform(textes)
        modele = ressources["model"]
        y_pred = modele.predict(X)
        if hasattr(modele, "predict_proba"):
            proba = modele.predict_proba(X)
        else: 
            s = modele.decision_function(X)
            e = np.exp(s - s.max(axis=1, keepdims=True))
            proba = e / e.sum(axis=1, keepdims=True)
        confiances = proba.max(axis=1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {e}")

    predictions = [
        Prediction(comment=c, label=int(y), confidence=round(float(p), 2))
        for c, y, p in zip(requete.comments, y_pred, confiances)
    ]
    
    total = len(predictions)
    counts = {s: sum(p.label == s for p in predictions) for s in (-1, 0, 1)}
    stats = {
        "total": total,
        "counts": counts,
        "percentages": {s: round(100 * n / total, 1) for s, n in counts.items()},
    }
    return BatchResponse(predictions=predictions, stats=stats)