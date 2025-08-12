from fastapi import FastAPI
from .database import engine, Base
import uvicorn
from .models import User, ChatRoom, RoomMember, Message
from app.api import auth

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


app = FastAPI()

app.include_router(auth.router, prefix="/users", tags=["Users"])