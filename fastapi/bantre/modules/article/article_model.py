from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from bantre.system.entity import Entity


class Article(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(foreign_key="entity.id", primary_key=True, default=None)
    entity: Entity = Relationship()
    title: str
    text: str
    text_source: str
    image: Optional[int]
    __mapper_args__ = {"polymorphic_identity": "article"}

    def __repr__(self):
        return f"Article(title={self.title}, text={self.text}, text_source={self.text_source}, image={self.image})"
