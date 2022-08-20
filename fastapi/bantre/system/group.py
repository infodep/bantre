from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .user import UserGroupLink


if TYPE_CHECKING:
    # This means that type-hints we add in quotes get autofill, its great
    from .section import Section
    from .user import User


class GroupSectionLink(SQLModel, table=True):  # type: ignore
    group_id: Optional[int] = Field(
        default=None, foreign_key="group.id", primary_key=True
    )
    group: "Group" = Relationship(back_populates="sections_permissions")
    section_id: Optional[int] = Field(
        default=None, foreign_key="section.id", primary_key=True
    )
    section: "Section" = Relationship(back_populates="groups_permissions")
    read: Optional[bool] = Field(default=False, index=True)
    write: Optional[bool] = Field(default=False)
    admin: Optional[bool] = Field(default=False)


class GroupBase(SQLModel):
    name: str
    type: int
    description: str


class Group(GroupBase, table=True):  # type: ignore
    """This is an actual database table because it has table=True"""

    id: Optional[int] = Field(default=None, primary_key=True)
    members: List["User"] = Relationship(
        back_populates="groups", link_model=UserGroupLink
    )
    sections_permissions: List["GroupSectionLink"] = Relationship(
        back_populates="group"
    )
