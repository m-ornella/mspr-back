from sqlalchemy import Column, Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from ..database import Base

class Photo(Base):
    __tablename__ = "Photos"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Photo = Column(LargeBinary, nullable=False)
    PlantGuardingId = Column(Integer, ForeignKey("PlantGuarding.Id"), nullable=True)
    PlantQuestionId = Column(Integer, ForeignKey("PlantQuestions.Id"), nullable=True)

    plant_guarding = relationship("PlantGuarding", back_populates="photos")
    plant_question = relationship("PlantQuestion", back_populates="photos")

from .plant_guarding import PlantGuarding
from .plant_question import PlantQuestion
