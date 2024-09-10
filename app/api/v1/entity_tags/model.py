"""
This module contains the ORM model and DTO models related to the EntityTag entity
"""

from http.client import HTTPException
from typing import Optional, TypeVar, Generic, List

from pydantic import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    PrimaryKeyConstraint,
    DateTime,
    func,
)

from app.api.v1.tag_groups.service import TagGroupService
from app.api.v1.tags.model import TagResponse, Tag
from app.api.v1.tags.service import TagService
from app.common.database import Base


class EntityTag(Base):
    """Describes the structure of the EntityTag entity in the database"""

    __tablename__ = "entity_tags"

    entity_id = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="RESTRICT"), nullable=False)
    # create_date = Column(DateTime, nullable=False, default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint("entity_id", "tag_id", name="pk_entity_tags"),
    )


class EntityTagCreateRequest(BaseModel):
    entity_id: str
    entity_type: str
    tag_id: int


class EntityTagDeleteRequest(BaseModel):
    entity_id: str
    tag_id: Optional[int] = None


class TagGroupTagsByNameRequest(BaseModel):
    tag_group_name: str
    tag_names: list[str]


class ResetEntityTagsByNameRequest(BaseModel):
    entity_id: str
    entity_type: str
    tag_groups: list[TagGroupTagsByNameRequest]


class ResetEntityTagsByNameResponse(BaseModel):
    entity_id: str
    entity_type: str
    tags: list[TagResponse]
    errors: list[str] = []


# ceating this class makes pydantic schema generation fail- why??? Because Tag is a sqlalchemy type, and pydantic cant generate type for it
# class ResetEntityTagsByNameResult(BaseModel):
#     tags: list[Tag]
#     errors: list[str] = []


class EntityTagResponse(BaseModel):
    """Structure of the EntityTag entity to be returned in the API response (DTO)"""

    entity_id: str
    entity_type: str
    tag_id: int
    tag: TagResponse
    # create_date: DateTime

    @classmethod
    def from_entity_tag(
        cls,
        entity_tag: EntityTag,
        tag_service: TagService,
        tag_group_service: TagGroupService,
    ):
        tag = tag_service.get(entity_tag.tag_id)

        return cls(
            entity_id=entity_tag.entity_id,
            entity_type=entity_tag.entity_type,
            tag_id=entity_tag.tag_id,
            tag=TagResponse.from_tag(tag, tag_group_service),
            # create_date=entity_tag.create_date,
        )


# Define a generic type variable
# T = TypeVar("T")
#
#
# class BulkOperationResult(BaseModel, Generic[T]):
#     results: List[T]
#     errors: List[str]
