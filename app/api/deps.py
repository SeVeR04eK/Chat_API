from typing import Annotated
from fastapi import Depends, HTTPException, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.core.security import oauth2_bearer, decode_access_token
from app.repository import UserRepository

db = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user_http(
        access_token: str = Depends(oauth2_bearer),
        session: AsyncSession = Depends(get_session)
):
    payload = decode_access_token(access_token)
    user_id = payload["id"]

    repository = UserRepository(session)
    user = await repository.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(401, "User not found")

    return user


async def get_current_user_websocket(
        access_token: str,
        session: AsyncSession,
        websocket: WebSocket
):
    try:
        payload = decode_access_token(access_token)
        user_id = payload["id"]
    except Exception:
        await websocket.close(code=1008, reason="Invalid or expired token")
        return None

    repository = UserRepository(session)
    user = await repository.get_user_by_id(user_id)

    if user is None:
        await websocket.close(code=1008, reason="User not found")
        return None

    return user

