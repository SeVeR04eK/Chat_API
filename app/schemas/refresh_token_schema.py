from pydantic import BaseModel, Field
from typing import Annotated


class RefreshTokenGet(BaseModel):
    refresh_token: Annotated[str, Field(..., title="Refresh Token")]
