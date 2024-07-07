from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.answer import create_answer, get_answer, get_answers, update_answer, delete_answer
from app.schemas.answer import Answer, AnswerCreate, AnswerUpdate
from app.database import get_db

router = APIRouter(
    prefix="/api/answers",
    tags=["answers"],
)

@router.post("/", response_model=Answer)
def create_answer_endpoint(answer: AnswerCreate, db: Session = Depends(get_db)):
    return create_answer(db, answer)

@router.get("/{answer_id}", response_model=Answer)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    db_answer = get_answer(db, answer_id)
    if db_answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    return db_answer

@router.get("/", response_model=List[Answer])
def read_answers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_answers(db, skip, limit)

@router.put("/{answer_id}", response_model=Answer)
def update_answer_endpoint(answer_id: int, answer: AnswerUpdate, db: Session = Depends(get_db)):
    db_answer = update_answer(db, answer_id, answer)
    if db_answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    return db_answer

@router.delete("/{answer_id}", response_model=Answer)
def delete_answer_endpoint(answer_id: int, db: Session = Depends(get_db)):
    db_answer = delete_answer(db, answer_id)
    if db_answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    return db_answer
