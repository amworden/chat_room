from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models.room import Room
from app.models.message import Message
from app.schemas import RoomCreate, RoomUpdate


async def get_rooms(db: Session):
    """
    Retrieve all rooms from the database.
    :param db:
    :return: list of rooms
    """
    query = select(Room).options(joinedload(Room.members)).distinct()
    result = db.execute(query)
    rooms = result.unique().scalars().all()
    return rooms


async def add_room(db: Session, room: RoomCreate):
    """
    Add a new room to the database.
    :param db:
    :param room:
    :return: new room
    """
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


async def get_room(db: Session, id: int):
    """
    Retrieve a room by ID from the database.
    :param db:
    :param id:
    :return: room data by ID
    """
    room = (
        db.query(Room).options(joinedload(Room.members)).filter(Room.id == id).first()
    )
    return room


async def update_room(db: Session, id: int, room: RoomUpdate):
    """
    Update a room by ID.
    :param db:
    :param id:
    :param room:
    :return: updated room
    """
    db_room = db.query(Room).filter(Room.id == id).first()
    if db_room:
        for key, value in room.dict(exclude_unset=True).items():
            setattr(db_room, key, value)
        db.commit()
        db.refresh(db_room)
    return db_room


async def delete_room(db: Session, id: int):
    """
    Delete a room by ID.
    :param db:
    :param id:
    :return: deleted room
    """
    # Delete associated messages first
    db.query(Message).filter(Message.room_id == id).delete()
    db.commit()

    # Delete the room
    db_room = db.query(Room).filter(Room.id == id).first()
    if db_room:
        db.delete(db_room)
        db.commit()
        return db_room
    return None
