import os
from datetime import datetime, timedelta
from jose import jwt
from pwdlib import PasswordHash
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "bite-flow-super-secret-key")
ALGORITHM = "HS256"

# এটা passlib এর চেয়ে 10x ফাস্ট এবং type error দেয় না
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_token(data: dict, expires_delta: timedelta = timedelta(hours=24)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt