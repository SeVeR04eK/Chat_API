from fastapi import APIRouter, status, Depends, Path, HTTPException, Query
from typing import Annotated, Optional

from app.schemas import MessageRead
from app.api.deps import db, get_current_user_http
from app.repository import MessagesRepository

history_router = APIRouter(prefix="/history", tags=["messages"])


@history_router.get("/{name}", status_code=status.HTTP_200_OK, response_model=list[MessageRead],
                    dependencies=[Depends(get_current_user_http)])
async def get_all_messages(
        session: db,
        name: Annotated[
            str,
            Path(..., title="Name of room", min_length=1, max_length=30)
        ],
        limit: Annotated[
            Optional[int],
            Query(title="Limit of messages", ge=1, le=100)
        ] = None,
        offset: Annotated[
            Optional[int],
            Query(title="Offset of messages", ge=0, le=100)
        ] = None,
        from_newest: Annotated[
            Optional[bool],
            Query(title="Sort from newest")] = False,
):
    messages_repository = MessagesRepository(session)
    
    messages = await messages_repository.get_messages_by_room(
        name, limit, offset, from_newest
    )
    
    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    
    return [MessageRead.model_validate(message) for message in messages]
