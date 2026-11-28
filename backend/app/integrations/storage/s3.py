from app.core.config import settings
from app.integrations.storage.base import ObjectStorageAdapter


class S3ObjectStorage(ObjectStorageAdapter):
    """Railway Bucket adapter using the S3-compatible boto3 API."""

    def __init__(self) -> None:
        import boto3

        kwargs: dict[str, object] = {}
        if settings.STORAGE_ENDPOINT_URL:
            kwargs["endpoint_url"] = settings.STORAGE_ENDPOINT_URL
        if settings.STORAGE_REGION:
            kwargs["region_name"] = settings.STORAGE_REGION
        if settings.STORAGE_ACCESS_KEY_ID and settings.STORAGE_SECRET_ACCESS_KEY:
            kwargs["aws_access_key_id"] = (
                settings.STORAGE_ACCESS_KEY_ID.get_secret_value()
            )
            kwargs["aws_secret_access_key"] = (
                settings.STORAGE_SECRET_ACCESS_KEY.get_secret_value()
            )
        self.client = boto3.client("s3", **kwargs)
        self.bucket = settings.STORAGE_BUCKET_NAME

    async def generate_presigned_upload_url(
        self,
        object_key: str,
        expires_in_seconds: int = 600,
        max_size_bytes: int = 15 * 1024 * 1024,
    ) -> str:
        return self.client.generate_presigned_post(
            self.bucket,
            object_key,
            Fields={"acl": "private"},
            Conditions=[
                {"acl": "private"},
                ["content-length-range", 1, max_size_bytes],
            ],
            ExpiresIn=expires_in_seconds,
        )["url"]

    async def generate_presigned_download_url(
        self, object_key: str, expires_in_seconds: int = 300
    ) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": object_key},
            ExpiresIn=expires_in_seconds,
        )

    async def check_object_exists(self, object_key: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket, Key=object_key)
            return True
        except Exception:
            return False

    async def delete_object(self, object_key: str) -> bool:
        try:
            self.client.delete_object(Bucket=self.bucket, Key=object_key)
            return True
        except Exception:
            return False
