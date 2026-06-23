from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from fastapi import HTTPException

from app.models import Message, Room


class MessagesRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self, room_name: str, user_id: int, text: str) -> Message:
        room = await self.session.scalar(select(Room).where(Room.name == room_name))
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")

        message = Message(
            user_id=user_id,
            room_name=room_name,
            text=text,
            created_at=datetime.now(timezone.utc),
        )

        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)

        return message
