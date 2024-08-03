from typing import List

from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.schemas import MessageCreate, MessageUpdate, Message as MessageSchema
from app.services.message import (
    get_messages,
    add_message,
    get_message,
    update_message,
    delete_message,
    get_messages_by_room,
)

router = APIRouter()


# Retrieve all messages
@router.get(
    "/", response_description="Messages retrieved", response_model=List[MessageSchema]
)
def get_all_messages(db: Session = Depends(get_db)):
    """
    Retrieve all messages from the database.
    :param db:
    :return: list of messages
    """
    messages = get_messages(db)
    if messages:
        return messages
    return []


# Add a new message
@router.post(
    "/",
    response_description="Message added into the database",
    response_model=MessageSchema,
)
async def add_message_data(
    message: MessageCreate = Body(...), db: Session = Depends(get_db)
):
    """
    Add a new message to the database.
    :param message:
    :param db:
    :return: new message
    """
    new_message = await add_message(db, message)
    return new_message


# Retrieve a message by ID
@router.get(
    "/{id}", response_description="Message data retrieved", response_model=MessageSchema
)
async def get_message_data(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a message by ID.
    :param id:
    :param db:
    :return: message
    """
    message = await get_message(db, id)
    if message:
        return message
    raise HTTPException(status_code=404, detail="Message doesn't exist.")


# Retrieve messages by room ID
@router.get(
    "/room/{room_id}",
    response_description="Messages retrieved by room ID",
    response_model=List[MessageSchema],
)
def get_messages_for_room(room_id: int, db: Session = Depends(get_db)):
    """
    Retrieve messages by room ID.
    :param room_id:
    :param db:
    :return: list of messages by room ID
    """
    messages = get_messages_by_room(db, room_id)
    if messages:
        return messages
    return []


# Update a message
@router.put(
    "/{id}",
    response_description="Message data updated in the database",
    response_model=MessageSchema,
)
async def update_message_data(
    id: int, req: MessageUpdate = Body(...), db: Session = Depends(get_db)
):
    """
    Update a message in the database.
    :param id:
    :param req:
    :param db:
    :return: updated message
    """
    updated_message = await update_message(db, id, req)
    if updated_message:
        return updated_message
    raise HTTPException(
        status_code=404,
        detail="There was an error updating the message data.",
    )


# Delete a message from the database
@router.delete(
    "/{id}",
    response_description="Message data deleted from the database",
    response_model=MessageSchema,
)
async def delete_message_data(id: int, db: Session = Depends(get_db)):
    """
    Delete a message from the database.
    :param id:
    :param db:
    :return: deleted message confirmation
    """
    deleted_message = await delete_message(db, id)
    if deleted_message:
        return deleted_message
    raise HTTPException(status_code=404, detail=f"Message with id {id} doesn't exist")
