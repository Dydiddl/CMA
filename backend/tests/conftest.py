#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 공통 설정 파일
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db
from app.models.base import Base
from app.core.config import settings

# 테스트용 데이터베이스 URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# 테스트용 엔진 생성
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 테스트용 세션 팩토리
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """이벤트 루프 픽스처"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db():
    """테스트 데이터베이스 설정"""
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    yield
    # 테이블 삭제
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db) -> Generator[Session, None, None]:
    """데이터베이스 세션 픽스처"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """테스트 클라이언트 픽스처"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_contract_data():
    """샘플 계약 데이터 픽스처"""
    return {
        "name": "테스트 계약",
        "contract_number": "CON-2024-001",
        "contract_amount": 1000000,
        "contract_date": "2024-01-15T00:00:00",
        "client_name": "테스트 발주처",
        "vendor_id": "test-vendor-id",
        "status": "진행중"
    }


@pytest.fixture
def sample_labor_data():
    """샘플 노무 데이터 픽스처"""
    return {
        "name": "테스트 노무",
        "position": "기술자",
        "hourly_rate": 25000,
        "contract_id": "test-contract-id"
    }


@pytest.fixture
def sample_financial_data():
    """샘플 재무 데이터 픽스처"""
    return {
        "transaction_type": "수입",
        "amount": 500000,
        "description": "테스트 거래",
        "contract_id": "test-contract-id"
    }


# 성능 테스트용 픽스처
@pytest.fixture
def large_dataset():
    """대용량 데이터셋 픽스처"""
    return [
        {
            "name": f"계약 {i}",
            "contract_number": f"CON-2024-{i:03d}",
            "contract_amount": 1000000 + (i * 100000),
            "contract_date": "2024-01-15T00:00:00",
            "client_name": f"발주처 {i}",
            "vendor_id": f"vendor-{i}",
            "status": "진행중"
        }
        for i in range(1, 101)  # 100개의 테스트 데이터
    ]


# ASCR 테스트용 픽스처
@pytest.fixture
def sample_pdf_data():
    """샘플 PDF 데이터 픽스처"""
    return {
        "file_path": "tests/fixtures/sample.pdf",
        "year": 2025,
        "expected_sections": ["공통부문", "토목부문", "건축부문"]
    }


# Excel 테스트용 픽스처
@pytest.fixture
def sample_excel_data():
    """샘플 Excel 데이터 픽스처"""
    return {
        "file_path": "tests/fixtures/sample.xlsx",
        "sheet_name": "Sheet1",
        "expected_columns": ["A", "B", "C"]
    } 