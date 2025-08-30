from fastapi import FastAPI
import uvicorn
from backend.api.v1 import batch_predict, home,users,airlines

app = FastAPI()

#Includes Routers
app.include_router(home.router,prefix="/api",tags=["info"])
app.include_router(users.router,prefix="/api",tags=["predicting from model"])
app.include_router(batch_predict.router,prefix="/api",tags=["predicting from model"])
app.include_router(airlines.router,prefix="/api",tags=["Fetching data"])
@app.get("/")
def root():
    return {"message": "Welcome to API"}

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)