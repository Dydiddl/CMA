#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI 의존성 주입 함수 (DB 세션, 사용자 등)
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.exceptions import AuthenticationException

# 데이터베이스 세션 의존성
from app.db.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """DB 세션 제공 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 사용자 인증 의존성 (예시)
from app.models.user import User

def get_current_user() -> User:
    """현재 사용자 반환 (임시 구현)"""
    # 실제 구현에서는 토큰/세션에서 사용자 조회
    # 여기서는 더미 사용자 반환
    user = User(
        email="admin@example.com",
        password_hash="dummyhash",
        full_name="관리자",
        role="admin",
        department="IT",
        phone="010-0000-0000",
        is_active=True
    )
    return user 