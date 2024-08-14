from pydantic import BaseModel, EmailStr
from datetime import date

# User models
class UserBase(BaseModel):
    email: EmailStr
    is_verified: bool = False  # Поле для перевірки верифікації
    avatar_url: str | None = None  # Додано поле для URL аватара

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Підтримка режиму ORM

# Схема для оновлення аватара
class AvatarUpdate(BaseModel):
    avatar_url: str

# Contact models
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: str = None

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Підтримка режиму ORM

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

# Email verification models
class EmailVerification(BaseModel):
    email: EmailStr

class EmailVerificationToken(BaseModel):
    token: str
    
        