# backend/app/main.py

"""
    This is the main entry point for backend
    here we have included various routes from api/v1 
    and a prefix /api is added..
    Our frontend was also communicating with backend via api only, they will just user dockerInternal Netwrok for 
    via http://backend/5000

"""

from fastapi import FastAPI
import uvicorn
from api.v1 import alternatives,batch_predict,predictor

app = FastAPI()

#Includes Routers

app.include_router(batch_predict.router,prefix="/api",tags=["predicting from model"])
# app.include_router(alternatives.router,prefix="/api",tags=["Alternatives flight if delayed"])
app.include_router(predictor.router,prefix="/api",tags="take one input and predict delayed or not")


@app.get("/")
def root():
    return {"message": "Welcome to API"}

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)