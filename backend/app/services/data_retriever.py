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