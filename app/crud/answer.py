from sqlalchemy.orm import Session
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate, AnswerUpdate

def create_answer(db: Session, answer: AnswerCreate) -> Answer:
    db_answer = Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_answer(db: Session, answer_id: int) -> Answer:
    return db.query(Answer).filter(Answer.id == answer_id).first()

def get_answers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Answer).offset(skip).limit(limit).all()

def update_answer(db: Session, answer_id: int, answer: AnswerUpdate) -> Answer:
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer is None:
        return None
    for key, value in answer.dict().items():
        setattr(db_answer, key, value)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def delete_answer(db: Session, answer_id: int) -> Answer:
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer is None:
        return None
    db.delete(db_answer)
    db.commit()
    return db_answer
