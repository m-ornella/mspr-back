from datetime import date
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    Name: str
    Surname: str
    Email: str
    Password: str
    IsBotanist: bool
    Birthday: date

class UserCreate(UserBase):
    pass


class User(UserBase):
    Id: int

    class Config:
        orm_mode = True



class AnswerBase(BaseModel):
    Content: str
    DateSent: Optional[str]


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    Id: int
    IdSender: Optional[int]
    IdQuestion: Optional[int]

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    Content: str
    DateSent: Optional[str]


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    Id: str
    IdSender: Optional[str]
    IdReceiver: Optional[str]

    class Config:
        orm_mode = True

class PhotoBase(BaseModel):
    Url: str

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    Id: int
    PlantGuardingId: Optional[int]
    PlantQuestionId: Optional[int]

    class Config:
        orm_mode = True

class PlantGuardingBase(BaseModel):
    Name: str
    Description: Optional[str]
    DateStart: Optional[str]
    DateEnd: Optional[str]
    Location: Optional[str]
    IdOwner: int


class PlantGuardingCreate(PlantGuardingBase):
    photos: Optional[List[PhotoCreate]] = []


class PlantGuarding(PlantGuardingBase):
    Id: Optional[str]
    IdGuard: Optional[str]
    photos: List[Photo] = []

    class Config:
        orm_mode = True


class PlantQuestionBase(BaseModel):
    Title: str
    Content: str
    DateSent: Optional[str]
    IdOwner: int

class PlantQuestionCreate(PlantQuestionBase):
    photos: Optional[List[PhotoCreate]] = []


class PlantQuestion(PlantQuestionBase):
    Id: Optional[int]
    photos: List[Photo] = []

    class Config:
        orm_mode = True


# class PlantTypesBase(BaseModel):
#     type_name: Optional[str]
#     description: Optional[str]


# class PlantTypesCreate(PlantTypesBase):
#     pass


# class PlantTypes(PlantTypesBase):
#     id: Optional[str]

#     class Config:
#         orm_mode = True


class UserBase(BaseModel):
    Name: str
    Surname: str
    Email: EmailStr
    Password: str
    IsBotanist: bool
    Birthday: Optional[str]
    


