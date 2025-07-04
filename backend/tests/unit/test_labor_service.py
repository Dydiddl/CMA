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
            "name": "홍길동",
            "phone": "010-1234-5678",
            "id_number": "900101-1234567",
            "bank_name": "신한은행",
            "bank_account": "110-123-456789",
            "daily_wage": 20000,
            "status": "재직",
            "contract_id": "contract-1"
        }
    
    @pytest.mark.asyncio
    async def test_get_labor_by_id_success(self, labor_service, mock_db):
        """노무자 ID로 조회 성공 테스트"""
        # Given
        labor_id = "labor-test-123"
        mock_labor = Mock()
        mock_labor.id = "labor-test-123"
        mock_labor.name = "홍길동"
        mock_labor.phone = "010-1234-5678"
        mock_labor.id_number = "900101-1234567"
        mock_labor.bank_name = "신한은행"
        mock_labor.bank_account = "110-123-456789"
        mock_labor.daily_wage = 20000.0
        mock_labor.status = "재직"
        mock_labor.contract_id = "contract-test-123"
        mock_labor.project_id = "project-test-123"
        mock_labor.user_id = "user-test-123"
        mock_labor.deleted_at = None
        mock_labor.is_deleted = False
        mock_labor.created_at = "2024-01-01T00:00:00"
        mock_labor.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_labor
        
        # When
        result = await labor_service.get_labor_by_id(labor_id)
        
        # Then
        assert result is not None
        assert result.id == labor_id
        assert result.name == "홍길동"
        assert result.daily_wage == 20000.0
        mock_db.query.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_labor_success(self, labor_service, mock_db):
        """노무자 생성 성공 테스트"""
        # Given
        labor_data = LaborCreate(
            name="김철수",
            phone="010-9876-5432",
            id_number="880101-8765432",
            bank_name="국민은행",
            bank_account="123-456-789012",
            daily_wage=25000.0,
            status="재직",
            contract_id="contract-test-123",
            project_id="project-test-123",
            user_id="user-test-123"
        )
        
        mock_labor = Mock()
        mock_labor.id = "labor-new-123"
        mock_labor.name = "김철수"
        mock_labor.phone = "010-9876-5432"
        mock_labor.id_number = "880101-8765432"
        mock_labor.bank_name = "국민은행"
        mock_labor.bank_account = "123-456-789012"
        mock_labor.daily_wage = 25000.0
        mock_labor.status = "재직"
        mock_labor.contract_id = "contract-test-123"
        mock_labor.project_id = "project-test-123"
        mock_labor.user_id = "user-test-123"
        mock_labor.deleted_at = None
        mock_labor.is_deleted = False
        mock_labor.created_at = "2024-01-01T00:00:00"
        mock_labor.updated_at = "2024-01-01T00:00:00"
        
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # When
        result = await labor_service.create_labor(labor_data)
        
        # Then
        assert result is not None
        assert result.name == "김철수"
        assert result.daily_wage == 25000.0
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_labor_success(self, labor_service, mock_db):
        """노무자 수정 성공 테스트"""
        # Given
        labor_id = "labor-test-123"
        labor_update = LaborUpdate(
            name="수정된 홍길동",
            phone="010-1111-2222",
            daily_wage=22000.0,
            status="휴직"
        )
        
        mock_labor = Mock()
        mock_labor.id = "labor-test-123"
        mock_labor.name = "수정된 홍길동"
        mock_labor.phone = "010-1111-2222"
        mock_labor.id_number = "900101-1234567"
        mock_labor.bank_name = "신한은행"
        mock_labor.bank_account = "110-123-456789"
        mock_labor.daily_wage = 22000.0
        mock_labor.status = "휴직"
        mock_labor.contract_id = "contract-test-123"
        mock_labor.project_id = "project-test-123"
        mock_labor.user_id = "user-test-123"
        mock_labor.deleted_at = None
        mock_labor.is_deleted = False
        mock_labor.created_at = "2024-01-01T00:00:00"
        mock_labor.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_labor
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # When
        result = await labor_service.update_labor(labor_id, labor_update)
        
        # Then
        assert result is not None
        assert result.name == "수정된 홍길동"
        assert result.phone == "010-1111-2222"
        assert result.daily_wage == 22000.0
        assert result.status == "휴직"
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_labor_success(self, labor_service, mock_db):
        """노무자 삭제 성공 테스트"""
        # Given
        labor_id = "labor-test-123"
        mock_labor = Mock()
        mock_labor.id = "labor-test-123"
        mock_labor.name = "홍길동"
        mock_labor.phone = "010-1234-5678"
        mock_labor.id_number = "900101-1234567"
        mock_labor.bank_name = "신한은행"
        mock_labor.bank_account = "110-123-456789"
        mock_labor.daily_wage = 20000.0
        mock_labor.status = "재직"
        mock_labor.contract_id = "contract-test-123"
        mock_labor.project_id = "project-test-123"
        mock_labor.user_id = "user-test-123"
        mock_labor.deleted_at = None
        mock_labor.is_deleted = False
        mock_labor.created_at = "2024-01-01T00:00:00"
        mock_labor.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_labor
        mock_db.delete.return_value = None
        mock_db.commit.return_value = None
        
        # When
        result = await labor_service.delete_labor(labor_id)
        
        # Then
        assert result is True
        mock_db.delete.assert_called_once_with(mock_labor)
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_labors_success(self, labor_service, mock_db):
        """노무자 목록 조회 성공 테스트"""
        # Given
        mock_labor1 = Mock()
        mock_labor1.id = "labor-test-1"
        mock_labor1.name = "홍길동"
        mock_labor1.phone = "010-1234-5678"
        mock_labor1.id_number = "900101-1234567"
        mock_labor1.bank_name = "신한은행"
        mock_labor1.bank_account = "110-123-456789"
        mock_labor1.daily_wage = 20000.0
        mock_labor1.status = "재직"
        mock_labor1.contract_id = "contract-test-123"
        mock_labor1.project_id = "project-test-123"
        mock_labor1.user_id = "user-test-123"
        mock_labor1.deleted_at = None
        mock_labor1.is_deleted = False
        mock_labor1.created_at = "2024-01-01T00:00:00"
        mock_labor1.updated_at = "2024-01-01T00:00:00"
        
        mock_labor2 = Mock()
        mock_labor2.id = "labor-test-2"
        mock_labor2.name = "김철수"
        mock_labor2.phone = "010-9876-5432"
        mock_labor2.id_number = "880101-8765432"
        mock_labor2.bank_name = "국민은행"
        mock_labor2.bank_account = "123-456-789012"
        mock_labor2.daily_wage = 25000.0
        mock_labor2.status = "재직"
        mock_labor2.contract_id = "contract-test-123"
        mock_labor2.project_id = "project-test-123"
        mock_labor2.user_id = "user-test-123"
        mock_labor2.deleted_at = None
        mock_labor2.is_deleted = False
        mock_labor2.created_at = "2024-01-01T00:00:00"
        mock_labor2.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [mock_labor1, mock_labor2]
        mock_db.query.return_value.count.return_value = 2
        
        # When
        result, total = await labor_service.get_labors(skip=0, limit=10)
        
        # Then
        assert len(result) == 2
        assert total == 2
        assert result[0].name == "홍길동"
        assert result[1].name == "김철수"
    
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
        mock_labor.name = "홍길동"
        mock_labor.phone = "010-1234-5678"
        mock_labor.job_type = "기술자"
        mock_labor.status = "재직"
        mock_labor.created_at = "2024-01-01T00:00:00"
        mock_labor.updated_at = "2024-01-01T00:00:00"

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
    
    def test_update_labor_not_found(self, labor_service, mock_db):
        """노무자 수정 실패 테스트"""
        # Given
        labor_id = "non-existent-id"
        labor_service.db.query.return_value.filter.return_value.first.return_value = None
        
        labor_update = LaborUpdate(name="김철수")
        
        # When
        result = labor_service.update_labor(labor_id, labor_update)
        
        # Then
        assert result is None
    
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

        # Mock 생성된 레코드들
        mock_records = []
        for i, record_data in enumerate(records_data):
            mock_record = Mock()
            mock_record.id = f"record-{i+1}"
            mock_record.worker_id = record_data["worker_id"]
            mock_record.work_date = record_data["work_date"]
            mock_record.hours_worked = record_data["hours_worked"]
            mock_record.project_id = record_data["project_id"]
            mock_record.created_at = "2024-01-01T00:00:00"
            mock_record.updated_at = "2024-01-01T00:00:00"
            mock_records.append(mock_record)

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
        mock_index_stats = [{"indexname": "ix_labor_name", "idx_scan": 100}]
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
            name="통합테스트노무자",
            phone="010-1234-5678",
            id_number="900101-1234567",
            bank_name="신한은행",
            bank_account="110-123-456789",
            daily_wage=20000,
            status="재직",
            contract_id="contract-1"
        )
        
        # When - 노무자 생성
        created_labor = labor_service.create_labor(labor_data)
        
        # Then
        assert created_labor is not None
        assert created_labor.name == "통합테스트노무자"
        
        # When - 노무자 조회
        retrieved_labor = labor_service.get_labor_by_id(created_labor.id)
        
        # Then
        assert retrieved_labor is not None
        assert retrieved_labor.name == "통합테스트노무자"
        assert retrieved_labor.job_type == "기술자"
        
        # Cleanup
        labor_service.delete_labor(created_labor.id)
    
    def test_labor_list_pagination(self, labor_service, db_session):
        """노무자 목록 페이징 테스트"""
        # Given - 여러 노무자 생성
        labor_data_list = [
            LaborCreate(
                name=f"페이징테스트{i}",
                phone=f"010-1234-{i:04d}",
                id_number=f"900101-{i:06d}",
                bank_name="신한은행",
                bank_account="110-123-456789",
                daily_wage=20000,
                status="재직",
                contract_id=f"contract-{i}"
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
            name="검색테스트노무자",
            phone="010-1234-5678",
            id_number="900101-1234567",
            bank_name="신한은행",
            bank_account="110-123-456789",
            daily_wage=20000,
            status="재직",
            contract_id="contract-1"
        )
        
        created_labor = labor_service.create_labor(search_labor_data)
        
        try:
            # When - 이름으로 검색
            result_by_name, total_by_name = labor_service.get_labor_records(search="검색테스트")
            
            # Then
            assert total_by_name >= 1
            assert any("검색테스트" in labor.name for labor in result_by_name)
            
            # When - 연락처로 검색
            result_by_phone, total_by_phone = labor_service.get_labor_records(search="1234")
            
            # Then
            assert total_by_phone >= 1
            assert any("1234" in labor.phone for labor in result_by_phone)
            
        finally:
            # Cleanup
            labor_service.delete_labor(created_labor.id) 