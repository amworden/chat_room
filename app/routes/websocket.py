from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.services.message import add_message, get_messages_by_room
from app.schemas import MessageCreate, Message as MessageSchema
from typing import List
import json

router = APIRouter()


# WebSocket connection manager
class ConnectionManager:
    """Manage WebSocket connections for broadcasting messages to all connected clients"""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# WebSocket endpoint
@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, room_id: int, db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for broadcasting messages to all connected clients.
    :param websocket:
    :param room_id:
    :param db:
    :return: websocket connection
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")  # Log received data
            try:
                # Parse JSON data from the client and create a new message object
                message_data = json.loads(data)
                new_message = MessageCreate(**message_data)
                message = await add_message(db, new_message)
                message_schema = MessageSchema.from_orm(message)
                # Broadcast the message to all connected clients
                await manager.broadcast(message_schema.json())
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                await websocket.send_text(json.dumps({"error": "Invalid JSON data"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
