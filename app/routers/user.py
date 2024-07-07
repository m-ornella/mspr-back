from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from app.crud.user import create_user, get_user_by_email, authenticate_user, create_access_token, get_user, get_users, update_user, delete_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.database import get_db
from pydantic import BaseModel

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signin")
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with the given details and return a JWT token.
    """
    db_user = get_user_by_email(db, user.Email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = create_user(db, user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.Email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": new_user}

@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.
    """
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.Email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user details by user ID.
    """
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of users.
    """
    return get_users(db, skip, limit)

@router.put("/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user details by user ID.
    """
    db_user = update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user by user ID.
    """
    db_user = delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
