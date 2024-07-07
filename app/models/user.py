from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = 'User'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Surname = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    Password = Column(String(60), nullable=False)
    IsBotanist = Column(Boolean, nullable=False, default=False)
    Birthday = Column(String(50), nullable=False)

    plant_guardings = relationship("PlantGuarding", foreign_keys="[PlantGuarding.IdOwner]", back_populates="owner")
    questions = relationship("PlantQuestion", back_populates="owner")
    messages_sent = relationship("Message", foreign_keys="[Message.IdSender]", back_populates="sender")
    messages_received = relationship("Message", foreign_keys="[Message.IdReceiver]", back_populates="receiver")
    answers = relationship("Answer", back_populates="sender")

    def __repr__(self):
        return f"<User(id={self.Id}, name='{self.Name}', email='{self.Email}')>"

from .plant_guarding import PlantGuarding
from .plant_question import PlantQuestion
from .message import Message
from .answer import Answer
