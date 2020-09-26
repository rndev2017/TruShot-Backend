import uuid
import creds
from fastapi import APIRouter, File, UploadFile, HTTPException
from google.cloud.storage import Client, Blob
from google.cloud.exceptions import GoogleCloudError

storage_router = APIRouter()


def init_cloud_storage(project_id: str) -> Client:
    """ Intializes the Google Cloud Storage

    Args:
        project_id (str): Id of project in GCP

    Returns:
        storage_client (google.cloud.storage.Client): client to interface with Cloud Storage
    """

    # Generate storage client to access Storage buckets
    storage_client = Client(project=project_id)

    return storage_client


@storage_router.post("/upload")
async def upload_picture(file: UploadFile = File(None, media_type="image/jpeg")):
    try:

        content = await file.read()

        storage_client = Client(project=creds.project_id)
        bucket = storage_client.get_bucket(creds.bucket_id)

        img_uuid = str(uuid.uuid4())[0:6]
        blob = bucket.blob(img_uuid)

        blob.upload_from_string(data=content, content_type="image/jpeg")


        return {"detail": f"File {img_uuid} uploaded to {bucket.name}"}
    except GoogleCloudError as e:
        raise HTTPException(detail=str(e), status_code=500)


