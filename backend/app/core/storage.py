import minio
from .config import get_settings
import uuid
from fastapi import UploadFile
from pathlib import Path

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
    else:
        print(f"Bucket {bucket_name} existed!")

def upload_file(client: minio.Minio, file: UploadFile, folder, old_url: str):
    _ensure_bucket(client, settings.minio_bucket)

    if old_url:
        object_name = old_url.split(f"{settings.minio_bucket}/")[-1]
        delete_file(client, object_name)

    file_extension = Path(file.filename).suffix

    # create an unique name for the file before upload it
    object_name = f"{folder}/{uuid.uuid4()}{file_extension}"

    try: 
        client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=object_name,
            data=file.file,
            length=-1,
            content_type=file.content_type
        )
        print("Uploading file successfully!")

        return {"public_url": f"{settings.minio_endpoint}/{settings.minio_bucket}/{object_name}"}
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