from pydantic import BaseModel
from typing import List, Optional

class Photo(BaseModel):
    url: str

class PlantGuardingBase(BaseModel):
    name: str
    description: Optional[str]
    date_start: str
    date_end: str
    location: str
    owner_id: int
    guard_id: int

class PlantGuardingCreate(PlantGuardingBase):
    photos: List[Photo]

class PlantGuardingUpdate(PlantGuardingBase):
    photos: List[Photo]

class PlantGuarding(PlantGuardingBase):
    id: int

    class Config:
        from_attributes = True
