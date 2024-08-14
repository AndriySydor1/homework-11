from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Any

from app import models, schemas, database
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from app.email import send_verification_email
from app.auth import create_verification_token, verify_verification_token
import cloudinary.uploader

router = APIRouter()

# Реєстрація нового користувача
@router.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    # Перевірка, чи користувач з таким email вже існує
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    # Хешування пароля та збереження нового користувача в базі даних
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Генерація токена верифікації та відправка листа
    token = create_verification_token(db_user.email)
    background_tasks.add_task(send_verification_email, db_user.email, token)
    
    return db_user

# Авторизація користувача та отримання JWT токена
@router.post("/token/", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Аутентифікація користувача
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Генерація JWT токена
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Верифікація електронної пошти
@router.get("/verify-email/", response_model=schemas.User)
def verify_email(token: str, db: Session = Depends(database.get_db)) -> Any:
    email = verify_verification_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already verified")
    
    user.is_verified = True
    db.commit()
    db.refresh(user)
    
    return user

# Функція аутентифікації користувача
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Оновлення аватара користувача
@router.post("/upload-avatar/")
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        # Завантаження зображення на Cloudinary
        result = cloudinary.uploader.upload(file.file)
        avatar_url = result.get("secure_url")
        
        # Оновлення URL аватара в базі даних
        current_user.avatar_url = avatar_url
        db.commit()
        db.refresh(current_user)
        
        return {"avatar_url": avatar_url}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to upload avatar") from e
