from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

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

    async def get_all_rooms(self) -> list[Room]:
        request = select(Room)

        result = await self.session.execute(request)

        return list(result.scalars().all())

    async def get_room_by_name(self, name: str) -> Room:
        request = (select(Room)
                   .options(selectinload(Room.messages))
                   .where(Room.name == name))

        return await self.session.scalar(request)

    async def delete_room(self, room: Room) -> None:
        await self.session.delete(room)
        await self.session.commit()
