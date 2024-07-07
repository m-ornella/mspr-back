from sqlalchemy.orm import Session
from app.models.plant_guarding import PlantGuarding
from app.schemas.plant_guarding import PlantGuardingCreate, PlantGuardingUpdate

def create_plant_guarding(db: Session, plant_guarding: PlantGuardingCreate) -> PlantGuarding:
    db_plant_guarding = PlantGuarding(**plant_guarding.dict())
    db.add(db_plant_guarding)
    db.commit()
    db.refresh(db_plant_guarding)
    return db_plant_guarding

def get_plant_guarding(db: Session, guarding_id: int) -> PlantGuarding:
    return db.query(PlantGuarding).filter(PlantGuarding.id == guarding_id).first()

def get_plant_guardings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PlantGuarding).offset(skip).limit(limit).all()

def update_plant_guarding(db: Session, guarding_id: int, guarding: PlantGuardingUpdate) -> PlantGuarding:
    db_plant_guarding = db.query(PlantGuarding).filter(PlantGuarding.id == guarding_id).first()
    if db_plant_guarding is None:
        return None
    for key, value in guarding.dict().items():
        setattr(db_plant_guarding, key, value)
    db.commit()
    db.refresh(db_plant_guarding)
    return db_plant_guarding

def delete_plant_guarding(db: Session, guarding_id: int) -> PlantGuarding:
    db_plant_guarding = db.query(PlantGuarding).filter(PlantGuarding.id == guarding_id).first()
    if db_plant_guarding is None:
        return None
    db.delete(db_plant_guarding)
    db.commit()
    return db_plant_guarding
