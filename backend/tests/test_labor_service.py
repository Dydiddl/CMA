#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 노무 관리 서비스 테스트
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.services.labor_service import LaborService
from app.schemas.labor import LaborCreate, LaborUpdate
from app.models.labor import Labor
from app.core.exceptions import ValidationException, NotFoundException


class TestLaborService:
    """노무 관리 서비스 테스트"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock 데이터베이스 세션"""
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_cache(self):
        """Mock 캐시"""
        cache = Mock()
        cache.get.return_value = None
        cache.set.return_value = None
        cache.delete_pattern.return_value = None
        return cache
    
    @pytest.fixture
    def labor_service(self, mock_db, mock_cache):
        """노무 서비스 인스턴스"""
        with patch('app.services.labor_service.get_cache', return_value=mock_cache):
            return LaborService(mock_db)
    
    @pytest.fixture
    def sample_labor_data(self):
        """샘플 노무자 데이터"""
        return {
            "worker_name": "홍길동",
            "ssn": "900101-1234567",
            "birth_date": "1990-01-01",
            "gender": "남성",
            "job_type": "기술자",
            "hire_date": "2024-01-01",
            "hourly_wage": 20000,
            "work_hours": 8,
            "status": "재직",
            "contact": "010-1234-5678",
            "address": "서울시 강남구",
            "emergency_contact": "010-9876-5432",
            "memo": "테스트 노무자"
        }
    
    def test_create_labor_success(self, labor_service, mock_db, sample_labor_data):
        """노무자 생성 성공 테스트"""
        # Given
        labor_create = LaborCreate(**sample_labor_data)
        mock_labor = Mock(spec=Labor)
        mock_labor.worker_name = sample_labor_data["worker_name"]
        
        # 중복 검사 결과 (중복 없음)
        labor_service.db.query.return_value.filter.return_value.first.return_value = None
        
        # 생성된 노무자 반환
        labor_service.db.add.return_value = None
        labor_service.db.commit.return_value = None
        labor_service.db.refresh.return_value = None
        
        # When
        result = labor_service.create_labor(labor_create)
        
        # Then
        assert result is not None
        labor_service.db.add.assert_called_once()
        labor_service.db.commit.assert_called_once()
        labor_service.db.refresh.assert_called_once()
    
    def test_create_labor_duplicate_error(self, labor_service, mock_db, sample_labor_data):
        """노무자 생성 중복 오류 테스트"""
        # Given
        labor_create = LaborCreate(**sample_labor_data)
        
        # 중복 검사 결과 (중복 있음)
        mock_existing_labor = Mock(spec=Labor)
        labor_service.db.query.return_value.filter.return_value.first.return_value = mock_existing_labor
        
        # When & Then
        with pytest.raises(ValidationException, match="이미 존재하는 노무자입니다"):
            labor_service.create_labor(labor_create)
    
    def test_get_labor_records_success(self, labor_service, mock_db, mock_cache):
        """노무자 목록 조회 성공 테스트"""
        # Given
        mock_labor = Mock(spec=Labor)
        mock_labor.id = "test-id"
        mock_labor.worker_name = "홍길동"
        
        labor_service.db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [mock_labor]
        labor_service.db.query.return_value.filter.return_value.count.return_value = 1
        
        # When
        result, total = labor_service.get_labor_records(skip=0, limit=10)
        
        # Then
        assert len(result) == 1
        assert total == 1
        mock_cache.set.assert_called()
    
    def test_get_labor_records_with_cache(self, labor_service, mock_db, mock_cache):
        """노무자 목록 조회 캐시 테스트"""
        # Given
        cached_result = ([Mock()], 1)
        mock_cache.get.return_value = cached_result
        
        # When
        result, total = labor_service.get_labor_records(skip=0, limit=10)
        
        # Then
        assert result == cached_result[0]
        assert total == cached_result[1]
        # 데이터베이스 쿼리 호출되지 않음
        labor_service.db.query.assert_not_called()
    
    def test_get_labor_by_id_success(self, labor_service, mock_db, mock_cache):
        """노무자 ID로 조회 성공 테스트"""
        # Given
        labor_id = "test-id"
        mock_labor = Mock(spec=Labor)
        mock_labor.id = labor_id
        mock_labor.worker_name = "홍길동"
        
        labor_service.db.query.return_value.filter.return_value.first.return_value = mock_labor
        
        # When
        result = labor_service.get_labor_by_id(labor_id)
        
        # Then
        assert result is not None
        mock_cache.set.assert_called()
    
    def test_get_labor_by_id_not_found(self, labor_service, mock_db, mock_cache):
        """노무자 ID로 조회 실패 테스트"""
        # Given
        labor_id = "non-existent-id"
        labor_service.db.query.return_value.filter.return_value.first.return_value = None
        
        # When
        result = labor_service.get_labor_by_id(labor_id)
        
        # Then
        assert result is None
    
    def test_get_labor_by_id_with_cache(self, labor_service, mock_db, mock_cache):
        """노무자 ID로 조회 캐시 테스트"""
        # Given
        labor_id = "test-id"
        cached_labor = Mock()
        mock_cache.get.return_value = cached_labor
        
        # When
        result = labor_service.get_labor_by_id(labor_id)
        
        # Then
        assert result == cached_labor
        # 데이터베이스 쿼리 호출되지 않음
        labor_service.db.query.assert_not_called()
    
    def test_update_labor_success(self, labor_service, mock_db, sample_labor_data):
        """노무자 수정 성공 테스트"""
        # Given
        labor_id = "test-id"
        mock_labor = Mock(spec=Labor)
        mock_labor.id = labor_id
        mock_labor.worker_name = "홍길동"
        
        labor_service.db.query.return_value.filter.return_value.first.return_value = mock_labor
        labor_service.db.query.return_value.filter.return_value.first.return_value = None  # 중복 검사
        
        labor_update = LaborUpdate(worker_name="김철수")
        
        # When
        result = labor_service.update_labor(labor_id, labor_update)
        
        # Then
        assert result is not None
        labor_service.db.commit.assert_called_once()
    
    def test_update_labor_not_found(self, labor_service, mock_db):
        """노무자 수정 실패 테스트"""
        # Given
        labor_id = "non-existent-id"
        labor_service.db.query.return_value.filter.return_value.first.return_value = None
        
        labor_update = LaborUpdate(worker_name="김철수")
        
        # When
        result = labor_service.update_labor(labor_id, labor_update)
        
        # Then
        assert result is None
    
    def test_delete_labor_success(self, labor_service, mock_db):
        """노무자 삭제 성공 테스트"""
        # Given
        labor_id = "test-id"
        mock_labor = Mock(spec=Labor)
        mock_labor.id = labor_id
        mock_labor.worker_name = "홍길동"
        
        labor_service.db.query.return_value.filter.return_value.first.return_value = mock_labor
        labor_service.db.query.return_value.filter.return_value.count.return_value = 0
        
        # When
        result = labor_service.delete_labor(labor_id)
        
        # Then
        assert result is True
        labor_service.db.delete.assert_called_once_with(mock_labor)
        labor_service.db.commit.assert_called_once()
    
    def test_delete_labor_not_found(self, labor_service, mock_db):
        """노무자 삭제 실패 테스트"""
        # Given
        labor_id = "non-existent-id"
        labor_service.db.query.return_value.filter.return_value.first.return_value = None
        
        # When
        result = labor_service.delete_labor(labor_id)
        
        # Then
        assert result is False
    
    def test_get_labor_summary_success(self, labor_service, mock_db, mock_cache):
        """노무 요약 통계 성공 테스트"""
        # Given
        # Mock 통계 데이터
        labor_service.db.query.return_value.scalar.side_effect = [10, 8, 20000.0, 160.0, 3200000.0, 40.0, 800.0]
        labor_service.db.query.return_value.join.return_value.filter.return_value.first.return_value = Mock(
            total_hours=160.0,
            total_cost=3200000.0
        )
        
        # When
        result = labor_service.get_labor_summary()
        
        # Then
        assert result is not None
        assert "total_workers" in result
        assert "active_workers" in result
        assert "average_wage" in result
        mock_cache.set.assert_called()
    
    def test_get_labor_summary_with_cache(self, labor_service, mock_db, mock_cache):
        """노무 요약 통계 캐시 테스트"""
        # Given
        cached_summary = {
            "total_workers": 10,
            "active_workers": 8,
            "average_wage": 20000
        }
        mock_cache.get.return_value = cached_summary
        
        # When
        result = labor_service.get_labor_summary()
        
        # Then
        assert result == cached_summary
        # 데이터베이스 쿼리 호출되지 않음
        labor_service.db.query.assert_not_called()
    
    def test_batch_create_labor_records_success(self, labor_service, mock_db):
        """노무 기록 배치 생성 성공 테스트"""
        # Given
        records_data = [
            {
                "worker_id": "worker-1",
                "work_date": "2024-01-01",
                "hours_worked": 8,
                "project_id": "project-1"
            },
            {
                "worker_id": "worker-2",
                "work_date": "2024-01-01",
                "hours_worked": 8,
                "project_id": "project-1"
            }
        ]
        
        # When
        result = labor_service.batch_create_labor_records(records_data)
        
        # Then
        assert len(result) == 2
        labor_service.db.bulk_save_objects.assert_called_once()
        labor_service.db.commit.assert_called_once()
    
    def test_get_labor_statistics_by_period_success(self, labor_service, mock_db):
        """기간별 노무 통계 성공 테스트"""
        # Given
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        
        # Mock 통계 데이터
        mock_period_stats = Mock(
            total_records=20,
            total_hours=160.0,
            total_cost=3200000.0,
            avg_hours_per_day=8.0
        )
        
        mock_job_type_stats = [
            Mock(job_type="기술자", record_count=10, total_hours=80.0, total_cost=1600000.0),
            Mock(job_type="일반노무자", record_count=10, total_hours=80.0, total_cost=1600000.0)
        ]
        
        labor_service.db.query.return_value.join.return_value.filter.return_value.first.return_value = mock_period_stats
        labor_service.db.query.return_value.join.return_value.filter.return_value.group_by.return_value.all.return_value = mock_job_type_stats
        
        # When
        result = labor_service.get_labor_statistics_by_period(start_date, end_date)
        
        # Then
        assert result is not None
        assert "period_stats" in result
        assert "job_type_stats" in result
        assert len(result["job_type_stats"]) == 2
    
    def test_optimize_database_queries_success(self, labor_service, mock_db):
        """데이터베이스 쿼리 최적화 성공 테스트"""
        # Given
        mock_index_stats = [{"indexname": "ix_labor_worker_name", "idx_scan": 100}]
        mock_slow_queries = [{"query": "SELECT * FROM labor", "mean_time": 10.5}]
        
        labor_service.db.execute.return_value.fetchall.side_effect = [mock_index_stats, mock_slow_queries]
        
        # When
        result = labor_service.optimize_database_queries()
        
        # Then
        assert result is not None
        assert "index_stats" in result
        assert "slow_queries" in result
        assert len(result["index_stats"]) == 1
        assert len(result["slow_queries"]) == 1


class TestLaborServiceIntegration:
    """노무 관리 서비스 통합 테스트"""
    
    @pytest.fixture
    def db_session(self):
        """실제 데이터베이스 세션"""
        from app.core.database import get_db
        return next(get_db())
    
    @pytest.fixture
    def labor_service(self, db_session):
        """실제 노무 서비스 인스턴스"""
        return LaborService(db_session)
    
    def test_create_and_retrieve_labor(self, labor_service, db_session):
        """노무자 생성 및 조회 통합 테스트"""
        # Given
        labor_data = LaborCreate(
            worker_name="통합테스트노무자",
            ssn="900101-1234567",
            birth_date="1990-01-01",
            gender="남성",
            job_type="기술자",
            hire_date="2024-01-01",
            hourly_wage=20000,
            work_hours=8,
            status="재직",
            contact="010-1234-5678",
            address="서울시 강남구",
            emergency_contact="010-9876-5432",
            memo="통합 테스트용 노무자"
        )
        
        # When - 노무자 생성
        created_labor = labor_service.create_labor(labor_data)
        
        # Then
        assert created_labor is not None
        assert created_labor.worker_name == "통합테스트노무자"
        
        # When - 노무자 조회
        retrieved_labor = labor_service.get_labor_by_id(created_labor.id)
        
        # Then
        assert retrieved_labor is not None
        assert retrieved_labor.worker_name == "통합테스트노무자"
        assert retrieved_labor.job_type == "기술자"
        
        # Cleanup
        labor_service.delete_labor(created_labor.id)
    
    def test_labor_list_pagination(self, labor_service, db_session):
        """노무자 목록 페이징 테스트"""
        # Given - 여러 노무자 생성
        labor_data_list = [
            LaborCreate(
                worker_name=f"페이징테스트{i}",
                ssn=f"900101-{i:06d}",
                birth_date="1990-01-01",
                gender="남성",
                job_type="기술자",
                hire_date="2024-01-01",
                hourly_wage=20000,
                work_hours=8,
                status="재직",
                contact=f"010-1234-{i:04d}",
                address="서울시 강남구",
                emergency_contact="010-9876-5432",
                memo=f"페이징 테스트용 노무자 {i}"
            )
            for i in range(1, 6)
        ]
        
        created_labors = []
        for labor_data in labor_data_list:
            created_labor = labor_service.create_labor(labor_data)
            created_labors.append(created_labor)
        
        try:
            # When - 페이징 조회
            result_page1, total_page1 = labor_service.get_labor_records(skip=0, limit=2)
            result_page2, total_page2 = labor_service.get_labor_records(skip=2, limit=2)
            
            # Then
            assert total_page1 == total_page2
            assert len(result_page1) <= 2
            assert len(result_page2) <= 2
            
        finally:
            # Cleanup
            for labor in created_labors:
                labor_service.delete_labor(labor.id)
    
    def test_labor_search_functionality(self, labor_service, db_session):
        """노무자 검색 기능 테스트"""
        # Given - 검색용 노무자 생성
        search_labor_data = LaborCreate(
            worker_name="검색테스트노무자",
            ssn="900101-1234567",
            birth_date="1990-01-01",
            gender="남성",
            job_type="기술자",
            hire_date="2024-01-01",
            hourly_wage=20000,
            work_hours=8,
            status="재직",
            contact="010-1234-5678",
            address="서울시 강남구",
            emergency_contact="010-9876-5432",
            memo="검색 테스트용 노무자"
        )
        
        created_labor = labor_service.create_labor(search_labor_data)
        
        try:
            # When - 이름으로 검색
            result_by_name, total_by_name = labor_service.get_labor_records(search="검색테스트")
            
            # Then
            assert total_by_name >= 1
            assert any("검색테스트" in labor.worker_name for labor in result_by_name)
            
            # When - 연락처로 검색
            result_by_contact, total_by_contact = labor_service.get_labor_records(search="1234")
            
            # Then
            assert total_by_contact >= 1
            assert any("1234" in labor.contact for labor in result_by_contact)
            
        finally:
            # Cleanup
            labor_service.delete_labor(created_labor.id) 