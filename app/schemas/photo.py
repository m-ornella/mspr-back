from pydantic import BaseModel

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
