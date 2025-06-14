import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_password_hash,
    verify_password
)
from app.models.user import User
from app.core.config import settings

def test_create_access_token():
    """액세스 토큰 생성 테스트"""
    # 토큰 생성
    token = create_access_token("test@example.com")
    assert token is not None
    
    # 토큰 검증
    payload = verify_token(token)
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload

def test_create_refresh_token():
    """리프레시 토큰 생성 테스트"""
    # 토큰 생성
    token = create_refresh_token("test@example.com")
    assert token is not None
    
    # 토큰 검증
    payload = verify_token(token)
    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "refresh"
    assert "exp" in payload

def test_token_expiration():
    """토큰 만료 테스트"""
    # 만료된 토큰 생성
    expired_token = create_access_token(
        "test@example.com",
        expires_delta=timedelta(microseconds=1)
    )
    
    # 토큰 만료 대기
    import time
    time.sleep(0.1)
    
    # 만료된 토큰 검증 시도
    with pytest.raises(HTTPException) as exc_info:
        verify_token(expired_token)
    assert exc_info.value.status_code == 401
    assert "토큰이 만료되었습니다" in str(exc_info.value.detail)

def test_invalid_token():
    """잘못된 토큰 테스트"""
    # 잘못된 토큰으로 검증 시도
    with pytest.raises(HTTPException) as exc_info:
        verify_token("invalid_token")
    assert exc_info.value.status_code == 401
    assert "유효하지 않은 토큰입니다" in str(exc_info.value.detail)

def test_password_hashing():
    """비밀번호 해싱 테스트"""
    # 비밀번호 해싱
    password = "TestPassword123!"
    hashed_password = get_password_hash(password)
    
    # 해시된 비밀번호 검증
    assert verify_password(password, hashed_password)
    assert not verify_password("WrongPassword123!", hashed_password)

def test_user_authentication(db_session: Session):
    """사용자 인증 테스트"""
    # 테스트 사용자 생성
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("TestPassword123!"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    
    # 액세스 토큰 생성
    access_token = create_access_token(user.email)
    assert access_token is not None
    
    # 리프레시 토큰 생성
    refresh_token = create_refresh_token(user.email)
    assert refresh_token is not None
    
    # 토큰 검증
    access_payload = verify_token(access_token)
    assert access_payload["sub"] == user.email
    
    refresh_payload = verify_token(refresh_token)
    assert refresh_payload["sub"] == user.email
    assert refresh_payload["type"] == "refresh"

def test_inactive_user_authentication(db_session: Session):
    """비활성화된 사용자 인증 테스트"""
    # 비활성화된 사용자 생성
    user = User(
        email="inactive@example.com",
        username="inactive",
        hashed_password=get_password_hash("TestPassword123!"),
        is_active=False
    )
    db_session.add(user)
    db_session.commit()
    
    # 토큰 생성 시도
    with pytest.raises(HTTPException) as exc_info:
        create_access_token(user.email)
    assert exc_info.value.status_code == 400
    assert "비활성화된 사용자입니다" in str(exc_info.value.detail) 