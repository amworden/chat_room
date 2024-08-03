from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.postgres import get_db
from app.services.user import (
    get_users as fetch_users,
    add_user,
    get_user,
    update_user,
    delete_user,
)
from app.schemas import UserCreate, UserUpdate, User as UserSchema

router = APIRouter()


# Retrieve all users
@router.get(
    "/", response_description="Users retrieved", response_model=List[UserSchema]
)
async def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all users from the database.
    :param db:
    :return: list of users
    """
    users = await fetch_users(db)
    if users:
        return users
    return []


# Add a new user
@router.post(
    "/", response_description="User added into the database", response_model=UserSchema
)
async def add_user_data(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    """
    Add a new user to the database.
    :param user:
    :param db:
    :return: new user
    """
    new_user = await add_user(db, user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="User could not be added.")
    return new_user


# Retrieve a user by ID
@router.get(
    "/{id}", response_description="User data retrieved", response_model=UserSchema
)
async def get_user_data(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by ID from the database.
    :param id:
    :param db:
    :return: user data by ID
    """
    user = await get_user(db, id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User doesn't exist.")


# Update a user
@router.put(
    "/{id}",
    response_description="User data updated in the database",
    response_model=UserSchema,
)
async def update_user_data(
    id: int, req: UserUpdate = Body(...), db: Session = Depends(get_db)
):
    """

    :param id:
    :param req:
    :param db:
    :return: updated user
    """
    updated_user = await update_user(db, id, req)
    if updated_user:
        return updated_user
    raise HTTPException(
        status_code=404,
        detail="There was an error updating the user data.",
    )


# Delete a user from the database
@router.delete(
    "/{id}",
    response_description="User data deleted from the database",
    response_model=UserSchema,
)
async def delete_user_data(id: int, db: Session = Depends(get_db)):
    """
    Delete a user from the database.
    :param id:
    :param db:
    :return: deleted user
    """
    deleted_user = await delete_user(db, id)
    if deleted_user:
        return deleted_user
    raise HTTPException(status_code=404, detail=f"User with id {id} doesn't exist")
