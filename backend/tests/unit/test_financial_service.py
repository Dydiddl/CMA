#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
재무 관리 서비스 테스트
"""

import pytest
from unittest.mock import Mock, patch
from app.services.financial import (
    create_financial_record,
    get_financial_records,
    get_financial_record,
    update_financial_record,
    delete_financial_record,
    create_financial_document,
    get_financial_documents
)
from app.schemas.financial import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialDocumentCreate
)
from app.models.financial import FinancialRecord, FinancialDocument


class TestFinancialService:
    """재무 관리 서비스 테스트 클래스"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock 데이터베이스 세션"""
        return Mock()
    
    @pytest.fixture
    def sample_financial_record_data(self):
        """샘플 재무 기록 데이터"""
        return {
            "type": "수입",
            "category": "계약금",
            "amount": 1000000,
            "description": "테스트 계약금",
            "date": "2024-01-01",
            "contract_id": "contract-1",
            "vendor_id": "vendor-1"
        }
    
    @pytest.fixture
    def sample_financial_record_model(self):
        """샘플 재무 기록 모델"""
        record = Mock(spec=FinancialRecord)
        record.id = "financial-1"
        record.type = "수입"
        record.category = "계약금"
        record.amount = 1000000
        record.description = "테스트 계약금"
        record.date = "2024-01-01"
        record.contract_id = "contract-1"
        record.vendor_id = "vendor-1"
        record.created_at = "2024-01-01T00:00:00"
        record.updated_at = "2024-01-01T00:00:00"
        return record
    
    @pytest.fixture
    def sample_financial_document_data(self):
        """샘플 재무 문서 데이터"""
        return {
            "name": "계약서",
            "file_path": "/path/to/contract.pdf",
            "document_type": "계약서",
            "description": "테스트 계약서"
        }
    
    @pytest.fixture
    def sample_financial_document_model(self):
        """샘플 재무 문서 모델"""
        document = Mock(spec=FinancialDocument)
        document.id = "document-1"
        document.name = "계약서"
        document.file_path = "/path/to/contract.pdf"
        document.document_type = "계약서"
        document.description = "테스트 계약서"
        document.record_id = "financial-1"
        document.created_at = "2024-01-01T00:00:00"
        document.updated_at = "2024-01-01T00:00:00"
        return document
    
    def test_create_financial_record_not_implemented(self, mock_db, sample_financial_record_data):
        """재무 기록 생성 - 아직 구현되지 않음"""
        # Given
        record_data = FinancialRecordCreate(**sample_financial_record_data)
        
        # When
        result = create_financial_record(mock_db, record_data)
        
        # Then
        assert result is None  # 아직 구현되지 않아서 None 반환
    
    def test_get_financial_records_not_implemented(self, mock_db):
        """재무 기록 목록 조회 - 아직 구현되지 않음"""
        # Given
        skip = 0
        limit = 10
        type_filter = None
        category = None
        start_date = None
        end_date = None
        contract_id = None
        vendor_id = None
        
        # When
        result = get_financial_records(
            mock_db, skip, limit, type_filter, category,
            start_date, end_date, contract_id, vendor_id
        )
        
        # Then
        assert result == []  # 아직 구현되지 않아서 빈 리스트 반환
    
    def test_get_financial_record_not_implemented(self, mock_db):
        """재무 기록 상세 조회 - 아직 구현되지 않음"""
        # Given
        record_id = 1
        
        # When
        result = get_financial_record(mock_db, record_id)
        
        # Then
        assert result is None  # 아직 구현되지 않아서 None 반환
    
    def test_update_financial_record_not_implemented(self, mock_db, sample_financial_record_data):
        """재무 기록 수정 - 아직 구현되지 않음"""
        # Given
        record_id = 1
        update_data = FinancialRecordUpdate(**sample_financial_record_data)
        
        # When
        result = update_financial_record(mock_db, record_id, update_data)
        
        # Then
        assert result is None  # 아직 구현되지 않아서 None 반환
    
    def test_delete_financial_record_not_implemented(self, mock_db):
        """재무 기록 삭제 - 아직 구현되지 않음"""
        # Given
        record_id = 1
        
        # When
        result = delete_financial_record(mock_db, record_id)
        
        # Then
        assert result is False  # 아직 구현되지 않아서 False 반환
    
    def test_create_financial_document_not_implemented(self, mock_db, sample_financial_document_data):
        """재무 문서 생성 - 아직 구현되지 않음"""
        # Given
        record_id = 1
        document_data = FinancialDocumentCreate(**sample_financial_document_data)
        
        # When
        result = create_financial_document(mock_db, record_id, document_data)
        
        # Then
        assert result is None  # 아직 구현되지 않아서 None 반환
    
    def test_get_financial_documents_not_implemented(self, mock_db):
        """재무 문서 목록 조회 - 아직 구현되지 않음"""
        # Given
        record_id = 1
        
        # When
        result = get_financial_documents(mock_db, record_id)
        
        # Then
        assert result == []  # 아직 구현되지 않아서 빈 리스트 반환
    
    @pytest.mark.skip(reason="구현 완료 후 활성화")
    def test_create_financial_record_success(self, mock_db, sample_financial_record_data, sample_financial_record_model):
        """재무 기록 생성 성공 테스트 (구현 완료 후 활성화)"""
        # Given
        record_data = FinancialRecordCreate(**sample_financial_record_data)
        
        # Mock 설정
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # When
        result = create_financial_record(mock_db, record_data)
        
        # Then
        assert result is not None
        assert result.type == record_data.type
        assert result.amount == record_data.amount
        assert result.id == "financial-1"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    @pytest.mark.skip(reason="구현 완료 후 활성화")
    def test_get_financial_records_with_filters(self, mock_db, sample_financial_record_model):
        """필터가 있는 재무 기록 목록 조회 테스트 (구현 완료 후 활성화)"""
        # Given
        skip = 0
        limit = 10
        type_filter = "수입"
        category = "계약금"
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        contract_id = "contract-1"
        vendor_id = "vendor-1"
        
        # Mock 설정
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.all.return_value = [sample_financial_record_model]
        
        # When
        result = get_financial_records(
            mock_db, skip, limit, type_filter, category,
            start_date, end_date, contract_id, vendor_id
        )
        
        # Then
        assert len(result) == 1
        assert result[0].type == type_filter
        assert result[0].category == category
    
    @pytest.mark.skip(reason="구현 완료 후 활성화")
    def test_update_financial_record_success(self, mock_db, sample_financial_record_model):
        """재무 기록 수정 성공 테스트 (구현 완료 후 활성화)"""
        # Given
        record_id = "financial-1"
        update_data = FinancialRecordUpdate(amount=2000000, description="수정된 계약금")
        
        # Mock 설정
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_financial_record_model
        mock_db.commit.return_value = None
        
        # When
        result = update_financial_record(mock_db, record_id, update_data)
        
        # Then
        assert result is not None
        assert result.amount == 2000000
        assert result.description == "수정된 계약금"
        mock_db.commit.assert_called_once()
    
    @pytest.mark.skip(reason="구현 완료 후 활성화")
    def test_delete_financial_record_success(self, mock_db, sample_financial_record_model):
        """재무 기록 삭제 성공 테스트 (구현 완료 후 활성화)"""
        # Given
        record_id = "financial-1"
        
        # Mock 설정
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_financial_record_model
        mock_db.delete.return_value = None
        mock_db.commit.return_value = None
        
        # When
        result = delete_financial_record(mock_db, record_id)
        
        # Then
        assert result is True
        mock_db.delete.assert_called_once_with(sample_financial_record_model)
        mock_db.commit.assert_called_once()
    
    @pytest.mark.skip(reason="구현 완료 후 활성화")
    def test_create_financial_document_success(self, mock_db, sample_financial_document_data, sample_financial_document_model):
        """재무 문서 생성 성공 테스트 (구현 완료 후 활성화)"""
        # Given
        record_id = "financial-1"
        document_data = FinancialDocumentCreate(**sample_financial_document_data)
        
        # Mock 설정
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # When
        result = create_financial_document(mock_db, record_id, document_data)
        
        # Then
        assert result is not None
        assert result.name == document_data.name
        assert result.file_path == document_data.file_path
        assert result.record_id == record_id
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    @pytest.mark.skip(reason="구현 완료 후 활성화")
    def test_get_financial_documents_success(self, mock_db, sample_financial_document_model):
        """재무 문서 목록 조회 성공 테스트 (구현 완료 후 활성화)"""
        # Given
        record_id = "financial-1"
        
        # Mock 설정
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [sample_financial_document_model]
        
        # When
        result = get_financial_documents(mock_db, record_id)
        
        # Then
        assert len(result) == 1
        assert result[0].name == "계약서"
        assert result[0].record_id == record_id

    @pytest.mark.asyncio
    async def test_get_financial_record_by_id_success(self, financial_service, mock_db):
        """재무 기록 ID로 조회 성공 테스트"""
        # Given
        record_id = "financial-test-123"
        mock_record = Mock()
        mock_record.id = "financial-test-123"
        mock_record.contract_id = "contract-test-123"
        mock_record.project_id = "project-test-123"
        mock_record.transaction_date = "2024-01-01"
        mock_record.date = "2024-01-01"
        mock_record.amount = 1000000.0
        mock_record.type = "수입"
        mock_record.category = "계약금"
        mock_record.description = "테스트 계약금"
        mock_record.payment_method = "계좌이체"
        mock_record.status = "지급완료"
        mock_record.vendor_id = "vendor-test-123"
        mock_record.user_id = "user-test-123"
        mock_record.deleted_at = None
        mock_record.is_deleted = False
        mock_record.created_at = "2024-01-01T00:00:00"
        mock_record.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_record
        
        # When
        result = await financial_service.get_financial_record_by_id(record_id)
        
        # Then
        assert result is not None
        assert result.id == record_id
        assert result.amount == 1000000.0
        assert result.type == "수입"
        mock_db.query.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_financial_record_success(self, financial_service, mock_db):
        """재무 기록 생성 성공 테스트"""
        # Given
        record_data = FinancialRecordCreate(
            contract_id="contract-test-123",
            transaction_date="2024-01-01",
            amount=500000.0,
            type="지출",
            category="자재비",
            description="테스트 자재비",
            payment_method="현금",
            status="지급완료",
            vendor_id="vendor-test-123"
        )
        
        mock_record = Mock()
        mock_record.id = "financial-new-123"
        mock_record.contract_id = "contract-test-123"
        mock_record.project_id = "project-test-123"
        mock_record.transaction_date = "2024-01-01"
        mock_record.date = "2024-01-01"
        mock_record.amount = 500000.0
        mock_record.type = "지출"
        mock_record.category = "자재비"
        mock_record.description = "테스트 자재비"
        mock_record.payment_method = "현금"
        mock_record.status = "지급완료"
        mock_record.vendor_id = "vendor-test-123"
        mock_record.user_id = "user-test-123"
        mock_record.deleted_at = None
        mock_record.is_deleted = False
        mock_record.created_at = "2024-01-01T00:00:00"
        mock_record.updated_at = "2024-01-01T00:00:00"
        
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # When
        result = await financial_service.create_financial_record(record_data)
        
        # Then
        assert result is not None
        assert result.amount == 500000.0
        assert result.type == "지출"
        assert result.category == "자재비"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_financial_record_success(self, financial_service, mock_db):
        """재무 기록 수정 성공 테스트"""
        # Given
        record_id = "financial-test-123"
        record_update = FinancialRecordUpdate(
            amount=1200000.0,
            description="수정된 계약금",
            status="지급대기"
        )
        
        mock_record = Mock()
        mock_record.id = "financial-test-123"
        mock_record.contract_id = "contract-test-123"
        mock_record.project_id = "project-test-123"
        mock_record.transaction_date = "2024-01-01"
        mock_record.date = "2024-01-01"
        mock_record.amount = 1200000.0
        mock_record.type = "수입"
        mock_record.category = "계약금"
        mock_record.description = "수정된 계약금"
        mock_record.payment_method = "계좌이체"
        mock_record.status = "지급대기"
        mock_record.vendor_id = "vendor-test-123"
        mock_record.user_id = "user-test-123"
        mock_record.deleted_at = None
        mock_record.is_deleted = False
        mock_record.created_at = "2024-01-01T00:00:00"
        mock_record.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_record
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # When
        result = await financial_service.update_financial_record(record_id, record_update)
        
        # Then
        assert result is not None
        assert result.amount == 1200000.0
        assert result.description == "수정된 계약금"
        assert result.status == "지급대기"
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_financial_record_success(self, financial_service, mock_db):
        """재무 기록 삭제 성공 테스트"""
        # Given
        record_id = "financial-test-123"
        mock_record = Mock()
        mock_record.id = "financial-test-123"
        mock_record.contract_id = "contract-test-123"
        mock_record.project_id = "project-test-123"
        mock_record.transaction_date = "2024-01-01"
        mock_record.date = "2024-01-01"
        mock_record.amount = 1000000.0
        mock_record.type = "수입"
        mock_record.category = "계약금"
        mock_record.description = "테스트 계약금"
        mock_record.payment_method = "계좌이체"
        mock_record.status = "지급완료"
        mock_record.vendor_id = "vendor-test-123"
        mock_record.user_id = "user-test-123"
        mock_record.deleted_at = None
        mock_record.is_deleted = False
        mock_record.created_at = "2024-01-01T00:00:00"
        mock_record.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_record
        mock_db.delete.return_value = None
        mock_db.commit.return_value = None
        
        # When
        result = await financial_service.delete_financial_record(record_id)
        
        # Then
        assert result is True
        mock_db.delete.assert_called_once_with(mock_record)
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_financial_records_success(self, financial_service, mock_db):
        """재무 기록 목록 조회 성공 테스트"""
        # Given
        mock_record1 = Mock()
        mock_record1.id = "financial-test-1"
        mock_record1.contract_id = "contract-test-123"
        mock_record1.project_id = "project-test-123"
        mock_record1.transaction_date = "2024-01-01"
        mock_record1.date = "2024-01-01"
        mock_record1.amount = 1000000.0
        mock_record1.type = "수입"
        mock_record1.category = "계약금"
        mock_record1.description = "테스트 계약금 1"
        mock_record1.payment_method = "계좌이체"
        mock_record1.status = "지급완료"
        mock_record1.vendor_id = "vendor-test-123"
        mock_record1.user_id = "user-test-123"
        mock_record1.deleted_at = None
        mock_record1.is_deleted = False
        mock_record1.created_at = "2024-01-01T00:00:00"
        mock_record1.updated_at = "2024-01-01T00:00:00"
        
        mock_record2 = Mock()
        mock_record2.id = "financial-test-2"
        mock_record2.contract_id = "contract-test-123"
        mock_record2.project_id = "project-test-123"
        mock_record2.transaction_date = "2024-01-02"
        mock_record2.date = "2024-01-02"
        mock_record2.amount = 500000.0
        mock_record2.type = "지출"
        mock_record2.category = "자재비"
        mock_record2.description = "테스트 자재비 2"
        mock_record2.payment_method = "현금"
        mock_record2.status = "지급완료"
        mock_record2.vendor_id = "vendor-test-123"
        mock_record2.user_id = "user-test-123"
        mock_record2.deleted_at = None
        mock_record2.is_deleted = False
        mock_record2.created_at = "2024-01-01T00:00:00"
        mock_record2.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [mock_record1, mock_record2]
        mock_db.query.return_value.count.return_value = 2
        
        # When
        result, total = await financial_service.get_financial_records(skip=0, limit=10)
        
        # Then
        assert len(result) == 2
        assert total == 2
        assert result[0].type == "수입"
        assert result[1].type == "지출" 