from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    """User 
    Args:
        Base ([type]): [description]
    """    
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String(255), nullable=True)
    reset_password_token = Column(String(255), index=True, nullable=True)
    reset_password_expires = Column(DateTime, nullable=True)
    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    """Contact 
    Args:
        Base ([type]): [description]
    """    
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True, nullable=False)
    last_name = Column(String(50), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", back_populates="contacts")
    