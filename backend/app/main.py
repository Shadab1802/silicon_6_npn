from fastapi import FastAPI
import uvicorn
from api.v1 import home

app = FastAPI()

#Includes Routers
app.include_router(home.router,prefix="/api",tags=["info"])

@app.get("/")
def root():
    return {"message": "Welcome to API"}

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)