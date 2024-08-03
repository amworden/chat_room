from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.postgres import get_db
from app.services.room import (
    get_rooms as fetch_rooms,
    add_room,
    get_room,
    update_room,
    delete_room,
)
from app.schemas import RoomCreate, RoomUpdate, Room as RoomSchema, User as UserSchema
from app.models.room import Room
from app.models.user import User

router = APIRouter()


# Retrieve all rooms
@router.get(
    "/", response_description="Rooms retrieved", response_model=List[RoomSchema]
)
async def get_all_rooms(db: Session = Depends(get_db)):
    """
    Retrieve all rooms from the database.
    :param db:
    :return: list of rooms
    """
    rooms = await fetch_rooms(db)
    return rooms


# Add a new room
@router.post(
    "/", response_description="Room added into the database", response_model=RoomSchema
)
async def add_room_data(room: RoomCreate = Body(...), db: Session = Depends(get_db)):
    """
    Add a new room to the database.
    :param room:
    :param db:
    :return: new room
    """
    new_room = await add_room(db, room)
    if new_room is None:
        raise HTTPException(status_code=400, detail="Room could not be added.")
    return new_room


# Retrieve a room by ID
@router.get(
    "/{id}", response_description="Room data retrieved", response_model=RoomSchema
)
async def get_room_data(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a room by ID from the database.
    :param id:
    :param db:
    :return: room data by ID
    """
    room = await get_room(db, id)
    if room:
        return room
    raise HTTPException(status_code=404, detail="Room doesn't exist.")


# Update a room
@router.put(
    "/{id}",
    response_description="Room data updated in the database",
    response_model=RoomSchema,
)
async def update_room_data(
    id: int, req: RoomUpdate = Body(...), db: Session = Depends(get_db)
):
    """
    Update a room in the database.
    :param id:
    :param req:
    :param db:
    :return: updated room
    """
    updated_room = await update_room(db, id, req)
    if updated_room:
        return updated_room
    raise HTTPException(
        status_code=404,
        detail="There was an error updating the room data.",
    )


# Delete a room from the database
@router.delete(
    "/{id}",
    response_description="Room data deleted from the database",
    response_model=RoomSchema,
)
async def delete_room_data(id: int, db: Session = Depends(get_db)):
    """
    Delete a room from the database.
    :param id:
    :param db:
    :return: confirmation message
    """
    deleted_room = await delete_room(db, id)
    if deleted_room:
        return deleted_room
    raise HTTPException(status_code=404, detail=f"Room with id {id} doesn't exist")


# Join a room
@router.post("/{room_id}/join", response_model=RoomSchema)
async def join_room(room_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Join a room by user ID.
    :param room_id:
    :param user_id:
    :param db:
    :return: room joined by user
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    user = db.query(User).filter(User.id == user_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    room.members.append(user)
    db.commit()
    db.refresh(room)

    return room
