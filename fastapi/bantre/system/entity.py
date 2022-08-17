from datetime import datetime
from email.policy import default
from typing import TYPE_CHECKING, List, Optional

from black import main
from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from .section import Section
    from .user import User


class EntitySectionLink(SQLModel, table=True):
    entity_id: Optional[int] = Field(
        default=None, foreign_key="entity.id", primary_key=True
    )
    section_id: Optional[int] = Field(
        default=None, foreign_key="section.id", primary_key=True
    )


class EntityBase(SQLModel):
    pass


class Entity(EntityBase, table=True):
    """This is an actual database table because it has table=True"""

    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(sa_column_kwargs={"server_default": func.now()})
    touched: Optional[datetime] = Field(
        sa_column_kwargs={"server_default": func.now(), "server_onupdate": func.now()}
    )
    views: Optional[int] = 0
    section_id: Optional[int] = Field(foreign_key="section.id")
    main_section: "Section" = Relationship()
    sections: List["Section"] = Relationship(
        back_populates="entities", link_model=EntitySectionLink
    )
    creator_id: Optional[int] = Field(foreign_key="user.id")
    creator: Optional["User"] = Relationship()
    type: str
    __mapper_args__ = {"polymorphic_identity": "article", "polymorphic_on": "type"}
