from abc import ABC, abstractmethod


class ObjectStorageAdapter(ABC):
    """Abstract port for S3-compatible object storage operations (Railway Buckets)."""

    @abstractmethod
    async def generate_presigned_upload_url(
        self, object_key: str, expires_in_seconds: int = 600, max_size_bytes: int = 15 * 1024 * 1024
    ) -> str:
        """Emits a short-lived presigned URL allowing direct client-to-bucket upload."""
        pass

    @abstractmethod
    async def generate_presigned_download_url(
        self, object_key: str, expires_in_seconds: int = 300
    ) -> str:
        """Emits a short-lived presigned URL for private read access."""
        pass

    @abstractmethod
    async def check_object_exists(self, object_key: str) -> bool:
        """Checks if an object was successfully uploaded and persisted."""
        pass

    @abstractmethod
    async def delete_object(self, object_key: str) -> bool:
        """Deletes an object permanently from storage."""
        pass

