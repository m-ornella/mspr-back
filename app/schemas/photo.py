from pydantic import BaseModel
from typing import Optional

class PhotoBase(BaseModel):
    image: bytes
    plant_guarding_id: Optional[int] = None
    plant_question_id: Optional[int] = None

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: int

    class Config:
        from_attributes = True