from fastapi import WebSocket
import json
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        # user_id: WebSocket
        self.active_connections: Dict[int, WebSocket] = {}
        # room_id: set[user_id]
        self.room_connections: Dict[int, set] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        # Remove user from all rooms
        for room_id in self.room_connections:
            if user_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(user_id)

    async def join_room(self, user_id: int, room_id: int):
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        self.room_connections[room_id].add(user_id)

    async def leave_room(self, user_id: int, room_id: int):
        if room_id in self.room_connections and user_id in self.room_connections[room_id]:
            self.room_connections[room_id].remove(user_id)

    async def broadcast_to_room(self, message: str, room_id: int, include_sender: bool = False):
        if room_id in self.room_connections:
            for user_id in self.room_connections[room_id]:
                if user_id in self.active_connections:
                    if include_sender or user_id != sender_id:
                        try:
                            await self.active_connections[user_id].send_text(message)
                        except:
                            self.disconnect(user_id)