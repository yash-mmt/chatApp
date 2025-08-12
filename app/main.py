from fastapi import FastAPI
from .database import engine, Base
import uvicorn
from .models import User, ChatRoom, RoomMember, Message
from app.api import auth
from app.api import chat
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Chat App",
    description="Chat app backend without WebSocket for now",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "FastAPI Chat backend running! Implement APIs next."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)



app.include_router(auth.router, prefix="/users", tags=["Users"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

app.mount("/", StaticFiles(directory="static", html=True), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)