from fastapi.testclient import TestClient

from app.api.v1.tags.model import Tag
from app.common.base_entity.model import AdvancedSearchRequest, FilterType, Filter
from app.main import app
from app.api.v1.entity_tags.model import (
    ResetEntityTagsByNameRequest,
    TagGroupTagsByNameRequest,
)

import json
from pydantic.json import pydantic_encoder
client = TestClient(app)


def test_create_tags_and_search_entities():

    tag_group_1 = TagGroupTagsByNameRequest(
        tag_group_name="language", tag_names=["java", "python"]
    )
    tag_group_2 = TagGroupTagsByNameRequest(
        tag_group_name="bu", tag_names=["bu-1", "bu-2"]
    )
    tag_group_3 = TagGroupTagsByNameRequest(
        tag_group_name="capability", tag_names=["cap1", "cap2"]
    )
    repo_1 = ResetEntityTagsByNameRequest(
        entity_id="/codium/repo1", entity_type="repo", tag_groups=[tag_group_1, tag_group_2]
    )

    repo_2 = ResetEntityTagsByNameRequest(
        entity_id="/codium/repo2", entity_type="repo", tag_groups=[tag_group_2, tag_group_3]
    )

    response = client.post("/api/v1/entity_tags/reset", content=json.dumps([repo_1, repo_2], default=pydantic_encoder), headers={"content-type": "application/json"})

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list), "Response should be a list"
    for item in response_data:
        assert "errors" in item, "expected errors array"
        assert item["errors"] == [], "expected no errors"

    # 2. search for tags (end user from ide)
    # search_request = AdvancedSearchRequest(
    #    filters= [
    #        Filter(filter_type=FilterType.EQUALS, field="tag_group_name", values=["language"]),
    #    ]
    #  )
    #
    # search_response = client.post("/api/v1/tags/advanced_search", content=json.dumps(search_request, default=pydantic_encoder), headers={"content-type": "application/json"})
    #
    # assert search_response.status_code == 200
    #
    # search_response_data = search_response.json()
    # assert search_response_data.count == 2
    # assert {"name": "java"} in search_response_data.results
    # assert {"name": "python"} in search_response_data.results



    # 3. ragger searches all entities with tags: /entity_tags/advanced_search
