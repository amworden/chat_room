from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.postgres import Base
from datetime import datetime


class Message(Base):
    """Create a data model for the database to be set up for generating messages"""
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user = relationship("User", back_populates="messages")
    room = relationship("Room", back_populates="messages")
