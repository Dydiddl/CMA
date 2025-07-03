#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 데이터베이스 관리자
"""

import logging
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DisconnectionError

from .exceptions import (
    DatabaseConnectionError, 
    DatabaseQueryError
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """데이터베이스 관리자 클래스"""
    
    def __init__(self, database_url: str = "sqlite:///cma_desktop.db"):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self._session: Optional[Session] = None
    
    def connect(self) -> bool:
        """데이터베이스 연결"""
        try:
            logger.info(f"[INFO] 데이터베이스 연결 시도: {self.database_url}")
            
            # 엔진 생성
            self.engine = create_engine(
                self.database_url,
                echo=False,  # SQL 로그 비활성화
                pool_pre_ping=True,  # 연결 상태 확인
                pool_recycle=3600  # 1시간마다 연결 재생성
            )
            
            # 세션 팩토리 생성
            self.SessionLocal = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=self.engine
            )
            
            # 연결 테스트
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            
            logger.info("[SUCCESS] 데이터베이스 연결 성공")
            return True
            
        except OperationalError as e:
            error_msg = f"데이터베이스 연결 실패 (운영 오류): {e}"
            logger.error(f"[ERROR] {error_msg}")
            raise DatabaseConnectionError(error_msg, details={"error_type": "operational"})
            
        except DisconnectionError as e:
            error_msg = f"데이터베이스 연결 실패 (연결 해제 오류): {e}"
            logger.error(f"[ERROR] {error_msg}")
            raise DatabaseConnectionError(error_msg, details={"error_type": "disconnection"})
            
        except SQLAlchemyError as e:
            error_msg = f"데이터베이스 연결 실패 (SQLAlchemy 오류): {e}"
            logger.error(f"[ERROR] {error_msg}")
            raise DatabaseConnectionError(error_msg, details={"error_type": "sqlalchemy"})
            
        except Exception as e:
            error_msg = f"데이터베이스 연결 실패 (예상치 못한 오류): {e}"
            logger.error(f"[ERROR] {error_msg}")
            raise DatabaseConnectionError(error_msg, details={"error_type": "unknown"})
    
    def disconnect(self):
        """데이터베이스 연결 종료"""
        try:
            if self._session:
                self._session.close()
                self._session = None
                logger.info("[INFO] 데이터베이스 세션 종료")
                
            if self.engine:
                self.engine.dispose()
                self.engine = None
                logger.info("[SUCCESS] 데이터베이스 연결 종료")
                
        except Exception as e:
            logger.error(f"[ERROR] 데이터베이스 연결 종료 실패: {e}")
    
    def get_session(self) -> Optional[Session]:
        """데이터베이스 세션 반환"""
        if not self.SessionLocal:
            error_msg = "데이터베이스가 연결되지 않았습니다"
            logger.error(f"[ERROR] {error_msg}")
            raise DatabaseConnectionError(error_msg)
        
        if not self._session:
            try:
                self._session = self.SessionLocal()
                logger.debug("[DEBUG] 새로운 데이터베이스 세션 생성")
            except Exception as e:
                error_msg = f"데이터베이스 세션 생성 실패: {e}"
                logger.error(f"[ERROR] {error_msg}")
                raise DatabaseConnectionError(error_msg)
        
        return self._session
    
    def execute_query(self, query_func, *args, **kwargs):
        """안전한 쿼리 실행"""
        session = self.get_session()
        try:
            result = query_func(session, *args, **kwargs)
            session.commit()
            return result
        except SQLAlchemyError as e:
            session.rollback()
            error_msg = f"데이터베이스 쿼리 실행 실패: {e}"
            logger.error(f"[ERROR] {error_msg}")
            raise DatabaseQueryError(error_msg, details={"query_func": query_func.__name__})
        except Exception as e:
            session.rollback()
            error_msg = f"예상치 못한 데이터베이스 오류: {e}"
            logger.error(f"[ERROR] {error_msg}")
            raise DatabaseQueryError(error_msg, details={"query_func": query_func.__name__})
    
    def test_connection(self) -> bool:
        """데이터베이스 연결 상태 테스트"""
        try:
            if self.engine:
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                    return True
            return False
        except Exception as e:
            logger.warning(f"[WARNING] 데이터베이스 연결 테스트 실패: {e}")
            return False 