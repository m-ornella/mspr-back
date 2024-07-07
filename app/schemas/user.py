from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
