"""
This module contains the controller (endpoints) for the Tags entity.
It handles all API/HTTP related issues.
It uses the service layer to perform the business logic.
"""

import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.tag_groups.controller import get_tag_group_service
from app.api.v1.tags.model import TagResponse, TagCreateRequest, Tag
from app.api.v1.tags.repository import TagRepository
from app.api.v1.tags.service import TagService
from app.common.base_entity.model import (
    AdvancedSearchResponse,
    AdvancedSearchRequest,
    DeleteResponse,
)
from app.common.database import get_db
from app.common.utils.logging_utils import setup_logger, LoggingFormat

logger = setup_logger(level="DEBUG", fmt=LoggingFormat.CONSOLE)

router = APIRouter()


# Dependency function to provide TagGroupService
def get_tag_service(db: Session = Depends(get_db)) -> TagService:
    repository = TagRepository(db)
    return TagService(repository)


def convert_advanced_search_response(
    response: AdvancedSearchResponse[Tag],
    tag_group_service=Depends(get_tag_group_service),
) -> AdvancedSearchResponse[TagResponse]:
    tag_responses = [
        TagResponse.from_tag(tag, tag_group_service) for tag in response.results
    ]
    return AdvancedSearchResponse[TagResponse](
        results=tag_responses,
        count=response.count,
        offset=response.offset,
        count_total=response.count_total,
    )


@router.post("/tags", response_model=TagResponse)
def create_tag(
    tag: TagCreateRequest,
    tag_service: TagService = Depends(get_tag_service),
    tag_group_service=Depends(get_tag_group_service),
):
    try:
        created = tag_service.create(tag)
        return TagResponse.from_tag(created, tag_group_service)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    # todo: remove error handling when global error is working


@router.get("/tags/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service),
    tag_group_service=Depends(get_tag_group_service),
):

    tag = tag_service.get(tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return TagResponse.from_tag(tag, tag_group_service)


@router.put("/tags/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag: TagCreateRequest,
    tag_service: TagService = Depends(get_tag_service),
    tag_group_service=Depends(get_tag_group_service),
):
    try:
        updated_tag = tag_service.update(tag_id, tag)
        return TagResponse.from_tag(updated_tag, tag_group_service)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    # todo: remove error handling when global error is working


@router.delete("/tags/{tag_id}", response_model=DeleteResponse)
def delete_tag(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service),
):
    deleted_count = tag_service.delete(tag_id)

    if deleted_count is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return DeleteResponse(count=deleted_count)


@router.post(
    "/tags/advanced_search",
    response_model=AdvancedSearchResponse[TagResponse],
)
def advanced_search(
    search_req: AdvancedSearchRequest,
    service: TagService = Depends(get_tag_service),
    tag_group_service=Depends(get_tag_group_service),
) -> AdvancedSearchResponse[TagResponse]:
    logger.info(f"advanced_search running")
    logger.debug(f"advanced_search running")
    logger.warning(f"advanced_search running")
    try:

        advanced_search_response = service.advanced_search(search_req)
        return convert_advanced_search_response(
            advanced_search_response, tag_group_service
        )
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e)) from e