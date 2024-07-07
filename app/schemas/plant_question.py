from datetime import date
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from app.schemas.photo import Photo, PhotoCreate

class PlantQuestionBase(BaseModel):
    Title: str
    Content: str
    DateSent: Optional[str]
    IdOwner: int

class PlantQuestionCreate(PlantQuestionBase):
    photos: Optional[List[PhotoCreate]] = []

class PlantQuestionUpdate(PlantQuestionBase):
    pass

class PlantQuestion(PlantQuestionBase):
    Id: Optional[int]
    photos: List[Photo] = []

    class Config:
        from_attributes = True