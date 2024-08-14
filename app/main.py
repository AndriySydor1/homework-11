from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import date, timedelta
from . import models, database
from app.routers import contacts, users
from app.routers import reset_password
from app.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from aioredis import Redis
import os
from contextlib import asynccontextmanager

# Створення об'єкта FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Підключення до Redis для обмеження швидкості запитів
    redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
    await FastAPILimiter.init(redis)
    
    yield  # Всі ваші маршрути будуть виконуватись між цими рядками
    
    # Закриття з'єднання з Redis
    await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)

# Налаштування CORS
origins = ["*"]  # Ви можете обмежити до конкретних доменів, наприклад ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(reset_password.router, prefix="/auth", tags=["auth"])

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
@app.post("/contacts/", response_model=ContactCreate, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_contact = models.Contact(**contact.model_dump(), owner_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/")
def get_contacts(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Contact).filter(models.Contact.owner_id == current_user.id).all()

@app.get("/contacts/{contact_id}")
def get_contact(
    contact_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
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
    current_user: models.User = Depends(get_current_user)
):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == current_user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.model_dump().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
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
    current_user: models.User = Depends(get_current_user)
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
    current_user: models.User = Depends(get_current_user)
):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.owner_id == current_user.id,
        models.Contact.birthday.between(today, next_week)
    ).all()
    
