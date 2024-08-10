from pydantic import BaseModel
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    birthday: Optional[date]
    additional_info: Optional[str]

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
        