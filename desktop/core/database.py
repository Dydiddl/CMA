#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 데이터베이스 관리자
"""

import logging
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

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
            self.engine = create_engine(self.database_url)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # 연결 테스트
            with self.engine.connect() as conn:
                from sqlalchemy import text
                conn.execute(text("SELECT 1"))
            
            logger.info("[SUCCESS] 데이터베이스 연결 성공")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] 데이터베이스 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 종료"""
        try:
            if self._session:
                self._session.close()
            if self.engine:
                self.engine.dispose()
            logger.info("[SUCCESS] 데이터베이스 연결 종료")
        except Exception as e:
            logger.error(f"[ERROR] 데이터베이스 연결 종료 실패: {e}")
    
    def get_session(self) -> Optional[Session]:
        """데이터베이스 세션 반환"""
        if not self.SessionLocal:
            logger.error("[ERROR] 데이터베이스가 연결되지 않았습니다")
            return None
        
        if not self._session:
            self._session = self.SessionLocal()
        
        return self._session 