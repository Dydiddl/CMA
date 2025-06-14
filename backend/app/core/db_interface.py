from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

Base = declarative_base()

class DatabaseInterface(ABC):
    @abstractmethod
    def get_connection(self) -> Any:
        pass
    
    @abstractmethod
    def get_session(self) -> Session:
        pass
    
    @abstractmethod
    def backup(self) -> str:
        pass
    
    @abstractmethod
    def restore(self, backup_path: str) -> bool:
        pass
    
    @abstractmethod
    def optimize(self) -> bool:
        pass

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_path: str = "data/db/construction_management.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def get_connection(self):
        return self.engine
    
    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def backup(self) -> str:
        backup_path = self.db_path.parent / f"backup_{int(time.time())}.db"
        import shutil
        shutil.copy2(self.db_path, backup_path)
        return str(backup_path)
    
    def restore(self, backup_path: str) -> bool:
        if not os.path.exists(backup_path):
            return False
        import shutil
        shutil.copy2(backup_path, self.db_path)
        return True
    
    def optimize(self) -> bool:
        try:
            with self.get_session() as session:
                session.execute("VACUUM")
                session.execute("ANALYZE")
                session.commit()
            return True
        except Exception:
            return False

class PostgreSQLDatabase(DatabaseInterface):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def get_connection(self):
        return self.engine
    
    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def backup(self) -> str:
        backup_path = f"data/backups/backup_{int(time.time())}.sql"
        os.system(f"pg_dump -U postgres construction_management > {backup_path}")
        return backup_path
    
    def restore(self, backup_path: str) -> bool:
        if not os.path.exists(backup_path):
            return False
        os.system(f"psql -U postgres construction_management < {backup_path}")
        return True
    
    def optimize(self) -> bool:
        try:
            with self.get_session() as session:
                session.execute("VACUUM ANALYZE")
                session.commit()
            return True
        except Exception:
            return False

class DatabaseFactory:
    @staticmethod
    def create_database(db_type: str, **kwargs) -> DatabaseInterface:
        if db_type == "sqlite":
            return SQLiteDatabase(**kwargs)
        elif db_type == "postgresql":
            return PostgreSQLDatabase(**kwargs)
        else:
            raise ValueError(f"지원하지 않는 데이터베이스 타입: {db_type}")

# 데이터베이스 설정
def get_database() -> DatabaseInterface:
    db_type = os.getenv("DB_TYPE", "sqlite")
    if db_type == "sqlite":
        return DatabaseFactory.create_database("sqlite")
    else:
        connection_string = os.getenv("DATABASE_URL")
        if not connection_string:
            raise ValueError("DATABASE_URL 환경 변수가 설정되지 않았습니다.")
        return DatabaseFactory.create_database("postgresql", connection_string=connection_string)

# 데이터베이스 세션 의존성
def get_db():
    db = get_database().get_session()
    try:
        yield db
    finally:
        db.close() 