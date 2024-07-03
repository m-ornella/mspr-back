from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class PlantGuarding(Base):
    __tablename__ = "PlantGuarding"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdOwner = Column(Integer, ForeignKey("User.Id"), nullable=False)
    IdGuard = Column(Integer, ForeignKey("User.Id"))
    Name = Column(String(100), nullable=False)
    Description = Column(String(255))
    DateStart = Column(Date, nullable=False)
    DateEnd = Column(Date)
    Location = Column(String(100))

    owner = relationship("User", foreign_keys=[IdOwner], back_populates="plant_guardings")
    guard = relationship("User", foreign_keys=[IdGuard])
    photos = relationship("Photo", back_populates="plant_guarding")
