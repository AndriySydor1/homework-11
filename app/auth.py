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
    """verify_password AI is creating summary for verify_password

    Args:
        plain_password (str): [description]
        hashed_password (str): [description]

    Returns:
        bool: [description]
    """    
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """get_password_hash AI is creating summary for get_password_hash

    Args:
        password (str): [description]

    Returns:
        str: [description]
    """    
    return pwd_context.hash(password)

# Налаштування JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token/")

# Підключення до Redis
redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """create_access_token AI is creating summary for create_access_token

    Args:
        data (dict): [description]
        expires_delta (Optional[timedelta], optional): [description]. Defaults to None.

    Returns:
        str: [description]
    """    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException) -> schemas.TokenData:
    """verify_token AI is creating summary for verify_token

    Args:
        token (str): [description]
        credentials_exception (HTTPException): [description]

    Raises:
        credentials_exception: [description]
        credentials_exception: [description]

    Returns:
        schemas.TokenData: [description]
    """    
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
    """get_current_user AI is creating summary for get_current_user

    Args:
        token (str, optional): [description]. Defaults to Depends(oauth2_scheme).
        db (Session, optional): [description]. Defaults to Depends(database.get_db).

    Raises:
        credentials_exception: [description]
        HTTPException: [description]

    Returns:
        models.User: [description]
    """    
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
    """create_verification_token AI is creating summary for create_verification_token

    Args:
        email (str): [description]

    Returns:
        str: [description]
    """    
    expire = datetime.now(timezone.utc) + timedelta(hours=24)  # Термін дії токена 24 години
    to_encode = {"sub": email, "exp": expire}
    verification_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return verification_token

def verify_verification_token(token: str) -> Optional[str]:
    """verify_verification_token AI is creating summary for verify_verification_token

    Args:
        token (str): [description]

    Returns:
        Optional[str]: [description]
    """    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None

async def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """authenticate_user AI is creating summary for authenticate_user

    Args:
        db (Session): [description]
        email (str): [description]
        password (str): [description]

    Returns:
        Optional[models.User]: [description]
    """    
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
