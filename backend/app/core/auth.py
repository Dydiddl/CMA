#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인증 관련 유틸리티 및 의존성 함수
"""
from app.models.user import User

def get_current_user() -> User:
    """현재 사용자 반환 (임시 구현)"""
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
