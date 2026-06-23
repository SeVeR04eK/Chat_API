from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Path
from sqlalchemy import select
from typing import Annotated

from app.api.websockets.manager import ConnectionManager
from app.models import Room
from app.api.deps import db, get_current_user_websocket
from app.repository import MessagesRepository

chat_router = APIRouter()
manager = ConnectionManager()


@chat_router.websocket("/ws/{name}")
async def websocket_endpoint(
        websocket: WebSocket,
        name: Annotated[str, Path(..., title="Name of room", min_length=1, max_length=30)],
        session: db
):
    token = websocket.query_params.get("token")
    if token is None:
        await websocket.close(code=1008, reason="Missing token")
        return

    user = await get_current_user_websocket(token, session, websocket)
    if user is None:
        return

    room = await session.scalar(select(Room).where(Room.name == name))
    if room is None:
        await websocket.close(code=1008, reason="Invalid room")
        return

    await websocket.accept()
    await manager.connect(name, websocket)

    repository = MessagesRepository(session)

    try:
        while True:
            data = await websocket.receive_text()
            if not data.strip():
                continue
            try:
                await repository.create_message(user_id=user.id, room_name=name, text=data)
                await manager.broadcast(name, data)
            except Exception as e:
                await websocket.send_text(f"Error sending message: {str(e)}")

    except WebSocketDisconnect:
        manager.disconnect(name, websocket)
    except Exception as e:
        await websocket.close(code=1011, reason=f"Server error: {str(e)}")
        manager.disconnect(name, websocket)

