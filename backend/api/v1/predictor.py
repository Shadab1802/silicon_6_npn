from backend.app.models.model_fetcher import classifier2
import pickle
from backend.app.models.input_model import Input
from fastapi import APIRouter

#creating router instance
router = APIRouter()

@router.post("/predict")
def predict(input: Input):
    #convert input to right shape for model
    features=[[input.a,input.b,input.c,input.d]]
    output=classifier2.predict(features)
    return {'prediction':output.tolist()}