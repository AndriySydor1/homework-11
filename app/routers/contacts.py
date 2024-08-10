from sqlalchemy import extract
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta

from app import models, schemas, database

router = APIRouter()

# Пошук контактів за ім'ям, прізвищем або електронною адресою
@router.get("/search/", response_model=List[schemas.Contact])
def search_contacts(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Contact)
    
    if first_name:
        query = query.filter(models.Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))
    
    results = query.all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No contacts found.")
    
    return results

# Отримання контактів з днями народження на найближчі 7 днів
@router.get("/upcoming_birthdays/", response_model=List[schemas.Contact])
def get_upcoming_birthdays(db: Session = Depends(database.get_db)):
    today = date.today()
    current_year = today.year

    # Список днів народження, які потрапляють у найближчі 7 днів
    upcoming_birthdays = []
    for i in range(7):
        day_to_check = today + timedelta(days=i)
        contacts = db.query(models.Contact).filter(
            extract('month', models.Contact.birthday) == day_to_check.month,
            extract('day', models.Contact.birthday) == day_to_check.day
        ).all()
        upcoming_birthdays.extend(contacts)

    if not upcoming_birthdays:
        raise HTTPException(status_code=404, detail="No upcoming birthdays found.")

    return upcoming_birthdays
