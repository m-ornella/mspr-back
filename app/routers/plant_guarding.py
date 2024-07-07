from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.crud.plant_guarding import create_plant_guarding, get_plant_guarding, get_plant_guardings, update_plant_guarding, delete_plant_guarding
from app.schemas.plant_guarding import PlantGuarding, PlantGuardingCreate, PlantGuardingUpdate
from app.database import SessionLocal
import shutil
import os

router = APIRouter(
    prefix="/api/plant_guardings",
    tags=["plant_guardings"],
)

@router.post("/", response_model=PlantGuarding)
def create_plant_guarding_endpoint(
    name: str,
    description: str,
    date_start: str,
    date_end: str,
    location: str,
    owner_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(SessionLocal)
):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    plant_guarding_data = PlantGuardingCreate(
        name=name,
        description=description,
        date_start=date_start,
        date_end=date_end,
        location=location,
        owner_id=owner_id,
        photos=[{"url": file_path}]
    )
    return create_plant_guarding(db, plant_guarding_data)

@router.get("/{guarding_id}", response_model=PlantGuarding)
def read_plant_guarding(guarding_id: int, db: Session = Depends(SessionLocal)):
    db_plant_guarding = get_plant_guarding(db, guarding_id)
    if db_plant_guarding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant guarding not found")
    return db_plant_guarding

@router.get("/", response_model=List[PlantGuarding])
def read_plant_guardings(skip: int = 0, limit: int = 100, db: Session = Depends(SessionLocal)):
    return get_plant_guardings(db, skip, limit)

@router.put("/{guarding_id}", response_model=PlantGuarding)
def update_plant_guarding_endpoint(guarding_id: int, guarding: PlantGuardingUpdate, db: Session = Depends(SessionLocal)):
    db_plant_guarding = update_plant_guarding(db, guarding_id, guarding)
    if db_plant_guarding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant guarding not found")
    return db_plant_guarding

@router.delete("/{guarding_id}", response_model=PlantGuarding)
def delete_plant_guarding_endpoint(guarding_id: int, db: Session = Depends(SessionLocal)):
    db_plant_guarding = delete_plant_guarding(db, guarding_id)
    if db_plant_guarding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant guarding not found")
    return db_plant_guarding
