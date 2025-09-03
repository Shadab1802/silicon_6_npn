# backend/app/services/data_retriver.py

"""
It is the funtion that commmunicate to s3 bucket and fetch the basic data's like airlines.json, states.json for basic fuction of backend required at runtime.
For now the basic data even airport.json is stored at s3 bucket so we can just update their without affecting the backend code.
As these data is dependent on the model training data , so storing their seemed convenient 

"""

from app.core.s3 import get_s3_resource

class DataRetriever:
    def __init__(self, bucket: str):
        self.bucket = get_s3_resource().Bucket(bucket)
    
    def get_airlines(self):
        response = self.bucket.Object(key="backendData/airlines.json").get()
        return response["Body"].read().decode("utf-8")
    
    def get_states(self):
        response = self.bucket.Object(key="backendData/states.json").get()
        return response["Body"].read().decode("utf-8")