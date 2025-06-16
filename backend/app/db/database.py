from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

print(f"[DB 연결 정보] SQLALCHEMY_DATABASE_URI: {settings.SQLALCHEMY_DATABASE_URI}")

# PostgreSQL 데이터베이스 엔진 생성
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성 (모든 모델의 부모 클래스)
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    """
    데이터베이스 세션을 생성하고 반환하는 의존성 함수
    FastAPI의 Depends에서 사용됩니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 초기화 함수
def init_db():
    """
    데이터베이스 테이블을 생성합니다.
    애플리케이션 시작 시 호출됩니다.
    """
    # 모든 모델을 import해야 테이블이 생성됩니다
    from ..models import user, vendor, contract, labor_cost, transaction
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블이 생성되었습니다.") 