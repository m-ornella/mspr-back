from datetime import date
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

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
    Picture: Optional[str]


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


# class PhotosBase(BaseModel):
#     file_path: Optional[str]
#     content_type: Optional[str]
#     content_id: Optional[str]


# class PhotosCreate(PhotosBase):
#     pass


# class Photos(PhotosBase):
#     id: Optional[str]

#     class Config:
#         orm_mode = True


class PlantGuardingBase(BaseModel):
    Name: str
    Description: Optional[str]
    Picture: Optional[str]
    DateStart: Optional[str]
    DateEnd: Optional[str]
    Location: Optional[str]
    IdOwner: int


class PlantGuardingCreate(PlantGuardingBase):
    pass


class PlantGuarding(PlantGuardingBase):
    Id: Optional[str]
    IdGuard: Optional[str]

    class Config:
        orm_mode = True


class PlantQuestionBase(BaseModel):
    Picture: Optional[HttpUrl]
    Title: str
    Content: str
    DateSent: Optional[str]
    IdOwner: int


class PlantQuestionCreate(PlantQuestionBase):
    pass


class PlantQuestion(PlantQuestionBase):
    Id: Optional[int]

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
    


