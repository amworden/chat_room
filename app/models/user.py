from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.postgres import Base


class User(Base):
    """Create a data model for the database to be set up for generating users,
    their rooms, messages, and identity colors"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    identity_color = Column(String)

    rooms = relationship("Room", secondary="room_members", back_populates="members")
    messages = relationship("Message", back_populates="user")
