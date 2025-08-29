# from backend.app.utils.model_fetcher import classifier2 ## including model from fetched file 
from backend.app.models.input_model import Input ## user input module
from fastapi import APIRouter

#creating router instance
router = APIRouter()

@router.post('/user')
def get_response(input: Input):
    #convert input to right shape for model
    features=[[input.a,input.b,input.c,input.d]]
    # delayed=classifier2.predict(features)[0]
    delayed=1

    if(delayed):
        return {"delayed":delayed,"message":"this will be masssage"}
    else:
        return {"delayed":delayed}