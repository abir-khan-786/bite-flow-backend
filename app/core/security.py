from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Bcrypt Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# পাসওয়ার্ড হ্যাশ করার ফাংশন
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# পাসওয়ার্ড ভেরিফাই করার ফাংশন
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Access Token জেনারেট করার ফাংশন
def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt