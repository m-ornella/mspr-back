from sqlalchemy.orm import Session
import app.schemas as schemas
from app.models.user import User
from app.models.answer import Answer
from app.models.message import Message
from app.models.plant_guarding import PlantGuarding
from app.models.plant_question import PlantQuestion
from app.models.photo import Photo
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.Email == email).first()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.Password)
    db_user = User(
        Name=user.Name,
        Surname=user.Surname,
        Email=user.Email,
        Password=hashed_password,
        IsBotanist=user.IsBotanist,
        Birthday=user.Birthday
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.Email == email).first()
    if not user:
        return None
    if not verify_password(password, user.Password):
        return None
    return user

# ####################################################################################
# ############ GET ###################################################################

# Questions
def get_plant_questions(db: Session):
    return db.query(PlantQuestion).all()

def get_plant_question_by_id(db: Session, question_id: int):
    return db.query(PlantQuestion).filter(PlantQuestion.Id == question_id).first()

# Sessions de garde
def get_plant_guardings(db: Session):
    return db.query(
        PlantGuarding,
        User.Email.label('OwnerEmail')
    ).join(User, PlantGuarding.IdOwner == User.Id).all()

def get_plant_guarding_by_id(db: Session, guarding_id: int):
    return db.query(PlantGuarding).filter(PlantGuarding.Id == guarding_id).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.Id == user_id).first()

# ####################################################################################
# ############ POST ##################################################################

# Questions
def create_plant_question(db: Session, plant_question: schemas.PlantQuestionCreate):
    db_plant_question = PlantQuestion(
        Title=plant_question.Title,
        Content=plant_question.Content,
        DateSent=plant_question.DateSent,
        IdOwner=plant_question.IdOwner
    )
    db.add(db_plant_question)
    db.commit()
    db.refresh(db_plant_question)

    for photo in plant_question.photos:
        db_photo = Photo(Url=photo.Url, PlantQuestionId=db_plant_question.Id)
        db.add(db_photo)
        db.commit()

    return db_plant_question

# Sessions de garde
def create_plant_guarding(db: Session, plant_guarding: schemas.PlantGuardingCreate):
    db_plant_guarding = PlantGuarding(
        Name=plant_guarding.Name,
        Description=plant_guarding.Description,
        DateStart=plant_guarding.DateStart,
        DateEnd=plant_guarding.DateEnd,
        Location=plant_guarding.Location,
        IdOwner=plant_guarding.IdOwner
    )
    db.add(db_plant_guarding)
    db.commit()
    db.refresh(db_plant_guarding)

    for photo in plant_guarding.photos:
        db_photo = Photo(Url=photo.Url, PlantGuardingId=db_plant_guarding.Id)
        db.add(db_photo)
        db.commit()

    return db_plant_guarding

# Messages
def create_message(db: Session, message: schemas.MessageCreate, sender_id: int, receiver_id: int):
    db_message = Message(
        **message.dict(), IdSender=sender_id, IdReceiver=receiver_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# ####################################################################################
# ############ PUT ###################################################################

# Questions
def update_plant_question(db: Session, question_id: int, question: schemas.PlantQuestionCreate):
    db.query(PlantQuestion).filter(PlantQuestion.Id == question_id).update(question.dict())
    db.commit()
    return db.query(PlantQuestion).filter(PlantQuestion.Id == question_id).first()

# Sessions de garde
def update_plant_guarding(db: Session, guarding_id: int, guarding: schemas.PlantGuardingCreate):
    db.query(PlantGuarding).filter(PlantGuarding.Id == guarding_id).update(guarding.dict())
    db.commit()
    return db.query(PlantGuarding).filter(PlantGuarding.Id == guarding_id).first()

# Messages
def update_message(db: Session, message_id: int, message: schemas.MessageCreate):
    db.query(Message).filter(Message.Id == message_id).update(message.dict())
    db.commit()
    return db.query(Message).filter(Message.Id == message_id).first()

# ####################################################################################
# ############ DELETE ################################################################

# Utilisateur
def delete_user(db: Session, user_id: int):
    db.query(User).filter(User.Id == user_id).delete()
    db.commit()

# Session de garde
def delete_plant_guarding(db: Session, guarding_id: int):
    db.query(PlantGuarding).filter(PlantGuarding.Id == guarding_id).delete()
    db.commit()

# Message
def delete_message(db: Session, message_id: int):
    db.query(Message).filter(Message.Id == message_id).delete()
    db.commit()
