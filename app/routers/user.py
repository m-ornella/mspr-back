from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.user import create_user, get_user, get_users, update_user, delete_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.database import SessionLocal

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

@router.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(SessionLocal)):
    return create_user(db, user)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(SessionLocal)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(SessionLocal)):
    return get_users(db, skip, limit)

@router.put("/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(SessionLocal)):
    db_user = update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, db: Session = Depends(SessionLocal)):
    db_user = delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
