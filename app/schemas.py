from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """
    Base schema for User
    """
    username: str
    identity_color: str


class UserCreate(UserBase):
    """
    Schema for creating a new User
    """
    pass


class UserUpdate(UserBase):
    """
    Schema for updating an existing User
    """
    username: Optional[str] = None
    identity_color: Optional[str] = None


class User(UserBase):
    """
    Schema for User
    """
    id: int
    rooms: List["RoomSimplified"] = []

    class Config:
        orm_mode = True
        from_attributes = True


class RoomBase(BaseModel):
    """
    Base schema for Room
    """
    name: str


class RoomCreate(RoomBase):
    """
    Schema for creating a new Room
    """
    pass


class RoomUpdate(RoomBase):
    """
    Schema for updating an existing Room
    """
    name: Optional[str] = None


class Room(RoomBase):
    """
    Schema for Room
    """
    id: int
    members: List[User] = []
    messages: List["Message"] = []

    class Config:
        orm_mode = True
        from_attributes = True


class RoomSimplified(RoomBase):
    """
    Simplified schema for Room
    """
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class MessageBase(BaseModel):
    """
    Base schema for Message
    """
    user_id: int
    room_id: int
    content: str


class MessageCreate(MessageBase):
    """
    Schema for creating a new Message
    """
    pass


class MessageUpdate(MessageBase):
    """
    Schema for updating an existing Message
    """
    content: Optional[str] = None


class Message(MessageBase):
    """
    Schema for Message
    """
    id: int
    timestamp: datetime
    user: User  # Include User schema for user details

    class Config:
        orm_mode = True
        from_attributes = True
