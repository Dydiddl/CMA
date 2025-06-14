from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
from typing import Generator
from .config import settings

# 로거 설정
logger = logging.getLogger(__name__)

# 데이터베이스 URL 설정
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 엔진 설정 최적화
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=30,  # 연결 타임아웃 (초)
    pool_recycle=1800,  # 연결 재사용 시간 (30분)
    pool_pre_ping=True,  # 연결 유효성 검사
    echo=settings.DEBUG,  # 디버그 모드에서만 SQL 로깅
)

# 세션 팩토리 설정
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # 성능 최적화
)

Base = declarative_base()

@contextmanager
def get_db() -> Generator:
    """
    데이터베이스 세션을 관리하는 컨텍스트 매니저
    자동으로 세션을 닫고 예외 처리를 수행합니다.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"데이터베이스 오류 발생: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"예상치 못한 오류 발생: {str(e)}")
        raise
    finally:
        db.close()

def init_db() -> None:
    """
    데이터베이스 초기화 함수
    모든 테이블을 생성합니다.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("데이터베이스 테이블이 성공적으로 생성되었습니다.")
    except SQLAlchemyError as e:
        logger.error(f"데이터베이스 초기화 중 오류 발생: {str(e)}")
        raise 