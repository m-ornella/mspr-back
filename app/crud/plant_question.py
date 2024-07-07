from sqlalchemy.orm import Session
from app.models.plant_question import PlantQuestion
from app.schemas.plant_question import PlantQuestionCreate, PlantQuestionUpdate

def create_plant_question(db: Session, plant_question: PlantQuestionCreate) -> PlantQuestion:
    db_plant_question = PlantQuestion(**plant_question.dict())
    db.add(db_plant_question)
    db.commit()
    db.refresh(db_plant_question)
    return db_plant_question

def get_plant_question(db: Session, question_id: int) -> PlantQuestion:
    return db.query(PlantQuestion).filter(PlantQuestion.Id == question_id).first()

def get_plant_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PlantQuestion).offset(skip).limit(limit).all()

def update_plant_question(db: Session, question_id: int, question: PlantQuestionUpdate) -> PlantQuestion:
    db_plant_question = db.query(PlantQuestion).filter(PlantQuestion.Id == question_id).first()
    if db_plant_question is None:
        return None
    for key, value in question.dict().items():
        setattr(db_plant_question, key, value)
    db.commit()
    db.refresh(db_plant_question)
    return db_plant_question

def delete_plant_question(db: Session, question_id: int) -> PlantQuestion:
    db_plant_question = db.query(PlantQuestion).filter(PlantQuestion.Id == question_id).first()
    if db_plant_question is None:
        return None
    db.delete(db_plant_question)
    db.commit()
    return db_plant_question
