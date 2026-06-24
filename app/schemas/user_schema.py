from pydantic import BaseModel, Field, model_validator
from typing import Annotated


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    username: Annotated[
        str,
        Field(..., min_length=1, title="Username")
    ]
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            max_length=128,
            title="User Password"
        )
    ]
    password_confirm: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            max_length=128,
            title="User Password Confirm"
        )
    ]

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class UserUpdate(UserBase):
    username: Annotated[
        str,
        Field(default=None, min_length=1, title="Username")
    ]
    password: Annotated[
        str,
        Field(
            default=None,
            min_length=8,
            max_length=128,
            title="User Password"
        )
    ]
    password_confirm: Annotated[
        str,
        Field(
            default=None,
            min_length=8,
            max_length=128,
            title="User Password Confirm"
        )
    ]

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password is not None or self.password_confirm is not None:
            if self.password is None or self.password_confirm is None:
                raise ValueError("Both password and password_confirm must be provided to change password")
            if self.password != self.password_confirm:
                raise ValueError("Passwords do not match")
        return self


class UserRead(UserBase):
    username: Annotated[str, Field(title="Username")]
    id: Annotated[int, Field(title="User ID")]

    model_config = {
        "from_attributes": True
    }

class OnlineUsersCount(BaseModel):
    count: int
