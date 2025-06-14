from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import sqlite3
import threading
import time
import os
from pathlib import Path

# 데이터베이스 파일 경로 설정
DB_PATH = Path("data/db")
DB_PATH.mkdir(parents=True, exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}/construction_management.db"

# SQLite 최적화 설정
def _sqlite_on_connect(dbapi_connection, connection_record):
    # 성능 최적화 설정
    dbapi_connection.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging
    dbapi_connection.execute("PRAGMA synchronous = NORMAL")  # 동기화 모드
    dbapi_connection.execute("PRAGMA cache_size = -2000")  # 캐시 크기 (2MB)
    dbapi_connection.execute("PRAGMA temp_store = MEMORY")  # 임시 테이블을 메모리에 저장
    dbapi_connection.execute("PRAGMA mmap_size = 30000000000")  # 메모리 매핑 크기
    dbapi_connection.execute("PRAGMA page_size = 4096")  # 페이지 크기
    dbapi_connection.execute("PRAGMA busy_timeout = 5000")  # 타임아웃 설정
    dbapi_connection.execute("PRAGMA foreign_keys = ON")  # 외래 키 제약 조건

# 데이터베이스 백업 함수
def backup_database():
    backup_path = DB_PATH / f"backup_{int(time.time())}.db"
    try:
        # 데이터베이스 파일 복사
        import shutil
        shutil.copy2(DB_PATH / "construction_management.db", backup_path)
        print(f"백업 완료: {backup_path}")
    except Exception as e:
        print(f"백업 실패: {e}")

# 데이터베이스 최적화 함수
def optimize_database():
    db = SessionLocal()
    try:
        # 인덱스 재구성
        db.execute("REINDEX")
        # 통계 업데이트
        db.execute("ANALYZE")
        # 공간 회수
        db.execute("VACUUM")
        db.commit()
        print("데이터베이스 최적화 완료")
    except Exception as e:
        print(f"최적화 실패: {e}")
    finally:
        db.close()

# 주기적 백업 및 최적화 스케줄러
def schedule_maintenance():
    while True:
        try:
            # 매일 자정에 백업
            backup_database()
            # 매주 일요일 자정에 최적화
            if time.strftime("%A") == "Sunday":
                optimize_database()
        except Exception as e:
            print(f"유지보수 작업 실패: {e}")
        time.sleep(86400)  # 24시간 대기

# 데이터베이스 엔진 설정
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,
    },
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

# SQLite 연결 이벤트 리스너 등록
event.listen(engine, 'connect', _sqlite_on_connect)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 상태 모니터링
def monitor_database_status():
    db = SessionLocal()
    try:
        # 데이터베이스 크기 확인
        db_size = os.path.getsize(DB_PATH / "construction_management.db")
        print(f"데이터베이스 크기: {db_size / 1024 / 1024:.2f} MB")
        
        # 테이블 수 확인
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print(f"테이블 수: {len(tables)}")
        
        # 인덱스 수 확인
        indexes = db.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()
        print(f"인덱스 수: {len(indexes)}")
        
        # 페이지 크기 확인
        page_size = db.execute("PRAGMA page_size").scalar()
        print(f"페이지 크기: {page_size} bytes")
        
        # 캐시 크기 확인
        cache_size = db.execute("PRAGMA cache_size").scalar()
        print(f"캐시 크기: {cache_size} pages")
        
    except Exception as e:
        print(f"모니터링 실패: {e}")
    finally:
        db.close()

# 데이터베이스 초기화
def init_db():
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 초기화 완료")

# 동시성 테스트 함수
def test_concurrency():
    def worker(worker_id):
        db = SessionLocal()
        try:
            # 동시에 여러 작업 수행
            for i in range(10):
                try:
                    # 데이터베이스 작업 수행
                    db.execute("SELECT 1")
                    time.sleep(0.1)  # 작업 간격
                except Exception as e:
                    print(f"Worker {worker_id} error: {e}")
        finally:
            db.close()

    # 여러 스레드에서 동시 작업 수행
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# 성능 모니터링
def monitor_performance():
    start_time = time.time()
    db = SessionLocal()
    try:
        # 쿼리 실행 시간 측정
        result = db.execute("SELECT COUNT(*) FROM users").scalar()
        execution_time = time.time() - start_time
        print(f"Query execution time: {execution_time:.2f} seconds")
        return result
    finally:
        db.close() 