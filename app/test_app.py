
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models import Room, User, Message

import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app

client = TestClient(app)


# Fixture to get the database session
@pytest.fixture(scope="module")
def db_session():
    db = next(get_db())
    yield db
    db.close()


# All tests in one spot for quick testing


# Users tests
def test_get_all_users(db_session: Session):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_user_data(db_session: Session):
    user_data = {"username": "testuser", "identity_color": "blue"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["identity_color"] == "blue"
    # Clean up
    user_id = response.json()["id"]
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.commit()


def test_get_user_data(db_session: Session):
    user_data = {"username": "testuser2", "identity_color": "red"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    # Clean up
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.commit()


def test_update_user_data(db_session: Session):
    user_data = {"username": "testuser3", "identity_color": "green"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    updated_data = {"username": "updateduser", "identity_color": "yellow"}
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"
    assert response.json()["identity_color"] == "yellow"
    # Clean up
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.commit()


def test_delete_user_data(db_session: Session):
    user_data = {"username": "testuser4", "identity_color": "purple"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    # Clean up not needed as user is deleted


# Rooms tests
def test_get_all_rooms(db_session: Session):
    response = client.get("/rooms/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_room_data(db_session: Session):
    room_data = {"name": "testroom"}
    response = client.post("/rooms/", json=room_data)
    assert response.status_code == 200
    assert response.json()["name"] == "testroom"
    # Clean up
    room_id = response.json()["id"]
    db_session.query(Room).filter(Room.id == room_id).delete()
    db_session.commit()


def test_get_room_data(db_session: Session):
    room_data = {"name": "testroom2"}
    response = client.post("/rooms/", json=room_data)
    room_id = response.json()["id"]

    response = client.get(f"/rooms/{room_id}")
    assert response.status_code == 200
    assert response.json()["id"] == room_id
    # Clean up
    db_session.query(Room).filter(Room.id == room_id).delete()
    db_session.commit()


def test_update_room_data(db_session: Session):
    room_data = {"name": "testroom3"}
    response = client.post("/rooms/", json=room_data)
    room_id = response.json()["id"]

    updated_data = {"name": "updatedroom"}
    response = client.put(f"/rooms/{room_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "updatedroom"
    # Clean up
    db_session.query(Room).filter(Room.id == room_id).delete()
    db_session.commit()


def test_delete_room_data(db_session: Session):
    room_data = {"name": "testroom4"}
    response = client.post("/rooms/", json=room_data)
    room_id = response.json()["id"]

    response = client.delete(f"/rooms/{room_id}")
    assert response.status_code == 200
    # Clean up not needed as room is deleted


def test_join_room(db_session: Session):
    user_data = {"username": "testuser5", "identity_color": "orange"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    room_data = {"name": "testroom5"}
    response = client.post("/rooms/", json=room_data)
    room_id = response.json()["id"]

    response = client.post(f"/rooms/{room_id}/join", params={"user_id": user_id})
    assert response.status_code == 200
    # Clean up
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.query(Room).filter(Room.id == room_id).delete()
    db_session.commit()


# Messages tests
def test_get_all_messages(db_session: Session):
    response = client.get("/messages/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_message_data(db_session: Session):
    user_data = {"username": "testuser6", "identity_color": "brown"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    room_data = {"name": "testroom6"}
    response = client.post("/rooms/", json=room_data)
    room_id = response.json()["id"]

    message_data = {"user_id": user_id, "room_id": room_id, "content": "test message"}
    response = client.post("/messages/", json=message_data)
    assert response.status_code == 200
    assert response.json()["content"] == "test message"
    # Clean up
    message_id = response.json()["id"]
    db_session.query(Message).filter(Message.id == message_id).delete()
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.query(Room).filter(Room.id == room_id).delete()
    db_session.commit()


def test_get_message_data(db_session: Session):
    user_data = {"username": "testuser7", "identity_color": "cyan"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    room_data = {"name": "testroom7"}
    response = client.post("/rooms/", json=room_data)
    room_id = response.json()["id"]

    message_data = {"user_id": user_id, "room_id": room_id, "content": "test message"}
    response = client.post("/messages/", json=message_data)
    message_id = response.json()["id"]

    response = client.get(f"/messages/{message_id}")
    assert response.status_code == 200
    assert response.json()["id"] == message_id
    # Clean up
    db_session.query(Message).filter(Message.id == message_id).delete()
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.query(Room).filter(Room.id == room_id).delete()
    db_session.commit()


def test_update_message_data(db_session: Session):
    user_data = {"username": "testuser8", "identity_color": "magenta"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    room_data = {"name": "testroom8"}
    response = client.post("/rooms/", json=room_data)
    room_id = response.json()["id"]

    message_data = {"user_id": user_id, "room_id": room_id, "content": "test message"}
    response = client.post("/messages/", json=message_data)
    message_id = response.json()["id"]

    updated_data = {
        "user_id": user_id,
        "room_id": room_id,
        "content": "updated message",
    }
    response = client.put(f"/messages/{message_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["content"] == "updated message"
    # Clean up
    db_session.query(Message).filter(Message.id == message_id).delete()
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.query(Room).filter(Room.id == room_id).delete()
    db_session.commit()


def test_get_messages_for_room(db_session: Session):
    user_data = {"username": "testuser10", "identity_color": "silver"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]

    room_data = {"name": "testroom10"}
    response = client.post("/rooms/", json=room_data)
    room_id = response.json()["id"]

    message_data = {"user_id": user_id, "room_id": room_id, "content": "test message"}
    response = client.post("/messages/", json=message_data)

    response = client.get(f"/messages/room/{room_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Clean up
    db_session.query(Message).filter(Message.room_id == room_id).delete()
    db_session.query(User).filter(User.id == user_id).delete()
    db_session.query(Room).filter(Room.id == room_id).delete()
    db_session.commit()
