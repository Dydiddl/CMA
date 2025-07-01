from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from ..core.config import settings
import time
import logging

logger = logging.getLogger(__name__)

# PostgreSQL 데이터베이스 엔진 생성 (성능 최적화 설정 포함)
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,  # 기본 커넥션 풀 크기
    max_overflow=10,  # 추가로 생성 가능한 커넥션 수
    pool_timeout=30,  # 커넥션 대기 시간
    pool_recycle=1800,  # 커넥션 재사용 시간 (30분)
    echo_pool=True,  # 풀 디버깅
    execution_options={
        "isolation_level": "READ COMMITTED"  # 격리 수준 설정
    }
)

# 데이터베이스 성능 모니터링을 위한 이벤트 리스너
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    logger.debug("Query: %s", statement)

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    logger.debug("Query Complete! Total Time: %f", total)
    if total > 0.5:  # 500ms 이상 걸리는 쿼리 로깅
        logger.warning("Slow Query Detected: %s", statement)

# 세션 팩토리 생성 (성능 최적화 설정 포함)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # 세션 종료 후 객체 만료 방지
)

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
    데이터베이스 테이블을 생성하고 초기 설정을 수행합니다.
    애플리케이션 시작 시 호출됩니다.
    """
    # 모든 모델을 import해야 테이블이 생성됩니다
    from ..models import user, vendor, contract, labor_cost, transaction
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 성능 최적화를 위한 인덱스 생성
    with engine.connect() as conn:
        # 자주 조회되는 컬럼에 대한 인덱스 생성
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);
            CREATE INDEX IF NOT EXISTS idx_contract_status ON contracts(status);
            CREATE INDEX IF NOT EXISTS idx_transaction_date ON transactions(transaction_date);
            CREATE INDEX IF NOT EXISTS idx_labor_cost_date ON labor_costs(work_date);
        """)
    
    print("✅ 데이터베이스 테이블과 인덱스가 생성되었습니다.") 