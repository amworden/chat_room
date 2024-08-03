from sqlalchemy import Table, Column, Integer, ForeignKey
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
