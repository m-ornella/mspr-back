from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    Name: str
    Surname: str
    Email: EmailStr
    IsBotanist: bool
    Birthday: date

class UserCreate(UserBase):
    Password: str

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    Id: int

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    Password: str
