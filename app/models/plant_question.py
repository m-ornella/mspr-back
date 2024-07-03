from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class PlantQuestion(Base):
    __tablename__ = "PlantQuestions"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdOwner = Column(Integer, ForeignKey("User.Id"), nullable=False)
    Title = Column(String(150), nullable=False)
    Content = Column(String(1000), nullable=False)
    DateSent = Column(Date, nullable=False)

    owner = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
    photos = relationship("Photo", back_populates="plant_question")