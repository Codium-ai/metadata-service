"""
This module contains the repository layer (database operations)
for the TagGroups entity.
"""

from sqlalchemy import asc, desc, and_, or_
from sqlalchemy.orm import Session

from app.api.v1.tag_groups.model import (
    TagGroup,
    # TagGroupAdvancedSearchResponse,
    TagGroupResponse,
)
from app.common.base_entity.model import (
    FilterType,
    SortType,
    AdvancedSearchResponse,
    AdvancedSearchRequest,
    LogicOperator,
)


class TagGroupRepository:
    """
    Provides methods to perform CRUD operations
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, tag_group: TagGroup) -> TagGroup:
        self.db.add(tag_group)
        self.db.commit()
        self.db.refresh(tag_group)
        return tag_group

    def get(self, tag_group_id: int) -> TagGroup:
        return self.db.query(TagGroup).filter(TagGroup.id == tag_group_id).first()

    def search(
        self,
        field: str,
        value: str,
        filter_type: str = FilterType.CONTAINS,
        is_case_sensitive: bool = False,
    ) -> list[TagGroup]:

        if value is not None and not is_case_sensitive:
            value = value.lower()

        if field is None:
            return self.db.query(TagGroup).all()

        if not hasattr(TagGroup, field):
            raise ValueError(f"Invalid field: {field}")

        column = getattr(TagGroup, field)

        if filter_type == FilterType.EQUALS:
            return self.db.query(TagGroup).filter(column == value).all()
        elif filter_type == FilterType.STARTS_WITH:
            return self.db.query(TagGroup).filter(column.like(f"{value}%")).all()
        elif filter_type == FilterType.CONTAINS:
            return self.db.query(TagGroup).filter(column.like(f"%{value}%")).all()
        else:
            raise ValueError(
                "Invalid search_type. Use 'exact', 'starts-with', or 'contains'."
            )

        # TODO: make error message generic, extract validator to common?
        #  - in global error handler when it wil work

    def search_advanced(
        self, search_req: AdvancedSearchRequest
    ) -> AdvancedSearchResponse[TagGroupResponse]:
        query = self.db.query(TagGroup)

        filter_clauses = []
        for filter in search_req.filters:
            column = getattr(TagGroup, filter.field)
            if filter.filter_type == FilterType.EQUALS:
                filter_clauses.append(column == filter.values[0])
            elif filter.filter_type == FilterType.STARTS_WITH:
                filter_clauses.append(column.like(f"{filter.values[0]}%"))
            elif filter.filter_type == FilterType.CONTAINS:
                filter_clauses.append(column.like(f"%{filter.values[0]}%"))

        if search_req.filters_operator == LogicOperator.AND:
            query = query.filter(and_(*filter_clauses))
        else:
            query = query.filter(or_(*filter_clauses))

        for sort in search_req.sorts:
            column = getattr(TagGroup, sort.field)
            if sort.sort_type == SortType.ASC:
                query = query.order_by(asc(column))
            else:
                query = query.order_by(desc(column))

        total_count = query.count()
        results = query.offset(search_req.offset).limit(search_req.limit).all()

        return AdvancedSearchResponse[TagGroupResponse](
            results=[TagGroupResponse.from_tag_group(res) for res in results],
            count=len(results),
            offset=search_req.offset,
            count_total=total_count,
        )

    def delete(self, tag_group):
        self.db.delete(tag_group)
        self.db.commit()
        return tag_group
