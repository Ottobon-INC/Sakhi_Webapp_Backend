# modules/auth.py
# JWT token generation and password hashing utilities
#
# Uses bcrypt directly (not via passlib) to avoid passlib 1.7.4 / bcrypt 5.x incompatibility.

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt

# ── Configuration ──────────────────────────────────────────────────────────────
JWT_SECRET_KEY     = os.getenv("JWT_SECRET_KEY", "janmasethu-sakhi-jwt-secret-2024-change-in-production")
JWT_ALGORITHM      = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "10080"))  # 7 days


# ── Password Utilities ─────────────────────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Hash a plain-text password with bcrypt. Returns a utf-8 string."""
    password_bytes = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if plain_password matches the stored bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


def is_already_hashed(value: str) -> bool:
    """
    Detect whether a stored value is already a bcrypt hash.
    Allows graceful handling of legacy plain-text passwords.
    """
    return value.startswith("$2b$") or value.startswith("$2a$")


# ── JWT Utilities ──────────────────────────────────────────────────────────────

def create_access_token(user_id: str, email: str, name: str = "") -> str:
    """
    Create a signed JWT access token.

    Payload includes:
        sub   – user_id (subject)
        email – user email
        name  – display name
        iat   – issued-at timestamp
        exp   – expiry timestamp
    """
    now    = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=JWT_EXPIRE_MINUTES)

    payload = {
        "sub":   user_id,
        "email": email,
        "name":  name,
        "iat":   now,
        "exp":   expire,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.
    Returns the payload dict, or None if invalid/expired.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


# ── Stateful Session Management ───────────────────────────────────────────────

import hashlib


def _hash_token(token: str) -> str:
    """Create a SHA-256 hash of the JWT for safe storage."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def save_session(user_id: str, token: str, expires_minutes: int = JWT_EXPIRE_MINUTES):
    """
    Store a new session in sakhi_user_sessions.
    Called right after create_access_token().
    """
    from supabase_client import supabase_insert

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=expires_minutes)

    supabase_insert("sakhi_user_sessions", {
        "user_id": user_id,
        "token_hash": _hash_token(token),
        "created_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
        "is_active": True,
    })


def validate_session(token: str) -> bool:
    """
    Check if the session for this token is still active in the database.
    Returns True only if the token hash exists AND is_active is True.
    """
    from supabase_client import supabase_select

    token_hash = _hash_token(token)
    rows = supabase_select(
        "sakhi_user_sessions",
        select="id,is_active",
        filters=f"token_hash=eq.{token_hash}&is_active=eq.true",
        limit=1,
    )
    return len(rows) > 0


def invalidate_session(token: str):
    """
    Mark a single session as inactive (logout from one device).
    """
    from supabase_client import supabase_update

    token_hash = _hash_token(token)
    supabase_update(
        "sakhi_user_sessions",
        f"token_hash=eq.{token_hash}",
        {"is_active": False},
    )


def invalidate_all_user_sessions(user_id: str):
    """
    Mark ALL sessions for a user as inactive (logout from all devices).
    """
    from supabase_client import supabase_update

    supabase_update(
        "sakhi_user_sessions",
        f"user_id=eq.{user_id}",
        {"is_active": False},
    )
