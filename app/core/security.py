from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM

# =============================
# JWT CONFIG (SINGLE SOURCE)
# =============================
SECRET_KEY = "dayflow_super_secret_key_123"   # MUST MATCH deps.py
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# =============================
# PASSWORD HASHING
# =============================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    """
    Hash password safely using bcrypt.
    bcrypt has a HARD LIMIT of 72 bytes.
    """
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password too long (bcrypt max 72 bytes)")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =============================
# JWT TOKEN CREATION
# =============================
def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    data MUST contain:
    - sub: str(user_id)
    - role: user role
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
