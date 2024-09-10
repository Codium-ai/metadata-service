"""
This module contains the controller (endpoints) for the EntityTags entity.
It handles all API/HTTP related issues.
It uses the service layer to perform the business logic.
"""

from idlelib.iomenu import errors
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.api.v1.entity_tags.repository import EntityTagRepository
from app.api.v1.entity_tags.service import EntityTagService
from app.api.v1.tag_groups.controller import get_tag_group_service
from app.api.v1.tag_groups.service import TagGroupService
from app.api.v1.tags.controller import get_tag_service
from app.api.v1.tags.model import TagResponse
from app.api.v1.tags.service import TagService
from app.common.base_entity.model import (
    AdvancedSearchRequest,
    AdvancedSearchResponse,
    DeleteResponse,
)
from app.common.database import get_db
from app.api.v1.entity_tags.model import (
    EntityTagResponse,
    EntityTagCreateRequest,
    EntityTag,
    EntityTagDeleteRequest,
    ResetEntityTagsByNameResponse,
    ResetEntityTagsByNameRequest,
)

from app.common.utils.logging_utils import get_logger

logger = get_logger()

router = APIRouter()


def get_entity_tag_service(db: Session = Depends(get_db)) -> EntityTagService:
    repository = EntityTagRepository(db)
    return EntityTagService(repository)


def convert_advanced_search_response(
    response: AdvancedSearchResponse[EntityTag],
    tag_service=Depends(get_tag_service),
    tag_group_service=Depends(get_tag_group_service),
) -> AdvancedSearchResponse[EntityTagResponse]:
    entity_tag_responses = [
        EntityTagResponse.from_entity_tag(entity_tag, tag_service, tag_group_service)
        for entity_tag in response.results
    ]
    return AdvancedSearchResponse[EntityTagResponse](
        results=entity_tag_responses,
        count=response.count,
        offset=response.offset,
        count_total=response.count_total,
    )


@router.post("/entity_tags", response_model=EntityTagResponse)
def create_entity_tag(
    create_request: EntityTagCreateRequest,
    tag_service: TagService = Depends(get_tag_service),
    tag_group_service: TagGroupService = Depends(get_tag_group_service),
    entity_tag_service: EntityTagService = Depends(get_entity_tag_service),
):
    try:
        created: EntityTag = entity_tag_service.create(create_request)
        return EntityTagResponse.from_entity_tag(
            created, tag_service, tag_group_service
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    # todo: remove error handling when global error is working


@router.post(
    "/entity_tags/advanced_search",
    response_model=AdvancedSearchResponse[EntityTagResponse],
)
def advanced_search(
    search_request: AdvancedSearchRequest,
    tag_service: TagService = Depends(get_tag_service),
    tag_group_service: TagGroupService = Depends(get_tag_group_service),
    entity_tag_service: EntityTagService = Depends(get_entity_tag_service),
):
    try:
        advanced_search_response = entity_tag_service.advanced_search(search_request)
        converted = convert_advanced_search_response(
            advanced_search_response, tag_service, tag_group_service
        )
        return converted
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/entity_tags/", response_model=DeleteResponse)
def delete(
    delete_request: EntityTagDeleteRequest,
    entity_tag_service: EntityTagService = Depends(get_entity_tag_service),
):
    try:
        deleted_count = entity_tag_service.delete(delete_request)

        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="No Tags found for entity")

        return DeleteResponse(count=deleted_count)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/entity_tags/reset", response_model=List[ResetEntityTagsByNameResponse])
def reset(
    reset_requests: list[ResetEntityTagsByNameRequest],
    entity_tag_service: EntityTagService = Depends(get_entity_tag_service),
    tag_service: TagService = Depends(get_tag_service),
    tag_group_service: TagGroupService = Depends(get_tag_group_service),
):
    results = []
    for reset_request in reset_requests:
        try:

            reset_entity_response = entity_tag_service.reset_entity_tags_by_name(
                reset_request, tag_service, tag_group_service
            )

            results.append(reset_entity_response)

        except Exception as e:
            logger.debug(
                f"Error resetting tags by name for entity {reset_request.entity_id} - {e}"
            )

    return results
