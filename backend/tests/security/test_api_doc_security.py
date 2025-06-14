import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.tests.utils.utils import get_superuser_token_headers
from app.tests.utils.api_doc import create_random_api_doc
from app.tests.utils.user import create_random_user

client = TestClient(app)

def test_api_doc_authentication(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 인증 테스트"""
    # 1. 인증 없이 API 문서 생성 시도
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        json={
            "title": "인증 테스트",
            "description": "인증 테스트를 위한 문서",
            "content": "# 인증 테스트",
            "category": "TEST",
            "tags": ["test", "security"]
        }
    )
    assert response.status_code == 401
    
    # 2. 잘못된 토큰으로 API 문서 조회 시도
    response = client.get(
        f"{settings.API_V1_STR}/api-docs",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    
    # 3. 만료된 토큰으로 API 문서 수정 시도
    response = client.put(
        f"{settings.API_V1_STR}/api-docs/1",
        headers={"Authorization": "Bearer expired_token"},
        json={"title": "수정된 제목"}
    )
    assert response.status_code == 401

def test_api_doc_authorization(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 권한 테스트"""
    # 1. 일반 사용자 생성
    user = create_random_user(db)
    user_token_headers = {"Authorization": f"Bearer {user.id}"}
    
    # 2. 일반 사용자가 API 문서 생성 시도
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=user_token_headers,
        json={
            "title": "권한 테스트",
            "description": "권한 테스트를 위한 문서",
            "content": "# 권한 테스트",
            "category": "TEST",
            "tags": ["test", "security"]
        }
    )
    assert response.status_code == 403
    
    # 3. 일반 사용자가 API 문서 수정 시도
    api_doc = create_random_api_doc(db)
    response = client.put(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=user_token_headers,
        json={"title": "수정된 제목"}
    )
    assert response.status_code == 403
    
    # 4. 일반 사용자가 API 문서 삭제 시도
    response = client.delete(
        f"{settings.API_V1_STR}/api-docs/{api_doc.id}",
        headers=user_token_headers
    )
    assert response.status_code == 403

def test_api_doc_input_validation(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 입력값 검증 테스트"""
    # 1. 필수 필드 누락
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
        json={
            "description": "입력값 검증 테스트",
            "content": "# 입력값 검증 테스트",
            "category": "TEST"
        }
    )
    assert response.status_code == 422
    
    # 2. 잘못된 카테고리 값
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
        json={
            "title": "입력값 검증 테스트",
            "description": "입력값 검증 테스트",
            "content": "# 입력값 검증 테스트",
            "category": "INVALID_CATEGORY",
            "tags": ["test"]
        }
    )
    assert response.status_code == 422
    
    # 3. 잘못된 태그 형식
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
        json={
            "title": "입력값 검증 테스트",
            "description": "입력값 검증 테스트",
            "content": "# 입력값 검증 테스트",
            "category": "TEST",
            "tags": ["invalid tag with space"]
        }
    )
    assert response.status_code == 422

def test_api_doc_sql_injection(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 SQL 인젝션 방지 테스트"""
    # 1. SQL 인젝션 시도 (제목)
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
        json={
            "title": "'; DROP TABLE api_docs; --",
            "description": "SQL 인젝션 테스트",
            "content": "# SQL 인젝션 테스트",
            "category": "TEST",
            "tags": ["test", "security"]
        }
    )
    assert response.status_code == 422
    
    # 2. SQL 인젝션 시도 (검색어)
    response = client.get(
        f"{settings.API_V1_STR}/api-docs?search='; DROP TABLE api_docs; --",
        headers=superuser_token_headers
    )
    assert response.status_code == 422

def test_api_doc_xss_prevention(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 XSS 방지 테스트"""
    # 1. XSS 시도 (제목)
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
        json={
            "title": "<script>alert('XSS')</script>",
            "description": "XSS 테스트",
            "content": "# XSS 테스트",
            "category": "TEST",
            "tags": ["test", "security"]
        }
    )
    assert response.status_code == 422
    
    # 2. XSS 시도 (내용)
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers=superuser_token_headers,
        json={
            "title": "XSS 테스트",
            "description": "XSS 테스트",
            "content": "<script>alert('XSS')</script>",
            "category": "TEST",
            "tags": ["test", "security"]
        }
    )
    assert response.status_code == 422

def test_api_doc_rate_limiting(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 요청 제한 테스트"""
    # 1. 빠른 연속 요청
    for _ in range(100):
        response = client.get(
            f"{settings.API_V1_STR}/api-docs",
            headers=superuser_token_headers
        )
        if response.status_code == 429:  # Too Many Requests
            break
    assert response.status_code == 429
    
    # 2. 빠른 연속 생성 요청
    for _ in range(50):
        response = client.post(
            f"{settings.API_V1_STR}/api-docs",
            headers=superuser_token_headers,
            json={
                "title": "Rate Limit 테스트",
                "description": "Rate Limit 테스트",
                "content": "# Rate Limit 테스트",
                "category": "TEST",
                "tags": ["test", "security"]
            }
        )
        if response.status_code == 429:  # Too Many Requests
            break
    assert response.status_code == 429

def test_api_doc_csrf_protection(
    db: Session, superuser_token_headers: dict
) -> None:
    """API 문서 CSRF 방지 테스트"""
    # 1. CSRF 토큰 없이 POST 요청
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers={
            "Authorization": superuser_token_headers["Authorization"],
            "Content-Type": "application/json"
        },
        json={
            "title": "CSRF 테스트",
            "description": "CSRF 테스트",
            "content": "# CSRF 테스트",
            "category": "TEST",
            "tags": ["test", "security"]
        }
    )
    assert response.status_code == 403
    
    # 2. 잘못된 CSRF 토큰으로 POST 요청
    response = client.post(
        f"{settings.API_V1_STR}/api-docs",
        headers={
            "Authorization": superuser_token_headers["Authorization"],
            "Content-Type": "application/json",
            "X-CSRF-Token": "invalid_token"
        },
        json={
            "title": "CSRF 테스트",
            "description": "CSRF 테스트",
            "content": "# CSRF 테스트",
            "category": "TEST",
            "tags": ["test", "security"]
        }
    )
    assert response.status_code == 403 