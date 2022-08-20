from typing import Optional

from sqlmodel import Field, SQLModel


class RefreshTokenModel(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
