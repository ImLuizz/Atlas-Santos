from app.core.config import Settings


def test_settings_default_values():
    custom_settings = Settings()
    assert custom_settings.APP_NAME == "Atlas Santos API"
    assert custom_settings.DEFAULT_PHOTO_QUOTA == 20
    assert custom_settings.MAX_UPLOAD_SIZE_MB == 15
    assert custom_settings.RESERVATION_TTL_MINUTES == 30
    assert custom_settings.PRESIGNED_UPLOAD_TTL_MINUTES == 10
    assert custom_settings.PRESIGNED_DOWNLOAD_TTL_MINUTES == 5


def test_settings_environment_override():
    custom = Settings(ENVIRONMENT="staging", PORT=9000, DEBUG=False)
    assert custom.ENVIRONMENT == "staging"
    assert custom.PORT == 9000
    assert custom.DEBUG is False


def test_railway_database_url_preserves_encoded_password():
    url = "postgresql://example:test%40localhost@db/atlas"
    assert Settings(DATABASE_URL=url).DATABASE_URL == url.replace(
        "postgresql://", "postgresql+psycopg://"
    )
