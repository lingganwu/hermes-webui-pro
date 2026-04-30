import os
import time
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.hash import bcrypt

SECRET_KEY = os.environ.get("HERMES_JWT_SECRET", "hermes-webui-secret-key-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

_password_hash = None

def get_password_hash() -> str | None:
    global _password_hash
    pw = os.environ.get("HERMES_WEB_PASSWORD", "")
    if not pw:
        return None
    if _password_hash is None:
        _password_hash = bcrypt.hash(pw)
    return _password_hash

def verify_password(plain: str) -> bool:
    hashed = get_password_hash()
    if not hashed:
        return True  # No password set = open access
    return bcrypt.verify(plain, hashed)

def create_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
