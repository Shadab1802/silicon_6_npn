from fastapi import APIRouter
import os
from backend.app.services.data_retriever import DataRetriever
from dotenv import load_dotenv
load_dotenv()
router = APIRouter()

retriever = DataRetriever(bucket=os.getenv("BUCKET_NAME"))

@router.get("/airlines")
def airlines():
    airlines_jason = retriever.get_airlines()

    return {"airlines":airlines_jason}