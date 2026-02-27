"""WebSocket routes for chat"""
from fastapi import APIRouter, WebSocketException, status, Depends, Query
from fastapi.websockets import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import decode_token
from app.websocket.manager import manager
from app.services.chat import ChatService
from app.schemas.chat import MessageRequest
import json

router = APIRouter()


async def get_user_from_token(token: str) -> str:
    """Extract user ID from JWT token"""
    payload = decode_token(token)
    if not payload:
        return None
    return payload.get("sub")


@router.websocket("/ws/chat/{conversation_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    conversation_id: str,
    token: str = Query(...),
):
    """WebSocket endpoint for real-time chat"""
    
    # Authenticate user
    user_id = await get_user_from_token(token)
    if not user_id:
        await websocket.close(code=status.WebSocket_1008_POLICY_VIOLATION)
        return

    # Connect user
    await manager.connect(conversation_id, user_id, websocket)

    # Notify others that user is online
    await manager.broadcast(
        conversation_id,
        {
            "type": "user_joined",
            "user_id": user_id,
        },
    )

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            message_type = message_data.get("type")

            if message_type == "message":
                # Save message to database
                async with AsyncSession() as session:
                    chat_service = ChatService(session)
                    message_request = MessageRequest(
                        content=message_data.get("content")
                    )
                    saved_message = await chat_service.send_message(
                        conversation_id, user_id, message_request
                    )

                # Broadcast to others
                await manager.send_new_message(
                    conversation_id,
                    {
                        "id": saved_message.id,
                        "sender_id": saved_message.sender_id,
                        "content": saved_message.content,
                        "created_at": saved_message.created_at.isoformat(),
                    },
                )

            elif message_type == "typing":
                # Broadcast typing indicator
                await manager.send_typing_indicator(
                    conversation_id,
                    user_id,
                    message_data.get("is_typing", False),
                )

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await manager.disconnect(conversation_id, user_id, websocket)
        await manager.broadcast(
            conversation_id,
            {
                "type": "user_left",
                "user_id": user_id,
            },
        )
