from backend.app.core.s3 import get_s3_resource
import pickle
class DataRetriever:
    def __init__(self, bucket: str):
        self.bucket = get_s3_resource().Bucket(bucket)
    
    def get_airlines(self):
        response = self.bucket.Object(key="backendData/airlines.json").get()
        return response["Body"].read().decode("utf-8")
    
    def load_pickle(self, key: str="ProdictionModels/model.pkl"):
        obj = self.bucket.Object(key).get()
        body = obj["Body"].read()
        return pickle.loads(body)