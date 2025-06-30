#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데이터베이스 설정
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from typing import Generator

# 데이터베이스 URL 설정
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5432/cma_db"
)

# 엔진 설정 (성능 최적화)
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,  # 연결 풀 크기
    max_overflow=30,  # 최대 오버플로우
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=3600,  # 1시간마다 연결 재생성
    echo=False  # SQL 로그 비활성화 (성능 향상)
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 베이스 모델
Base = declarative_base()

def get_db() -> Generator:
    """데이터베이스 세션 생성기"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """테이블 생성"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """테이블 삭제"""
    Base.metadata.drop_all(bind=engine) 