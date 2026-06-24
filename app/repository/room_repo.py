from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from typing import Optional, Sequence

from app.models import Room
from app.schemas import RoomCreate


class RoomRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_room(self, room: RoomCreate) -> Room:
        room = Room(
            name=room.name,
            created_at=datetime.now(timezone.utc)
        )

        self.session.add(room)
        await self.session.commit()
        await self.session.refresh(room)

        return room

    async def get_all_rooms(
            self,
            limit: Optional[int],
            offset: Optional[int],
            from_newest: Optional[bool]
    ) -> Sequence[Room]:

        request = select(Room)

        if from_newest:
            request = request.order_by(Room.id.desc())
        else:
            request = request.order_by(Room.id.asc())

        if offset is not None:
            request = request.offset(offset)

        if limit is not None:
            request = request.limit(limit)

        return (await self.session.scalars(request)).all()


    async def get_room_by_name(self, name: str) -> Room:
        request = (select(Room).where(Room.name == name))

        return await self.session.scalar(request)

    async def delete_room(self, room: Room) -> None:
        await self.session.delete(room)
        await self.session.commit()
