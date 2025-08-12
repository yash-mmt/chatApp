from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.core.constants import MessageType

class MessageCreate(BaseModel):
    content: Optional[str] = None
    file_url: Optional[str] = None
    message_type: MessageType = MessageType.TEXT
    room_id: int

class MessageOut(MessageCreate):
    id: int
    sender_id: int
    timestamp: datetime
    is_read: bool

    class Config:
        orm_mode = True