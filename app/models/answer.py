from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Answer(Base):
    __tablename__ = "Answers"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdSender = Column(Integer, ForeignKey("User.Id"), nullable=False)
    IdQuestion = Column(Integer, ForeignKey("PlantQuestions.Id"), nullable=False)
    Content = Column(String(1000), nullable=False)
    DateSent = Column(Date, nullable=False)
    Picture = Column(String(255))

    sender = relationship("User", back_populates="answers")
    question = relationship("PlantQuestion", back_populates="answers")