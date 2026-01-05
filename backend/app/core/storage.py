import minio
from minio.error import S3Error
from .config import get_settings
import uuid
from fastapi import UploadFile
from pathlib import Path
import json

# load setting from pre-defined configs
settings = get_settings()

# create Minio client
def get_minio_client():
    client = minio.Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False # add this cause we are using http
    )

    return client

def _ensure_bucket(client: minio.Minio, bucket_name: str):
    # ensure the bucket exist. If not then create a new one.
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Created bucket name: {bucket_name}")
        
        # Set bucket policy to public read
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }
        try:
            client.set_bucket_policy(bucket_name, json.dumps(policy))
            print(f"Bucket {bucket_name} set to public read")
        except S3Error as e:
            print(f"Error setting bucket policy: {e}")
    else:
        print(f"Bucket {bucket_name} existed!")
        # Đảm bảo policy được set ngay cả khi bucket đã tồn tại
        try:
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                    }
                ]
            }
            client.set_bucket_policy(bucket_name, json.dumps(policy))
        except S3Error as e:
            print(f"Warning: Could not set bucket policy: {e}")

def upload_file(client: minio.Minio, file: UploadFile, folder, old_url: str):
    _ensure_bucket(client, settings.minio_bucket)

    if old_url:
        object_name = old_url.split(f"{settings.minio_bucket}/")[-1]
        delete_file(client, object_name)

    file_extension = Path(file.filename).suffix

    # create an unique name for the file before upload it
    object_name = f"{folder}/{uuid.uuid4()}{file_extension}"

    try:
        # Read file content to get size
        file_content = file.file.read()
        file_size = len(file_content)

        # Reset file pointer to beginning
        file.file.seek(0)

        client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=object_name,
            data=file.file,
            length=file_size,
            content_type=file.content_type
        )
        print("Uploading file successfully!")

        return {"public_url": f"{settings.minio_public_url}/{settings.minio_bucket}/{object_name}"}
    except Exception as e:
        print(f"Error while uploading file: {e}")
        return None

def delete_file(client: minio.Minio, object_name):
    try:
        client.remove_object(
            bucket_name=settings.minio_bucket,
            object_name=object_name
        )

    except Exception as e:
        print(f"Error while deleting file: {e}")