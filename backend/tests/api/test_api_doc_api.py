import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.tests.utils.utils import get_superuser_token_headers
from app.tests.utils.api_doc import create_random_api_doc
from app.tests.utils.user import create_random_user

client = TestClient(app)

def test_create_api_doc(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 생성 테스트"""
    data = {
        "title": "사용자 관리 API",
        "description": "사용자 관리 관련 API 문서",
        "content": "# 사용자 관리 API\n\n## 개요\n사용자 관리 API는...",
        "category": "USER",
        "tags": ["user", "auth"]
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["content"] == data["content"]
    assert content["category"] == data["category"]
    assert content["tags"] == data["tags"]
    assert content["status"] == "DRAFT"
    assert "id" in content

def test_read_api_doc(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 조회 테스트"""
    api_doc = create_random_api_doc(db)
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == api_doc.id
    assert content["title"] == api_doc.title
    assert content["description"] == api_doc.description

def test_read_api_docs(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 목록 조회 테스트"""
    api_doc = create_random_api_doc(db)
    response = client.get(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["items"]) > 0
    assert content["items"][0]["id"] == api_doc.id

def test_update_api_doc(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 수정 테스트"""
    api_doc = create_random_api_doc(db)
    data = {
        "title": "사용자 관리 API v2",
        "description": "사용자 관리 관련 API 문서 (업데이트)",
        "content": "# 사용자 관리 API v2\n\n## 개요\n사용자 관리 API는...",
        "category": "USER",
        "tags": ["user", "auth", "v2"]
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
    assert content["content"] == data["content"]
    assert content["tags"] == data["tags"]

def test_delete_api_doc(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 삭제 테스트"""
    api_doc = create_random_api_doc(db)
    response = client.delete(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "API 문서가 성공적으로 삭제되었습니다."

def test_create_api_doc_version(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 버전 생성 테스트"""
    api_doc = create_random_api_doc(db)
    data = {
        "version": "1.1.0",
        "content": "# 사용자 관리 API v1.1.0\n\n## 개요\n사용자 관리 API는...",
        "changes": "새로운 엔드포인트 추가 및 응답 형식 변경"
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/versions",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["version"] == data["version"]
    assert content["content"] == data["content"]
    assert content["changes"] == data["changes"]

def test_read_api_doc_versions(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 버전 목록 조회 테스트"""
    api_doc = create_random_api_doc(db)
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/versions",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "items" in content
    assert "total" in content

def test_add_api_doc_tags(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 태그 추가 테스트"""
    api_doc = create_random_api_doc(db)
    data = {
        "tags": ["new-feature", "deprecated"]
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/tags",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "new-feature" in content["tags"]
    assert "deprecated" in content["tags"]

def test_create_api_doc_comment(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 댓글 추가 테스트"""
    api_doc = create_random_api_doc(db)
    data = {
        "content": "API 응답 형식에 대한 설명이 필요합니다.",
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
    assert content["parent_id"] == data["parent_id"]

def test_read_api_doc_comments(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 댓글 목록 조회 테스트"""
    api_doc = create_random_api_doc(db)
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/comments",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "items" in content
    assert "total" in content

def test_get_api_doc_statistics(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 통계 조회 테스트"""
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
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 권한 테스트"""
    # 일반 사용자 토큰 생성
    user = create_random_user(db)
    user_token_headers = {"Authorization": f"Bearer {user.id}"}
    
    # 일반 사용자가 API 문서 생성 시도
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=user_token_headers,
        json={},
    )
    assert response.status_code == 403
    
    # 일반 사용자가 API 문서 수정 시도
    api_doc = create_random_api_doc(db)
    response = client.put(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=user_token_headers,
        json={},
    )
    assert response.status_code == 403 