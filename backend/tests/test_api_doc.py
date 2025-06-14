from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string
from app.tests.utils.api_doc import create_random_api_doc
from app.tests.utils.user import create_random_user

def test_create_api_doc(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 생성 API 테스트
    """
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "content": random_lower_string(),
        "version": "1.0.0",
        "status": "DRAFT",
        "category": "USER_API",
        "tags": ["user", "authentication"]
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["version"] == data["version"]
    assert content["status"] == data["status"]
    assert content["category"] == data["category"]
    assert "id" in content

def test_read_api_doc(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 조회 API 테스트
    """
    api_doc = create_random_api_doc(db)
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == api_doc.title
    assert content["id"] == api_doc.id

def test_read_api_docs(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 목록 조회 API 테스트
    """
    create_random_api_doc(db)
    create_random_api_doc(db)
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 2

def test_update_api_doc(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 수정 API 테스트
    """
    api_doc = create_random_api_doc(db)
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "status": "PUBLISHED"
    }
    response = client.put(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["status"] == data["status"]
    assert content["id"] == api_doc.id

def test_delete_api_doc(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 삭제 API 테스트
    """
    api_doc = create_random_api_doc(db)
    response = client.delete(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == "success"

def test_create_version(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 버전 생성 API 테스트
    """
    api_doc = create_random_api_doc(db)
    data = {
        "version": "1.1.0",
        "content": random_lower_string(),
        "changes": "API 엔드포인트 추가",
        "status": "DRAFT"
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/versions",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["version"] == data["version"]
    assert content["changes"] == data["changes"]
    assert content["status"] == data["status"]
    assert "id" in content

def test_create_tag(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 태그 생성 API 테스트
    """
    api_doc = create_random_api_doc(db)
    data = {
        "name": random_lower_string(),
        "description": random_lower_string()
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/tags",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content

def test_create_comment(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 댓글 생성 API 테스트
    """
    api_doc = create_random_api_doc(db)
    data = {
        "content": random_lower_string(),
        "parent_id": None
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/comments",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["content"] == data["content"]
    assert "id" in content

def test_get_statistics(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 통계 API 테스트
    """
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/statistics",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "total_docs" in content
    assert "docs_by_category" in content
    assert "docs_by_status" in content
    assert "recent_updates" in content

def test_api_doc_permissions(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    """
    API 문서 API 권한 테스트
    """
    api_doc = create_random_api_doc(db)
    
    # 조회 권한 테스트
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    
    # 수정 권한 테스트
    data = {"title": random_lower_string()}
    response = client.put(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 403
    
    # 삭제 권한 테스트
    response = client.delete(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403 