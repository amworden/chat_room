from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .room import Room
from .message import Message
