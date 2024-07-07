from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate

def create_message(db: Session, message: MessageCreate) -> Message:
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: int) -> Message:
    return db.query(Message).filter(Message.id == message_id).first()

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).offset(skip).limit(limit).all()

def update_message(db: Session, message_id: int, message: MessageUpdate) -> Message:
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        return None
    for key, value in message.dict().items():
        setattr(db_message, key, value)
    db.commit()
    db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int) -> Message:
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        return None
    db.delete(db_message)
    db.commit()
    return db_message
