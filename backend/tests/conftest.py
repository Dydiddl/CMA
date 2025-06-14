import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.config import settings
from backend.app.models import User, Department

@pytest.fixture(scope="session")
def engine():
    return create_engine(settings.DATABASE_URL)

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(engine, tables):
    """테스트용 데이터베이스 세션을 생성합니다."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client():
    """테스트용 FastAPI 클라이언트를 생성합니다."""
    from fastapi.testclient import TestClient
    from ..main import app
    return TestClient(app) 