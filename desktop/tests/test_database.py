#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 데이터베이스 테스트
"""

import pytest
import tempfile
import os
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
import sys
sys.path.insert(0, str(project_root))

from desktop.core.database import DatabaseManager
from desktop.core.exceptions import DatabaseConnectionError, DatabaseQueryError


class TestDatabaseManager:
    """데이터베이스 관리자 테스트 클래스"""
    
    @pytest.fixture
    def temp_db_path(self):
        """임시 데이터베이스 경로 생성"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        yield db_path
        # 테스트 후 정리
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    @pytest.fixture
    def db_manager(self, temp_db_path):
        """데이터베이스 관리자 인스턴스 생성"""
        db_url = f"sqlite:///{temp_db_path}"
        manager = DatabaseManager(db_url)
        yield manager
        # 테스트 후 연결 종료
        manager.disconnect()
    
    def test_database_connection(self, db_manager):
        """데이터베이스 연결 테스트"""
        # 연결 성공 테스트
        assert db_manager.connect() is True
        
        # 연결 상태 확인
        assert db_manager.engine is not None
        assert db_manager.SessionLocal is not None
    
    def test_database_disconnect(self, db_manager):
        """데이터베이스 연결 종료 테스트"""
        # 연결 후 종료
        db_manager.connect()
        db_manager.disconnect()
        
        # 연결 종료 확인
        assert db_manager.engine is None
        assert db_manager._session is None
    
    def test_get_session(self, db_manager):
        """세션 반환 테스트"""
        db_manager.connect()
        session = db_manager.get_session()
        
        # 세션 생성 확인
        assert session is not None
        assert db_manager._session is not None
    
    def test_connection_test(self, db_manager):
        """연결 상태 테스트"""
        db_manager.connect()
        
        # 연결 상태 확인
        assert db_manager.test_connection() is True
    
    def test_invalid_database_url(self):
        """잘못된 데이터베이스 URL 테스트"""
        # 잘못된 URL로 관리자 생성
        manager = DatabaseManager("invalid://url")
        
        # 연결 실패 예상
        with pytest.raises(DatabaseConnectionError):
            manager.connect()
    
    def test_query_execution(self, db_manager):
        """쿼리 실행 테스트"""
        db_manager.connect()
        
        def test_query(session):
            """테스트 쿼리 함수"""
            from sqlalchemy import text
            result = session.execute(text("SELECT 1 as test_value"))
            return result.fetchone()[0]
        
        # 쿼리 실행
        result = db_manager.execute_query(test_query)
        assert result == 1
    
    def test_query_error_handling(self, db_manager):
        """쿼리 오류 처리 테스트"""
        db_manager.connect()
        
        def invalid_query(session):
            """잘못된 쿼리 함수"""
            from sqlalchemy import text
            session.execute(text("SELECT * FROM non_existent_table"))
        
        # 쿼리 오류 예상
        with pytest.raises(DatabaseQueryError):
            db_manager.execute_query(invalid_query)


if __name__ == "__main__":
    pytest.main([__file__]) 