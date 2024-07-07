from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.crud.plant_question import create_plant_question, get_plant_question, get_plant_questions, update_plant_question, delete_plant_question
from app.schemas.plant_question import PlantQuestion, PlantQuestionCreate, PlantQuestionUpdate
from app.database import get_db
from app.crud.photo import create_photo

router = APIRouter(
    prefix="/api/plant_questions",
    tags=["plant_questions"],
)

@router.post("/", response_model=PlantQuestion)
def create_plant_question_endpoint(
    Title: str,
    Content: str,
    DateSent: str,
    IdOwner: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_data = file.file.read()
    plant_question_data = PlantQuestionCreate(
        Title=Title,
        Content=Content,
        DateSent=DateSent,
        IdOwner=IdOwner
    )

    db_plant_question = create_plant_question(db, plant_question_data)

    photo = create_photo(db=db, photo_data=file_data, plant_question_id=db_plant_question.Id)
    db_plant_question.photos.append(photo)
    db.commit()
    db.refresh(db_plant_question)

    # Convert DateSent to string
    response_data = db_plant_question.__dict__.copy()
    response_data['DateSent'] = db_plant_question.DateSent.isoformat()
    return response_data

@router.get("/{question_id}", response_model=PlantQuestion)
def read_plant_question(question_id: int, db: Session = Depends(get_db)):
    db_plant_question = get_plant_question(db, question_id)
    if db_plant_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant question not found")
    response_data = db_plant_question.__dict__.copy()
    response_data['DateSent'] = db_plant_question.DateSent.isoformat()
    return response_data

@router.get("/", response_model=List[PlantQuestion])
def read_plant_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = get_plant_questions(db, skip, limit)
    response_data = []
    for question in questions:
        data = question.__dict__.copy()
        data['DateSent'] = question.DateSent.isoformat()
        response_data.append(data)
    return response_data

@router.put("/{question_id}", response_model=PlantQuestion)
def update_plant_question_endpoint(question_id: int, question: PlantQuestionUpdate, db: Session = Depends(get_db)):
    db_plant_question = update_plant_question(db, question_id, question)
    if db_plant_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant question not found")
    response_data = db_plant_question.__dict__.copy()
    response_data['DateSent'] = db_plant_question.DateSent.isoformat()
    return response_data

@router.delete("/{question_id}", response_model=PlantQuestion)
def delete_plant_question_endpoint(question_id: int, db: Session = Depends(get_db)):
    db_plant_question = delete_plant_question(db, question_id)
    if db_plant_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant question not found")
    response_data = db_plant_question.__dict__.copy()
    response_data['DateSent'] = db_plant_question.DateSent.isoformat()
    return response_data
