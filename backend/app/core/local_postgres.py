from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from pathlib import Path
import time

# 로컬 PostgreSQL 설정
LOCAL_POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "database": "construction_management"
}

# 데이터베이스 URL 생성
SQLALCHEMY_DATABASE_URL = f"postgresql://{LOCAL_POSTGRES_CONFIG['user']}:{LOCAL_POSTGRES_CONFIG['password']}@{LOCAL_POSTGRES_CONFIG['host']}:{LOCAL_POSTGRES_CONFIG['port']}/{LOCAL_POSTGRES_CONFIG['database']}"

# 데이터베이스 엔진 설정
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 초기화
def init_db():
    Base.metadata.create_all(bind=engine)
    print("로컬 PostgreSQL 데이터베이스 초기화 완료")

# 데이터베이스 백업
def backup_database():
    backup_dir = Path("data/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # pg_dump 명령어 실행
    backup_file = backup_dir / f"backup_{int(time.time())}.sql"
    os.system(f"pg_dump -U {LOCAL_POSTGRES_CONFIG['user']} -h {LOCAL_POSTGRES_CONFIG['host']} {LOCAL_POSTGRES_CONFIG['database']} > {backup_file}")
    print(f"백업 완료: {backup_file}")

# 데이터베이스 복원
def restore_database(backup_file: str):
    if not os.path.exists(backup_file):
        print(f"백업 파일을 찾을 수 없습니다: {backup_file}")
        return
    
    # psql 명령어로 복원
    os.system(f"psql -U {LOCAL_POSTGRES_CONFIG['user']} -h {LOCAL_POSTGRES_CONFIG['host']} {LOCAL_POSTGRES_CONFIG['database']} < {backup_file}")
    print(f"복원 완료: {backup_file}")

# 데이터베이스 최적화
def optimize_database():
    db = SessionLocal()
    try:
        # 통계 업데이트
        db.execute("ANALYZE")
        # 인덱스 재구성
        db.execute("REINDEX DATABASE construction_management")
        db.commit()
        print("데이터베이스 최적화 완료")
    except Exception as e:
        print(f"최적화 실패: {e}")
    finally:
        db.close() 