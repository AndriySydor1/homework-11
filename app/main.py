from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import date, timedelta
from . import models, database
from app.routers import contacts

# Створення об'єкта FastAPI
app = FastAPI()

# Підключення роутера для контактів
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

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
def create_contact(contact: ContactCreate, db: Session = Depends(database.get_db)):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/")
def get_contacts(db: Session = Depends(database.get_db)):
    return db.query(models.Contact).all()

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(database.get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(database.get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(database.get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}

# Additional Features
@app.get("/contacts/search/")
def search_contacts(query: str, db: Session = Depends(database.get_db)):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.ilike(f"%{query}%")) |
        (models.Contact.last_name.ilike(f"%{query}%")) |
        (models.Contact.email.ilike(f"%{query}%"))
    ).all()

@app.get("/contacts/upcoming-birthdays/")
def upcoming_birthdays(db: Session = Depends(database.get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.birthday.between(today, next_week)
    ).all()
