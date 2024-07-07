from sqlalchemy.orm import Session
from app.models.plant_question import PlantQuestion
from app.schemas.plant_question import PlantQuestionCreate, PlantQuestionUpdate, PlantQuestionResponse
from app.schemas.photo import PhotoResponse

def create_plant_question(db: Session, plant_question: PlantQuestionCreate) -> PlantQuestion:
    db_plant_question = PlantQuestion(**plant_question.dict(exclude_unset=True))
    db.add(db_plant_question)
    db.commit()
    db.refresh(db_plant_question)
    return db_plant_question

def get_plant_question(db: Session, question_id: int) -> PlantQuestionResponse:
    question = db.query(PlantQuestion).filter(PlantQuestion.Id == question_id).first()
    if question:
        for photo in question.photos:
            photo.url = f"/api/photos/{photo.Id}"
        question.DateSent = question.DateSent.isoformat()  # Convert DateSent to string
        return PlantQuestionResponse.from_orm(question)
    return None

def get_plant_question_user(db: Session, user_id: int) -> PlantQuestionResponse:
    question = db.query(PlantQuestion).filter(PlantQuestion.IdOwner == user_id).first()
    if question:
        for photo in question.photos:
            photo.url = f"/api/photos/{photo.Id}"
        question.DateSent = question.DateSent.isoformat()  # Convert DateSent to string
        return PlantQuestionResponse.from_orm(question)
    return None

def get_plant_questions(db: Session, skip: int = 0, limit: int = 100):
    questions = db.query(PlantQuestion).offset(skip).limit(limit).all()
    for question in questions:
        for photo in question.photos:
            photo.url = f"/api/photos/{photo.Id}"
    return questions

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
