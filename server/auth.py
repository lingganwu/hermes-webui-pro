import os
import time
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = os.environ.get("HERMES_JWT_SECRET", "hermes-webui-secret-key-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# Simple password comparison (no bcrypt to avoid version issues)
_stored_password = None

def _get_password() -> str:
    return os.environ.get("HERMES_WEB_PASSWORD", "")

def verify_password(plain: str) -> bool:
    pw = _get_password()
    if not pw:
        return True  # No password set = open access
    return plain == pw

def create_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
