from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.schemas import RoomCreate, RoomRead
from app.repository import RoomRepository


class RoomService:

    def __init__(self, session: AsyncSession):
        self.repository = RoomRepository(session)

    async def create_room_service(self, room: RoomCreate) -> RoomRead:

        check_room = await self.repository.get_room_by_name(room.name)
        if check_room is not None:
            raise HTTPException(400, "Room already exists")

        new_room = await self.repository.create_room(room)

        return RoomRead.model_validate(new_room)

    async def get_all_rooms_service(self) -> list[RoomRead]:
        rooms = await self.repository.get_all_rooms()

        return [RoomRead.model_validate(room) for room in rooms]

    async def get_room_by_name_service(self, name: str) -> RoomRead:
        room = await self.repository.get_room_by_name(name)

        if room is None:
            raise HTTPException(404, "Room not found")

        return RoomRead.model_validate(room)

    async def delete_room_service(self, name: str) -> None:

        room = await self.repository.get_room_by_name(name)

        if room is None:
            raise HTTPException(404, "Room not found")

        await self.repository.delete_room(room)
