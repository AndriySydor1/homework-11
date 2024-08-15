from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app import models, schemas, database, auth
from app.email import send_reset_password_email

router = APIRouter()

@router.post("/reset-password/request/", response_model=dict)
def request_password_reset(email: str, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    """request_password_reset 

    Args:
        email (str): [description]
        background_tasks (BackgroundTasks): [description]
        db (Session, optional): [description]. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email does not exist.")

    # Генерація токену для скидання паролю
    reset_token = auth.create_reset_password_token(email)
    user.reset_password_token = reset_token
    user.reset_password_expires = datetime.now(timezone.utc) + timedelta(hours=1)  # Токен дійсний 1 годину
    db.commit()

    # Відправлення email з токеном
    background_tasks.add_task(send_reset_password_email, user.email, reset_token)
    
    return {"msg": "Password reset link has been sent to your email."}

@router.post("/reset-password/verify/", response_model=dict)
def verify_reset_token(token: str, db: Session = Depends(database.get_db)):
    """verify_reset_token 
    Args:
        token (str): [description]
        db (Session, optional): [description]. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """    
    user = db.query(models.User).filter(models.User.reset_password_token == token).first()
    if not user or user.reset_password_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")
    
    return {"msg": "Reset token is valid."}

@router.post("/reset-password/", response_model=dict)
def reset_password(token: str, new_password: str, db: Session = Depends(database.get_db)):
    """reset_password 
    Args:
        token (str): [description]
        new_password (str): [description]
        db (Session, optional): [description]. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """    
    user = db.query(models.User).filter(models.User.reset_password_token == token).first()
    if not user or user.reset_password_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")
    
    # Оновлення пароля
    hashed_password = auth.get_password_hash(new_password)
    user.hashed_password = hashed_password
    user.reset_password_token = None  # Видалення токену після успішного скидання
    user.reset_password_expires = None
    db.commit()
    
    return {"msg": "Password has been reset successfully."}
