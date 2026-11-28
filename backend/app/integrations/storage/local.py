from app.integrations.storage.base import ObjectStorageAdapter


class InMemoryObjectStorage(ObjectStorageAdapter):
    """Safe local fallback used when Railway/S3 credentials are absent."""

    objects: dict[str, bytes] = {}

    async def put(self, object_key: str, content: bytes) -> None:
        self.objects[object_key] = content

    async def get(self, object_key: str) -> bytes | None:
        return self.objects.get(object_key)

    async def generate_presigned_upload_url(
        self,
        object_key: str,
        expires_in_seconds: int = 600,
        max_size_bytes: int = 15 * 1024 * 1024,
    ) -> str:
        return f"/local-storage/{object_key}"

    async def generate_presigned_download_url(
        self, object_key: str, expires_in_seconds: int = 300
    ) -> str:
        return f"/local-storage/{object_key}"

    async def check_object_exists(self, object_key: str) -> bool:
        return object_key in self.objects

    async def delete_object(self, object_key: str) -> bool:
        return self.objects.pop(object_key, None) is not None


local_storage = InMemoryObjectStorage()
