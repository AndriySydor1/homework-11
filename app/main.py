from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import date, timedelta
from . import models, database
from app.routers import contacts, users
from fastapi.security import OAuth2PasswordBearer
from app.auth import get_current_user  # Додано для перевірки токенів

# Створення об'єкта FastAPI
app = FastAPI()

# Підключення роутерів
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Створення таблиць у базі даних
models.Base.metadata.create_all(bind=database.engine)

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: str = None

class ContactUpdate(ContactCreate):
    pass

# CRUD Operations
@app.post("/contacts/", response_model=ContactCreate)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)  # Перевірка токена
):
    db_contact = models.Contact(**contact.dict(), owner_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/")
def get_contacts(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)  # Перевірка токена
):
    return db.query(models.Contact).filter(models.Contact.owner_id == current_user.id).all()

@app.get("/contacts/{contact_id}")
def get_contact(
    contact_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)  # Перевірка токена
):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == current_user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}")
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)  # Перевірка токена
):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == current_user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)  # Перевірка токена
):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == current_user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}

# Additional Features
@app.get("/contacts/search/")
def search_contacts(
    query: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)  # Перевірка токена
):
    return db.query(models.Contact).filter(
        (models.Contact.owner_id == current_user.id) &
        (
            (models.Contact.first_name.ilike(f"%{query}%")) |
            (models.Contact.last_name.ilike(f"%{query}%")) |
            (models.Contact.email.ilike(f"%{query}%"))
        )
    ).all()

@app.get("/contacts/upcoming-birthdays/")
def upcoming_birthdays(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)  # Перевірка токена
):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.owner_id == current_user.id,
        models.Contact.birthday.between(today, next_week)
    ).all()
    
