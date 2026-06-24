from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from fastapi import HTTPException
from typing import Optional, Sequence

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

    async def get_messages_by_room(
            self,
            room_name: str,
            limit: Optional[int],
            offset: Optional[int],
            from_newest: Optional[bool]
    ) -> Sequence[Message]:

        request = select(Message).where(Message.room_name == room_name)

        if from_newest:
            request = request.order_by(Message.id.desc())
        else:
            request = request.order_by(Message.id.asc())

        if offset is not None:
            request = request.offset(offset)

        if limit is not None:
            request = request.limit(limit)

        return (await self.session.scalars(request)).all()
