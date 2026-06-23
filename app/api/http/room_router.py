from fastapi import APIRouter, status, Depends, Path
from typing import Annotated

from app.schemas import RoomRead, RoomCreate
from app.api.deps import db, get_current_user_http
from app.services import RoomService

room_router = APIRouter(prefix="/room", tags=["room"])


@room_router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoomRead,
                  dependencies=[Depends(get_current_user_http)])
async def create_room(
        room: RoomCreate,
        session: db
):
    service = RoomService(session=session)
    return await service.create_room_service(room)


@room_router.get("/", status_code=status.HTTP_200_OK, response_model=list[RoomRead],
                 dependencies=[Depends(get_current_user_http)])
async def get_all_rooms(
        session: db
):
    service = RoomService(session=session)
    return await service.get_all_rooms_service()


@room_router.get("/{name}", status_code=status.HTTP_200_OK, response_model=RoomRead,
                 dependencies=[Depends(get_current_user_http)])
async def get_room_by_name(
        name: Annotated[str, Path(..., title="Name of room", min_length=1, max_length=30)],
        session: db
):
    service = RoomService(session=session)
    return await service.get_room_by_name_service(name)


@room_router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user_http)])
async def delete_room(
        name: Annotated[str, Path(..., title="Name of room", min_length=1, max_length=30)],
        session: db
):
    service = RoomService(session=session)
    await service.delete_room_service(name)

    return True
