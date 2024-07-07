from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class PlantGuarding(Base):
    __tablename__ = "PlantGuarding"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdOwner = Column(Integer, ForeignKey("User.Id"), nullable=False)
    IdGuard = Column(Integer, ForeignKey("User.Id"), nullable=True)
    Name = Column(String(100), nullable=False)
    Description = Column(String(255), nullable=True)
    DateStart = Column(Date, nullable=False)
    DateEnd = Column(Date, nullable=True)
    Location = Column(String(100), nullable=True)

    owner = relationship("User", foreign_keys=[IdOwner], back_populates="plant_guardings")
    guard = relationship("User", foreign_keys=[IdGuard])
    photos = relationship("Photo", back_populates="plant_guarding")

from .user import User
from .photo import Photo