from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from .photo import Photo

class PlantQuestionBase(BaseModel):
    Title: str
    Content: str
    DateSent: date
    IdOwner: int

class PlantQuestionCreate(PlantQuestionBase):
    photos: Optional[List[Photo]] = []

class PlantQuestionUpdate(PlantQuestionBase):
    photos: Optional[List[Photo]] = []

class PlantQuestionInDBBase(PlantQuestionBase):
    Id: int
    photos: List[Photo] = []

    class Config:
        from_attributes = True

class PlantQuestion(PlantQuestionInDBBase):
    pass

class PlantQuestionInDB(PlantQuestionInDBBase):
    pass
