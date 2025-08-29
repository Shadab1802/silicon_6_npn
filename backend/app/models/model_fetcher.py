from backend.app.core.config import settings
import boto3, pickle

s3 = boto3.resource(
    service_name="s3",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key,
    aws_secret_access_key=settings.aws_secret_access_key,
)

obj = s3.Bucket("modelproduction1811").Object("classifier.pkl").get()
body = obj["Body"].read()
classifier2 = pickle.loads(body)
