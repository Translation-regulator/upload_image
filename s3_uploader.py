import boto3
import uuid
import os
from fastapi import UploadFile
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def upload_image_to_s3(file: UploadFile) -> str:
    key = f"uploads/{uuid.uuid4().hex}_{file.filename}"
    s3.upload_fileobj(
        file.file,
        S3_BUCKET,
        key,
        ExtraArgs={
            "ContentType": file.content_type
        }
    )
    return f"{CLOUDFRONT_URL.rstrip('/')}/{key}"
