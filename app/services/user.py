from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models.user import User
from app.schemas import UserCreate, UserUpdate


async def get_users(db: Session):
    """
    Retrieve all users from the database.
    :param db:
    :return: list of users
    """
    query = select(User).options(joinedload(User.rooms)).distinct()
    result = db.execute(query)
    users = result.unique().scalars().all()
    return users


async def add_user(db: Session, user: UserCreate):
    """
    Add a new user to the database.
    :param db:
    :param user:
    :return: new user
    """
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user(db: Session, id: int):
    """
    Retrieve a user by ID from the database.
    :param db:
    :param id:
    :return: user data by ID
    """
    query = select(User).where(User.id == id).options(joinedload(User.rooms))
    result = db.execute(query)
    user = result.unique().scalar_one_or_none()
    return user


async def update_user(db: Session, id: int, user: UserUpdate):
    """
    Update a user by ID.
    :param db:
    :param id:
    :param user:
    :return: updated user
    """
    db_user = db.query(User).filter(User.id == id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


async def delete_user(db: Session, id: int):
    """
    Delete a user by ID.
    :param db:
    :param id:
    :return: deleted user
    """
    db_user = db.query(User).filter(User.id == id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
