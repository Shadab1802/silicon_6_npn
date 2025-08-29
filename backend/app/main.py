from fastapi import FastAPI
import uvicorn
from backend.api.v1 import home,predictor

app = FastAPI()

#Includes Routers
app.include_router(home.router,prefix="/api",tags=["info"])
app.include_router(predictor.router,prefix="/api",tags=["predicting from model"])
@app.get("/")
def root():
    return {"message": "Welcome to API"}

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)