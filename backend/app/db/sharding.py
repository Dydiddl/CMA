"""
데이터베이스 샤딩 구현 모듈
"""
from typing import List, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..core.config import settings
import hashlib

class ShardManager:
    """
    데이터베이스 샤드 관리 클래스
    """
    def __init__(self):
        self.shard_map: Dict[int, str] = {
            0: settings.SQLALCHEMY_DATABASE_URI,  # 기본 데이터베이스
            1: settings.SHARD_1_DATABASE_URI,     # 샤드 1
            2: settings.SHARD_2_DATABASE_URI,     # 샤드 2
        }
        self.shard_engines = {}
        self._initialize_engines()

    def _initialize_engines(self):
        """
        각 샤드에 대한 데이터베이스 엔진을 초기화합니다.
        """
        for shard_id, uri in self.shard_map.items():
            self.shard_engines[shard_id] = create_engine(
                uri,
                pool_size=10,
                max_overflow=5,
                pool_timeout=30
            )

    def get_shard_id(self, key: str) -> int:
        """
        주어진 키에 대한 샤드 ID를 계산합니다.
        """
        hash_value = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
        return hash_value % len(self.shard_map)

    def get_engine(self, shard_id: int):
        """
        특정 샤드의 데이터베이스 엔진을 반환합니다.
        """
        return self.shard_engines.get(shard_id)

class ShardedSession:
    """
    샤딩된 데이터베이스 세션 관리 클래스
    """
    def __init__(self, shard_manager: ShardManager):
        self.shard_manager = shard_manager
        self.sessions: Dict[int, Session] = {}

    def get_session(self, key: str) -> Session:
        """
        주어진 키에 해당하는 샤드의 세션을 반환합니다.
        """
        shard_id = self.shard_manager.get_shard_id(key)
        if shard_id not in self.sessions:
            engine = self.shard_manager.get_engine(shard_id)
            self.sessions[shard_id] = Session(engine)
        return self.sessions[shard_id]

    def close_all(self):
        """
        모든 세션을 종료합니다.
        """
        for session in self.sessions.values():
            session.close()

# 샤드 매니저 인스턴스 생성
shard_manager = ShardManager()

def get_sharded_session(key: str) -> Session:
    """
    샤딩된 세션을 반환하는 의존성 함수
    """
    session = ShardedSession(shard_manager)
    try:
        yield session.get_session(key)
    finally:
        session.close_all()

def init_shards():
    """
    모든 샤드를 초기화합니다.
    """
    from ..models.base import Base
    
    for shard_id, engine in shard_manager.shard_engines.items():
        Base.metadata.create_all(bind=engine)
        print(f"✅ 샤드 {shard_id} 초기화 완료") 