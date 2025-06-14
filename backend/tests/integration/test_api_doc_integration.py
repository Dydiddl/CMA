from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, get_superuser_token_headers
from app.tests.utils.api_doc import create_random_api_doc
from app.tests.utils.user import create_random_user
from app.main import app

client = TestClient(app)

def test_api_doc_lifecycle(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 전체 생명주기 테스트"""
    # 1. API 문서 생성
    create_data = {
        "title": "통합 테스트 API 문서",
        "description": "API 문서 통합 테스트를 위한 문서",
        "content": "# 통합 테스트\n\n## 개요\n이 문서는...",
        "category": "TEST",
        "tags": ["test", "integration"]
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
        json=create_data,
    )
    assert response.status_code == 200
    doc_data = response.json()
    doc_id = doc_data["id"]
    
    # 2. API 문서 조회
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{doc_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == create_data["title"]
    
    # 3. API 문서 버전 생성
    version_data = {
        "version": "1.1.0",
        "content": "# 통합 테스트 v1.1.0\n\n## 개요\n이 문서는...",
        "changes": "내용 업데이트"
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{doc_id}/versions",
        headers=superuser_token_headers,
        json=version_data,
    )
    assert response.status_code == 200
    version_id = response.json()["id"]
    
    # 4. API 문서 댓글 추가
    comment_data = {
        "content": "통합 테스트 댓글",
        "parent_id": None
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{doc_id}/comments",
        headers=superuser_token_headers,
        json=comment_data,
    )
    assert response.status_code == 200
    comment_id = response.json()["id"]
    
    # 5. API 문서 태그 추가
    tag_data = {
        "tags": ["integration-test", "api-doc"]
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{doc_id}/tags",
        headers=superuser_token_headers,
        json=tag_data,
    )
    assert response.status_code == 200
    assert "integration-test" in response.json()["tags"]
    
    # 6. API 문서 수정
    update_data = {
        "title": "통합 테스트 API 문서 (수정)",
        "description": "API 문서 통합 테스트를 위한 문서 (수정)",
        "content": "# 통합 테스트 (수정)\n\n## 개요\n이 문서는...",
        "category": "TEST",
        "tags": ["test", "integration", "updated"]
    }
    response = client.put(
        f"{settings.API_V1_STR}/api-docs/{doc_id}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    
    # 7. API 문서 삭제
    response = client.delete(
        f"{settings.API_V1_STR}/api-docs/{doc_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    
    # 8. 삭제된 문서 조회 시도
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{doc_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404

def test_api_doc_search_and_filter(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 검색 및 필터링 통합 테스트"""
    # 1. 테스트 데이터 생성
    docs = []
    for i in range(5):
        doc = create_random_api_doc(db)
        docs.append(doc)
    
    # 2. 카테고리별 필터링
    response = client.get(
        f"{settings.API_V1_STR}/api-docs?category={docs[0].category}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    filtered_docs = response.json()["items"]
    assert all(doc["category"] == docs[0].category for doc in filtered_docs)
    
    # 3. 태그별 필터링
    response = client.get(
        f"{settings.API_V1_STR}/api-docs?tags={docs[0].tags[0]}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    filtered_docs = response.json()["items"]
    assert any(docs[0].tags[0] in doc["tags"] for doc in filtered_docs)
    
    # 4. 검색어 검색
    search_term = docs[0].title.split()[0]
    response = client.get(
        f"{settings.API_V1_STR}/api-docs?search={search_term}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    search_results = response.json()["items"]
    assert any(search_term.lower() in doc["title"].lower() for doc in search_results)

def test_api_doc_version_management(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 버전 관리 통합 테스트"""
    # 1. API 문서 생성
    doc = create_random_api_doc(db)
    
    # 2. 여러 버전 생성
    versions = []
    for i in range(3):
        version_data = {
            "version": f"1.{i}.0",
            "content": f"# 버전 {i} 내용",
            "changes": f"버전 {i} 변경사항"
        }
        response = client.post(
            f"{settings.API_V1_STR}/api-docs/{doc.id}/versions",
            headers=superuser_token_headers,
            json=version_data,
        )
        assert response.status_code == 200
        versions.append(response.json())
    
    # 3. 버전 목록 조회
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{doc.id}/versions",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    version_list = response.json()["items"]
    assert len(version_list) == 3
    
    # 4. 버전 정렬 확인
    version_numbers = [v["version"] for v in version_list]
    assert version_numbers == sorted(version_numbers, reverse=True)

def test_api_doc_comment_thread(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 댓글 스레드 통합 테스트"""
    # 1. API 문서 생성
    doc = create_random_api_doc(db)
    
    # 2. 부모 댓글 생성
    parent_comment = {
        "content": "부모 댓글",
        "parent_id": None
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{doc.id}/comments",
        headers=superuser_token_headers,
        json=parent_comment,
    )
    assert response.status_code == 200
    parent_id = response.json()["id"]
    
    # 3. 자식 댓글 생성
    child_comment = {
        "content": "자식 댓글",
        "parent_id": parent_id
    }
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{doc.id}/comments",
        headers=superuser_token_headers,
        json=child_comment,
    )
    assert response.status_code == 200
    
    # 4. 댓글 목록 조회
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{doc.id}/comments",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    comments = response.json()["items"]
    assert len(comments) == 2
    assert any(c["parent_id"] == parent_id for c in comments)

def test_api_doc_statistics(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 통계 통합 테스트"""
    # 1. 테스트 데이터 생성
    for _ in range(10):
        doc = create_random_api_doc(db)
        # 각 문서에 댓글 추가
        for _ in range(2):
            client.post(
                f"{settings.API_V1_STR}/api-docs/{doc.id}/comments",
                headers=superuser_token_headers,
                json={"content": "테스트 댓글", "parent_id": None},
            )
    
    # 2. 통계 정보 조회
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/statistics",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    stats = response.json()
    
    # 3. 통계 데이터 검증
    assert stats["total_docs"] >= 10
    assert "docs_by_category" in stats
    assert "docs_by_status" in stats
    assert "recent_updates" in stats
    assert len(stats["recent_updates"]) > 0 