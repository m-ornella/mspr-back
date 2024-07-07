from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import user, message, plant_guarding, plant_question, photo

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS settings to allow frontend URLs access
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(message.router)
app.include_router(plant_guarding.router)
app.include_router(plant_question.router)
app.include_router(photo.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/db-status")
def db_status():
    # Implementation of db status check
    pass
