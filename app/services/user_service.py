from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.repository import UserRepository


class UserService:

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def create_user_service(self, user: UserCreate) -> UserRead:

        check_user = await self.repository.get_user_by_username(user.username)
        if check_user is not None:
            raise HTTPException(400, "Username already used")

        new_user = await self.repository.create_user(user)

        return UserRead.model_validate(new_user)

    @staticmethod
    async def get_user_service(user: User) -> UserRead:
        return UserRead.model_validate(user)

    async def update_user_service(self, user, user_update: UserUpdate) -> UserRead:
        updated_user = await self.repository.update_user(user=user, user_update=user_update)

        return UserRead.model_validate(updated_user)

    async def delete_user_service(self, user: User) -> None:
        await self.repository.delete_user(user=user)
