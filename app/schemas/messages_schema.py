from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


class MessageRead(BaseModel):
    id: Annotated[int, Field(title="Message ID")]
    room_name: Annotated[str, Field(title="Room name")]
    user_id: Annotated[int, Field(title="User ID")]
    text: Annotated[str, Field(title="Message text")]
    created_at: Annotated[datetime, Field(title="Created at")]

    model_config = {
        "from_attributes": True
    }
