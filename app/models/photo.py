from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Photo(Base):
    __tablename__ = "Photos"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Url = Column(String(255), nullable=False)
    PlantGuardingId = Column(Integer, ForeignKey("PlantGuarding.Id"), nullable=True)
    PlantQuestionId = Column(Integer, ForeignKey("PlantQuestions.Id"), nullable=True)

    plant_guarding = relationship("PlantGuarding", back_populates="photos")
    plant_question = relationship("PlantQuestion", back_populates="photos")