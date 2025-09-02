from app.utils.model_loader import model,encoders## including model from fetched file 
from app.schemas.input_model import Input ## user input module
from fastapi import APIRouter
import pandas as pd
from sklearn.preprocessing import RobustScaler, StandardScaler
from app.utils import sub_encoder
#creating router instance
router = APIRouter()

@router.post("/predict")
def predict(input: Input):
    
    model_input = sub_encoder(input)
    data = pd.DataFrame([model_input.dict()])

    #encoder logic 
    for col, le in encoders.items():
        data[col] = le.transform(data[col])
    
    robust_cols = ['DEPARTURE_TIME', 'DEPARTURE_DELAY'] #req in minitues
    standard_cols = ['MONTH', 'DAY_OF_WEEK','ARRIVAL_TIME'] #req in minitues
    robust_scaler = RobustScaler()
    standard_scaler = StandardScaler()
    data[robust_cols] = robust_scaler.transform(data[robust_cols])
    data[standard_cols] = standard_scaler.transform(data[standard_cols])

    output=model.predict(data)

    return{'Delayed':output.tolist()}