from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas, database
from typing import Optional
import os
import json
from aioredis import Redis

# Налаштування хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Налаштування JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token/")  # Оновлений шлях до отримання токену

# Підключення до Redis
redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException) -> schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)

    # Спроба отримати користувача з кешу
    cached_user = await redis.get(f"user:{token_data.email}")
    if cached_user:
        user_data = json.loads(cached_user)
        user = schemas.User.model_validate(user_data)
    else:
        user = db.query(models.User).filter(models.User.email == token_data.email).first()
        if user is None:
            raise credentials_exception
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified",
            )
        # Кешування даних користувача
        user_data = schemas.User.model_validate(user).model_dump()
        await redis.set(f"user:{token_data.email}", json.dumps(user_data), ex=3600)  # Кешуємо на 1 годину

    return user

def create_verification_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=24)  # Термін дії токена 24 години
    to_encode = {"sub": email, "exp": expire}
    verification_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return verification_token

async def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    # Перевірка, чи користувач є в кеші
    cached_user = await redis.get(f"user:{email}")
    if cached_user:
        user_data = json.loads(cached_user)
        user = schemas.User.model_validate(user_data)
    else:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        # Кешування даних користувача після успішної аутентифікації
        user_data = schemas.User.model_validate(user).model_dump()
        await redis.set(f"user:{email}", json.dumps(user_data), ex=3600)  # Кешуємо на 1 годину
    
    return user
