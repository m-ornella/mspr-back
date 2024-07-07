from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.crud.photo import create_photo, get_photo, get_photos, update_photo, delete_photo
from app.schemas.photo import Photo, PhotoCreate, PhotoUpdate
from app.database import get_db
import io

router = APIRouter(
    prefix="/api/photos",
    tags=["photos"],
)

@router.post("/", response_model=Photo)
def create_photo_endpoint(photo: PhotoCreate, db: Session = Depends(get_db)):
    return create_photo(db, photo)

@router.get("/{photo_id}")
def get_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.Id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    
    return StreamingResponse(io.BytesIO(photo.Photo), media_type="image/jpeg")

@router.get("/", response_model=List[Photo])
def read_photos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_photos(db, skip, limit)

@router.put("/{photo_id}", response_model=Photo)
def update_photo_endpoint(photo_id: int, photo: PhotoUpdate, db: Session = Depends(get_db)):
    db_photo = update_photo(db, photo_id, photo)
    if db_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return db_photo

@router.delete("/{photo_id}", response_model=Photo)
def delete_photo_endpoint(photo_id: int, db: Session = Depends(get_db)):
    db_photo = delete_photo(db, photo_id)
    if db_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return db_photo
