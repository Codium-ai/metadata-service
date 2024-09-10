"""
This module contains the repository layer (database operations) for the Tags entity.
"""

from sqlalchemy.orm import Session
from app.api.v1.tags.model import Tag
from app.common.base_entity.repository import BaseRepository


class TagRepository(BaseRepository[Tag]):
    """
    Provides methods to perform CRUD operations
    """

    def __init__(self, db: Session):
        super().__init__(db, Tag)
