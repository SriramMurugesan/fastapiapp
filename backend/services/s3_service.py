import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# boto3 automatically reads these environment variables:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
s3_client = boto3.client("s3")

BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME", "talentspark-resumes-bucket")


def upload_file_to_s3(file_bytes: bytes, filename: str, content_type: str) -> str:
    """
    Upload a file to S3 and return a pre-signed URL so the user can view it.
    
    Steps:
    1. Upload the file bytes to S3
    2. Generate a pre-signed URL (valid for 1 hour) so the student can open the file
    3. Return the URL
    """
    # 1. Upload file to S3
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,          # the file path inside the bucket
        Body=file_bytes,       # the actual file content
        ContentType=content_type
    )

    # 2. Generate a pre-signed URL (expires in 3600 seconds = 1 hour)
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": filename},
        ExpiresIn=3600
    )

    return url
