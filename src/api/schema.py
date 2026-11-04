from typing import List
from pydantic import BaseModel, Field


class BatchRequest(BaseModel):
    comments: List[str] = Field(..., min_length=1, max_length=500)


class Prediction(BaseModel):
    comment: str
    label: int    


class BatchResponse(BaseModel):
    predictions: List[Prediction]
    stats: dict