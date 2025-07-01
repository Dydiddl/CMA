"""
pytest 설정 파일
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.api.deps import get_db
from app.main import app

# 테스트용 데이터베이스 URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/construction_management"

# 테스트용 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 테스트용 세션 생성
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """
    테스트용 데이터베이스 세션 픽스처
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """
    테스트용 FastAPI 클라이언트 픽스처
    """
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def get_test_db():
    """
    테스트용 DB 세션을 반환하는 함수 (테스트에서 import용)
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close() 