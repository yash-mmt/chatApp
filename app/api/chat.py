from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket_manager import ConnectionManager
from app.models import Message
from app.database import SessionLocal
import json
from app.models.chat import User
from app.services.user_service import get_user_id_from_token
from starlette import status
router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    db = SessionLocal()
    try:
        # Authenticate user
        user_id = get_user_id_from_token(token, db)
        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        await manager.connect(websocket, user_id)
        
        try:
            while True:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                if message_data.get("type") == "join_room":
                    room_id = message_data["room_id"]
                    await manager.join_room(user_id, room_id)
                    
                elif message_data.get("type") == "message":
                    room_id = message_data["room_id"]
                    content = message_data.get("content", "")
                    
                    # Save message to database
                    message = Message(
                        content=content,
                        sender_id=user_id,
                        room_id=room_id
                    )
                    db.add(message)
                    db.commit()
                    db.refresh(message)
                    
                    # Broadcast to room members
                    await manager.broadcast_to_room(
                        json.dumps({
                            "type": "message",
                            "content": content,
                            "sender_id": user_id,
                            "room_id": room_id,
                            "timestamp": message.timestamp.isoformat()
                        }),
                        room_id,
                        include_sender=True
                    )
                    
        except WebSocketDisconnect:
            manager.disconnect(user_id)
    finally:
        db.close()