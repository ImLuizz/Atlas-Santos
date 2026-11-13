import hashlib
import secrets


def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token (e.g. for invitations or sessions)."""
    return secrets.token_urlsafe(length)


def hash_token(token: str) -> str:
    """Return a SHA-256 hash of a token for safe database storage."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
