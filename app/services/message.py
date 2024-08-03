from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Message, User
from app.schemas import MessageCreate, MessageUpdate


async def add_message(db: Session, message: MessageCreate):
    """
    Add a new message to the database.
    :param db:
    :param message:
    :return: message
    """
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages(db: Session):
    """
    Retrieve all messages from the database.
    :param db:
    :return: messages
    """
    return db.query(Message).all()


async def get_message(db: Session, id: int):
    """
    Retrieve a message by ID.
    :param db:
    :param id:
    :return: message
    """
    return db.query(Message).filter(Message.id == id).first()


def get_messages_by_room(db: Session, room_id: int):
    """
    Retrieve all messages by room ID.
    :param db:
    :param room_id:
    :return: list of messages by room ID
    """
    query = (
        select(
            Message.id,
            Message.content,
            Message.timestamp,
            Message.user_id,
            Message.room_id,
            User.id.label("user_id"),
            User.username,
            User.identity_color,
        )
        .join(User, Message.user_id == User.id)
        .where(Message.room_id == room_id)
    )
    result = db.execute(query)
    messages = result.fetchall()
    return [
        {
            "id": row.id,
            "content": row.content,
            "timestamp": row.timestamp,
            "user_id": row.user_id,
            "room_id": row.room_id,
            "user": {
                "id": row.user_id,
                "username": row.username,
                "identity_color": row.identity_color,
            },
        }
        for row in messages
    ]


async def update_message(db: Session, id: int, message: MessageUpdate):
    """
    Update a message in the database.
    :param db:
    :param id:
    :param message: updated message
    :return:
    """
    db_message = db.query(Message).filter(Message.id == id).first()
    if db_message:
        for key, value in message.dict(exclude_unset=True).items():
            setattr(db_message, key, value)
        db.commit()
        db.refresh(db_message)
    return db_message


async def delete_message(db: Session, id: int):
    """
    Delete a message from the database.
    :param db:
    :param id:
    :return: deleted message
    """
    db_message = db.query(Message).filter(Message.id == id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
        return db_message
    return None
