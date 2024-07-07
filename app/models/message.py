from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.database import Base

class Message(Base):
    __tablename__ = "Messages"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    IdSender = Column(Integer, ForeignKey("User.Id"), nullable=False)
    IdReceiver = Column(Integer, ForeignKey("User.Id"), nullable=False)
    Content = Column(String(1000), nullable=False)
    DateSent = Column(Date, nullable=False)

    sender = relationship("User", foreign_keys=[IdSender])
    receiver = relationship("User", foreign_keys=[IdReceiver])

from .user import User