from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.crud.plant_question import create_plant_question, get_plant_question, get_plant_questions, update_plant_question, delete_plant_question
from app.schemas.plant_question import PlantQuestion, PlantQuestionCreate, PlantQuestionUpdate
from app.database import SessionLocal
import shutil
import os

router = APIRouter(
    prefix="/api/plant_questions",
    tags=["plant_questions"],
)

@router.post("/", response_model=PlantQuestion)
def create_plant_question_endpoint(
    title: str,
    content: str,
    date_sent: str,
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

    plant_question_data = PlantQuestionCreate(
        title=title,
        content=content,
        date_sent=date_sent,
        owner_id=owner_id,
        photos=[{"url": file_path}]
    )
    return create_plant_question(db, plant_question_data)

@router.get("/{question_id}", response_model=PlantQuestion)
def read_plant_question(question_id: int, db: Session = Depends(SessionLocal)):
    db_plant_question = get_plant_question(db, question_id)
    if db_plant_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant question not found")
    return db_plant_question

@router.get("/", response_model=List[PlantQuestion])
def read_plant_questions(skip: int = 0, limit: int = 100, db: Session = Depends(SessionLocal)):
    return get_plant_questions(db, skip, limit)

@router.put("/{question_id}", response_model=PlantQuestion)
def update_plant_question_endpoint(question_id: int, question: PlantQuestionUpdate, db: Session = Depends(SessionLocal)):
    db_plant_question = update_plant_question(db, question_id, question)
    if db_plant_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant question not found")
    return db_plant_question

@router.delete("/{question_id}", response_model=PlantQuestion)
def delete_plant_question_endpoint(question_id: int, db: Session = Depends(SessionLocal)):
    db_plant_question = delete_plant_question(db, question_id)
    if db_plant_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant question not found")
    return db_plant_question
