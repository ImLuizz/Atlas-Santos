import base64
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta


def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token (e.g. for invitations or sessions)."""
    return secrets.token_urlsafe(length)


def hash_token(token: str) -> str:
    """Return a SHA-256 hash of a token for safe database storage."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return (
        "scrypt$"
        + base64.b64encode(salt).decode("ascii")
        + "$"
        + base64.b64encode(digest).decode("ascii")
    )


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, salt_text, digest_text = encoded.split("$", 2)
        if algorithm != "scrypt":
            return False
        salt = base64.b64decode(salt_text)
        expected = base64.b64decode(digest_text)
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def session_expiry(minutes: int) -> datetime:
    return datetime.now(UTC) + timedelta(minutes=minutes)
