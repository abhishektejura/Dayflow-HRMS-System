from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(
        index=True,
        nullable=False,
        sa_column_kwargs={"unique": True}
    )

    password_hash: str = Field(nullable=False)

    role: str = Field(nullable=False)  # EMPLOYEE | ADMIN

    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
