"""WebSocket connection manager for real-time chat"""
from typing import Dict, List, Set
import json


class ConnectionManager:
    """Manage WebSocket connections for chat"""

    def __init__(self):
        # conversation_id -> set of connected user IDs
        self.active_connections: Dict[str, Set[tuple]] = {}

    async def connect(self, conversation_id: str, user_id: str, websocket):
        """Connect user to conversation"""
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = set()

        self.active_connections[conversation_id].add((user_id, websocket))
        await websocket.accept()

    async def disconnect(self, conversation_id: str, user_id: str, websocket):
        """Disconnect user from conversation"""
        if conversation_id in self.active_connections:
            self.active_connections[conversation_id].discard((user_id, websocket))
            if not self.active_connections[conversation_id]:
                del self.active_connections[conversation_id]

    async def broadcast(self, conversation_id: str, data: dict):
        """Broadcast message to all users in conversation"""
        if conversation_id not in self.active_connections:
            return

        for user_id, websocket in self.active_connections[conversation_id]:
            try:
                await websocket.send_json(data)
            except Exception as e:
                print(f"Error sending message: {e}")

    async def send_typing_indicator(
        self, conversation_id: str, user_id: str, is_typing: bool
    ):
        """Send typing indicator"""
        data = {
            "type": "typing",
            "user_id": user_id,
            "is_typing": is_typing,
        }
        await self.broadcast(conversation_id, data)

    async def send_new_message(
        self, conversation_id: str, message_data: dict
    ):
        """Broadcast new message"""
        data = {
            "type": "message",
            "message": message_data,
        }
        await self.broadcast(conversation_id, data)


# Global connection manager
manager = ConnectionManager()
