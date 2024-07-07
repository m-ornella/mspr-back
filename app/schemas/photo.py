from pydantic import BaseModel
from typing import Optional

class PhotoBase(BaseModel):
    PlantGuardingId: int = None
    PlantQuestionId: int = None

class PhotoCreate(PhotoBase):
    Photo: bytes

class PhotoUpdate(PhotoBase):
    Photo: bytes

class PhotoInDBBase(PhotoBase):
    Id: int
    Photo: bytes

    class Config:
        from_attributes = True

class Photo(PhotoInDBBase):
    pass

class PhotoInDB(PhotoInDBBase):
    pass

class Photo(BaseModel):
    Id: int
    url: str
    PlantGuardingId: int | None = None
    PlantQuestionId: int | None = None

    class Config:
        from_attributes = True

class PhotoResponse(BaseModel):
    Id: int
    url: str
    PlantGuardingId: Optional[int] = None
    PlantQuestionId: Optional[int] = None

    class Config:
        from_attributes = True