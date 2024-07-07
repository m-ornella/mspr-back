from sqlalchemy.orm import Session
from app.models.photo import Photo
from app.schemas.photo import PhotoCreate, PhotoUpdate

def create_photo(db: Session, photo: PhotoCreate) -> Photo:
    db_photo = Photo(
        image=photo.image,
        plant_guarding_id=photo.plant_guarding_id,
        plant_question_id=photo.plant_question_id
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def get_photo(db: Session, photo_id: int) -> Photo:
    return db.query(Photo).filter(Photo.id == photo_id).first()

def get_photos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Photo).offset(skip).limit(limit).all()

def update_photo(db: Session, photo_id: int, photo: PhotoUpdate) -> Photo:
    db_photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if db_photo is None:
        return None
    db_photo.image = photo.image
    db_photo.plant_guarding_id = photo.plant_guarding_id
    db_photo.plant_question_id = photo.plant_question_id
    db.commit()
    db.refresh(db_photo)
    return db_photo

def delete_photo(db: Session, photo_id: int) -> Photo:
    db_photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if db_photo is None:
        return None
    db.delete(db_photo)
    db.commit()
    return db_photo
