import time
import pytest
from typing import Dict, List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.core.config import settings
from app.tests.utils.api_doc import create_random_api_doc
from app.tests.utils.user import create_random_user
from app.main import app
from app.tests.utils.utils import get_superuser_token_headers

client = TestClient(app)

def test_api_doc_list_performance(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 목록 조회 성능 테스트"""
    # 테스트 데이터 생성
    for _ in range(100):
        create_random_api_doc(db)
    
    # 전체 목록 조회 성능 테스트
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 1.0  # 1초 이내 응답
    
    # 필터링된 목록 조회 성능 테스트
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/api-docs?category=USER&status=ACTIVE",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 0.5  # 0.5초 이내 응답

def test_api_doc_search_performance(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 검색 성능 테스트"""
    # 테스트 데이터 생성
    for _ in range(100):
        create_random_api_doc(db)
    
    # 검색어 목록
    search_terms = ["user", "auth", "api", "test", "document"]
    
    # 각 검색어에 대한 성능 테스트
    for term in search_terms:
        start_time = time.time()
        response = client.get(
            f"{settings.API_V1_STR}/api-docs?search={term}",
            headers=superuser_token_headers,
        )
        end_time = time.time()
        assert response.status_code == 200
        assert end_time - start_time < 0.5  # 0.5초 이내 응답

def test_api_doc_version_performance(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 버전 관리 성능 테스트"""
    api_doc = create_random_api_doc(db)
    
    # 버전 생성 성능 테스트
    start_time = time.time()
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/versions",
        headers=superuser_token_headers,
        json={
            "version": "1.1.0",
            "content": "# Updated API Documentation",
            "changes": "Updated content"
        }
    )
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 0.5  # 0.5초 이내 응답
    
    # 버전 목록 조회 성능 테스트
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/versions",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 0.5  # 0.5초 이내 응답

def test_api_doc_comments_performance(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 댓글 관리 성능 테스트"""
    api_doc = create_random_api_doc(db)
    
    # 댓글 생성 성능 테스트
    start_time = time.time()
    response = client.post(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/comments",
        headers=superuser_token_headers,
        json={
            "content": "Test comment",
            "parent_id": None
        }
    )
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 0.5  # 0.5초 이내 응답
    
    # 댓글 목록 조회 성능 테스트
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}/comments",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 0.5  # 0.5초 이내 응답

def test_api_doc_concurrent_operations(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 동시 작업 성능 테스트"""
    api_doc = create_random_api_doc(db)
    
    def read_doc():
        response = client.get(
            f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
            headers=superuser_token_headers,
        )
        return response.status_code == 200
    
    def update_doc():
        response = client.put(
            f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
            headers=superuser_token_headers,
            json={
                "title": "Updated Title",
                "description": "Updated Description"
            }
        )
        return response.status_code == 200
    
    def add_comment():
        response = client.post(
            f"{settings.API_V1_STR}/api-docs/{api_doc.id}/comments",
            headers=superuser_token_headers,
            json={
                "content": "Concurrent comment",
                "parent_id": None
            }
        )
        return response.status_code == 200
    
    # 동시 작업 실행
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for _ in range(3):
            futures.append(executor.submit(read_doc))
            futures.append(executor.submit(update_doc))
            futures.append(executor.submit(add_comment))
        
        success_count = sum(1 for future in as_completed(futures) if future.result())
    
    end_time = time.time()
    assert end_time - start_time < 3.0  # 3초 이내 완료
    assert success_count >= 7  # 9개 작업 중 최소 7개 성공

def test_api_doc_statistics_performance(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 통계 조회 성능 테스트"""
    # 테스트 데이터 생성
    for _ in range(100):
        create_random_api_doc(db)
    
    # 통계 조회 성능 테스트
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/api-docs/statistics",
        headers=superuser_token_headers,
    )
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 1.0  # 1초 이내 응답 