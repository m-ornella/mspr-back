from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from .photo import Photo
from app.schemas.photo import PhotoResponse

class PlantQuestionBase(BaseModel):
    Title: str
    Content: str
    DateSent: date
    IdOwner: int

class PlantQuestionCreate(PlantQuestionBase):
    photos: Optional[List[PhotoResponse]] = []

class PlantQuestionUpdate(PlantQuestionBase):
    photos: Optional[List[PhotoResponse]] = []

class PlantQuestionInDBBase(PlantQuestionBase):
    Id: int
    photos: List[PhotoResponse] = []

    class Config:
        from_attributes = True

class PlantQuestion(PlantQuestionInDBBase):
    pass

class PlantQuestionInDB(PlantQuestionInDBBase):
    pass

class PlantQuestionResponse(BaseModel):
    Id: int
    Title: str
    Content: str
    DateSent: str
    IdOwner: int
    photos: List[PhotoResponse] = []

    class Config:
        from_attributes = True