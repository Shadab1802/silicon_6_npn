# app/core/s3.py
import boto3
from backend.app.core.config import settings

def get_s3_resource():
    return boto3.resource(
        service_name="s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

def get_s3_client():
    return boto3.client(
        service_name="s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
