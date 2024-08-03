from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, room, message, websocket
from app.database.postgres import database

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Frontend URL
    "http://localhost:8000",  # Backend URL
]

# Keep it simple for now and allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# instantiate routers
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(room.router, prefix="/rooms", tags=["rooms"])
app.include_router(message.router, prefix="/messages", tags=["messages"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/")
async def read_root():
    return {"message": "Lets Chat!"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
