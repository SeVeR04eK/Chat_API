from fastapi import APIRouter, status, Depends, Path, HTTPException
from typing import Annotated

from app.schemas import MessageRead
from app.api.deps import db, get_current_user_http
from app.repository import RoomRepository

history_router = APIRouter(prefix="/history", tags=["messages"])


@history_router.get("/{name}", status_code=status.HTTP_200_OK, response_model=list[MessageRead],
                    dependencies=[Depends(get_current_user_http)])
async def get_all_messages(
        session: db,
        name: Annotated[str, Path(..., title="Name of room", min_length=1, max_length=30)]
):
    room_repository = RoomRepository(session)

    room = await room_repository.get_room_by_name(name)

    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    return [MessageRead.model_validate(message) for message in room.messages]
