from app import schemas
from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from sqlalchemy.orm import Session
import app.crud as crud
import app.models.user, app.models.answer, app.models.message, app.models.plant_guarding, app.models.plant_question
# app.models.plant_type
from app.models.user import User
from app.models.message import Message
from app.models.plant_guarding import PlantGuarding
from app.models.plant_question import PlantQuestion
from app.models.photo import Photo
# from app.models.plant_type import PlantType
from app.models.answer import Answer
from app.database import SessionLocal, engine, Base
from .database import SessionLocal, engine, Base
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt
import shutil
import os

from fastapi.middleware.cors import CORSMiddleware

app.database.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configure CORS settings to allow frontend urls access
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# # Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/db-status")
def db_status(db: Session = Depends(SessionLocal)):
    try:
        db.execute("SELECT * FROM User;") 
        return {"status": "Database connection OK"}
    except Exception as e:
        return {"status": "Database connection error", "error": str(e)}


# Fonction pour vérifier le token JWT et récupérer les informations d'identification de l'utilisateur
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id


# Endpoint protégé nécessitant une authentification
@app.delete("/api/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Vérifiez si l'utilisateur courant est autorisé à supprimer le compte utilisateur
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this user",
        )
    # Si l'utilisateur est autorisé, supprimez le compte utilisateur
    return crud.delete_user(db, user_id)


@app.post("/api/users/signin")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user


@app.post("/api/users/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.Email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# GET /api/plantsQuestions
@app.get("/api/plantsQuestions")
def read_plant_questions(db: Session = Depends(get_db)):
    return crud.get_plant_questions(db)


# GET /api/plantsQuestions/:id
@app.get("/api/plantsQuestions/{question_id}")
def read_plant_question(question_id: int, db: Session = Depends(get_db)):
    question = crud.get_plant_question_by_id(db, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# GET /api/plantsGuarding
@app.get("/api/plantsGuarding")
def read_plant_guardings(db: Session = Depends(get_db)):
    return crud.get_plant_guardings(db)


# GET /api/plantsGuarding/:id
@app.get("/api/plantsGuarding/{guarding_id}")
def read_plant_guarding(guarding_id: int, db: Session = Depends(get_db)):
    guarding = crud.get_plant_guarding_by_id(db, guarding_id)
    if guarding is None:
        raise HTTPException(status_code=404, detail="Guarding session not found")
    return guarding


# PUT /api/plantsGuarding/:id
@app.put("/api/plantsGuarding/{guarding_id}")
def update_plant_guarding(
    guarding_id: int,
    guarding: schemas.PlantGuardingCreate,
    db: Session = Depends(get_db),
):
    return crud.update_plant_guarding(db, guarding_id, guarding)


# DELETE /api/plantsGuarding/:id
@app.delete("/api/plantsGuarding/{guarding_id}")
def create_plant_guarding(
    name: str,
    description: str,
    date_start: str,
    date_end: str,
    location: str,
    id_owner: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Ensure the uploads directory exists
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Save the uploaded file
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    plant_guarding_data = schemas.PlantGuardingCreate(
        Name=name,
        Description=description,
        DateStart=date_start,
        DateEnd=date_end,
        Location=location,
        IdOwner=id_owner,
        photos=[schemas.PhotoCreate(Url=file_path)]
    )
    return crud.create_plant_guarding(db=db, plant_guarding=plant_guarding_data)

# POST /api/plantsQuestions
@app.post("/api/plantsQuestions")
def create_plant_question(
    title: str,
    content: str,
    date_sent: str,
    id_owner: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Ensure the uploads directory exists
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Save the uploaded file
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    plant_question_data = schemas.PlantQuestionCreate(
        Title=title,
        Content=content,
        DateSent=date_sent,
        IdOwner=id_owner,
        photos=[schemas.PhotoCreate(Url=file_path)]
    )
    return crud.create_plant_question(db=db, plant_question=plant_question_data)


# POST /api/plantsGuarding
def create_plant_guarding(plant_guarding: schemas.PlantGuardingCreate, db: Session = Depends(get_db)):
    return crud.create_plant_guarding(db=db, plant_guarding=plant_guarding)


# POST /api/message/:IdSender:IdReceiver
@app.post("/api/message/{sender_id}/{receiver_id}")
def create_message(
    sender_id: int,
    receiver_id: int,
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
):
    return crud.create_message(db, message, sender_id, receiver_id)


# PUT /api/plantsQuestions/:id
@app.put("/api/plantsQuestions/{question_id}")
def update_plant_question(
    question_id: int,
    question: schemas.PlantQuestionCreate,
    db: Session = Depends(get_db),
):
    return crud.update_plant_question(db, question_id, question)


# PUT /api/plantsGuarding/:id
@app.put("/api/plantsGuarding/{guarding_id}")
def update_plant_guarding(
    guarding_id: int,
    guarding: schemas.PlantGuardingCreate,
    db: Session = Depends(get_db),
):
    return crud.update_plant_guarding(db, guarding_id, guarding)


# PUT /api/messages/:id
@app.put("/api/messages/{message_id}")
def update_message(
    message_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)
):
    return crud.update_message(db, message_id, message)


# DELETE /api/users/:id
@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)


# DELETE /api/plantsGuarding/:id
@app.delete("/api/plantsGuarding/{guarding_id}")
def delete_plant_guarding(guarding_id: int, db: Session = Depends(get_db)):
    return crud.delete_plant_guarding(db, guarding_id)


# DELETE /api/message/:id
@app.delete("/api/message/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    return crud.delete_message(db, message_id)
