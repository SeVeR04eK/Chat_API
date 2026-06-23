from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from app.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    messages: Mapped[list["Message"]] = relationship(back_populates="user", cascade="all, delete-orphan")
