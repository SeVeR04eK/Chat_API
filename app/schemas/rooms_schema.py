from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime, timezone


class RoomBase(BaseModel):
    name: str


class RoomCreate(RoomBase):
    name: Annotated[
        str,
        Field(..., min_length=1, title="Name of room", max_length=30)
    ]


class RoomRead(RoomBase):
    id: Annotated[int, Field(title="Room ID")]
    name: Annotated[str, Field(title="Name of room")]
    created_at: Annotated[datetime, Field(title="Created at")]

    model_config = {
        "from_attributes": True
    }
