from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database.postgres import Base

# Association table for many-to-many relationship between rooms and users
room_members = Table(
    "room_members",
    Base.metadata,
    Column(
        "room_id", Integer, ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Room(Base):
    """Create a data model for the database to be set up for generating rooms and their members"""
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    members = relationship("User", secondary=room_members, back_populates="rooms")
    messages = relationship("Message", back_populates="room", cascade="all, delete")
