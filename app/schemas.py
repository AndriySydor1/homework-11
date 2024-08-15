from pydantic import BaseModel, EmailStr
from datetime import date

# User models
class UserBase(BaseModel):
    """UserBase 
    Args:
        BaseModel ([type]): [description]
    """    
    email: EmailStr
    is_verified: bool = False  # Поле для перевірки верифікації
    avatar_url: str | None = None  # Додано поле для URL аватара

class UserCreate(UserBase):
    """UserCreate 
    Args:
        UserBase ([type]): [description]
    """    
    password: str

class User(UserBase):
    """User 
    Args:
        UserBase ([type]): [description]
    """    
    id: int

    class Config:
        from_attributes = True  # Підтримка режиму ORM

# Схема для оновлення аватара
class AvatarUpdate(BaseModel):
    """AvatarUpdate 
    Args:
        BaseModel ([type]): [description]
    """    
    avatar_url: str

# Contact models
class ContactBase(BaseModel):
    """ContactBase 

    Args:
        BaseModel ([type]): [description]
    """    
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: str = None

class ContactCreate(ContactBase):
    """ContactCreate 

    Args:
        ContactBase ([type]): [description]
    """    
    pass

class Contact(ContactBase):
    """Contact 
    Args:
        ContactBase ([type]): [description]
    """    
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Підтримка режиму ORM

# Token models
class Token(BaseModel):
    """Token 

    Args:
        BaseModel ([type]): [description]
    """    
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """TokenData 

    Args:
        BaseModel ([type]): [description]
    """    
    email: str | None = None

# Email verification models
class EmailVerification(BaseModel):
    """EmailVerification 

    Args:
        BaseModel ([type]): [description]
    """    
    email: EmailStr

class EmailVerificationToken(BaseModel):
    """EmailVerificationToken 

    Args:
        BaseModel ([type]): [description]
    """    
    token: str
    
        