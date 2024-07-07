from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.message import create_message, get_message, get_messages, update_message, delete_message
from app.schemas.message import Message, MessageCreate, MessageUpdate
from app.database import get_db

router = APIRouter(
    prefix="/api/messages",
    tags=["messages"],
)

@router.post("/", response_model=Message)
def create_message_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db, message)

@router.get("/{message_id}", response_model=Message)
def read_message(message_id: int, db: Session = Depends(get_db)):
    db_message = get_message(db, message_id)
    if db_message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return db_message

@router.get("/", response_model=List[Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_messages(db, skip, limit)

@router.put("/{message_id}", response_model=Message)
def update_message_endpoint(message_id: int, message: MessageUpdate, db: Session = Depends(get_db)):
    db_message = update_message(db, message_id, message)
    if db_message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return db_message

@router.delete("/{message_id}", response_model=Message)
def delete_message_endpoint(message_id: int, db: Session = Depends(get_db)):
    db_message = delete_message(db, message_id)
    if db_message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return db_message
