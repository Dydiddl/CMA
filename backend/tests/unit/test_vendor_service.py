#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
거래처 관리 서비스 테스트
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.exc import IntegrityError
from app.services.vendor import VendorService
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorDocumentCreate
from app.core.exceptions import ValidationException
from app.models.vendor import Vendor, VendorDocument


class TestVendorService:
    """거래처 관리 서비스 테스트 클래스"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock 데이터베이스 세션"""
        return Mock()
    
    @pytest.fixture
    def vendor_service(self, mock_db):
        """거래처 서비스 인스턴스"""
        return VendorService(mock_db)
    
    @pytest.fixture
    def sample_vendor_data(self):
        """샘플 거래처 데이터"""
        return {
            "name": "테스트 거래처",
            "business_number": "123-45-67890",
            "representative": "홍길동",
            "address": "서울시 강남구 테스트로 123",
            "phone": "02-1234-5678",
            "email": "test@vendor.com",
            "bank_name": "신한은행",
            "bank_account": "110-123-456789",
            "status": "활성",
            "description": "테스트용 거래처입니다."
        }
    
    @pytest.fixture
    def sample_vendor_model(self):
        """샘플 거래처 모델"""
        vendor = Mock(spec=Vendor)
        vendor.id = 1
        vendor.name = "테스트 거래처"
        vendor.business_number = "1234567890"
        vendor.representative = "홍길동"
        vendor.address = "서울시 강남구 테스트로 123"
        vendor.phone = "02-1234-5678"
        vendor.email = "test@vendor.com"
        vendor.bank_name = "신한은행"
        vendor.bank_account = "110-123-456789"
        vendor.status = "활성"
        vendor.description = "테스트용 거래처입니다."
        vendor.created_at = "2024-01-01T00:00:00"
        vendor.updated_at = "2024-01-01T00:00:00"
        return vendor
    
    def test_create_vendor_success(self, vendor_service, sample_vendor_data):
        """거래처 생성 성공 테스트"""
        # Given
        vendor_data = VendorCreate(**sample_vendor_data)
        new_vendor = Mock(spec=Vendor)
        new_vendor.id = 1
        new_vendor.name = vendor_data.name
        new_vendor.business_number = vendor_data.business_number
        new_vendor.representative = vendor_data.representative
        new_vendor.address = vendor_data.address
        new_vendor.phone = vendor_data.phone
        new_vendor.email = vendor_data.email
        new_vendor.bank_name = vendor_data.bank_name
        new_vendor.bank_account = vendor_data.bank_account
        new_vendor.status = vendor_data.status
        new_vendor.description = vendor_data.description
        new_vendor.created_at = "2024-01-01T00:00:00"
        new_vendor.updated_at = "2024-01-01T00:00:00"
        
        # Mock 설정
        vendor_service.db.add.return_value = None
        vendor_service.db.commit.return_value = None
        vendor_service.db.refresh.return_value = None
        
        # When
        result = vendor_service.create_vendor(vendor_data)
        
        # Then
        assert result is not None
        assert result.name == vendor_data.name
        assert result.business_number == vendor_data.business_number
        vendor_service.db.add.assert_called_once()
        vendor_service.db.commit.assert_called_once()
    
    def test_create_vendor_duplicate_error(self, vendor_service, sample_vendor_data):
        """중복 거래처 생성 실패 테스트"""
        # Given
        vendor_data = VendorCreate(**sample_vendor_data)
        
        # Mock 설정
        vendor_service.db.add.side_effect = IntegrityError("", "", "")
        
        # When & Then
        with pytest.raises(ValidationException, match="이미 존재하는 거래처입니다"):
            vendor_service.create_vendor(vendor_data)
        vendor_service.db.rollback.assert_called_once()
    
    def test_create_vendor_database_error(self, vendor_service, sample_vendor_data):
        """데이터베이스 오류로 거래처 생성 실패 테스트"""
        # Given
        vendor_data = VendorCreate(**sample_vendor_data)
        
        # Mock 설정
        vendor_service.db.add.side_effect = Exception("Database error")
        
        # When & Then
        with pytest.raises(ValidationException, match="거래처 생성 중 오류 발생"):
            vendor_service.create_vendor(vendor_data)
        vendor_service.db.rollback.assert_called_once()
    
    def test_get_vendors_success(self, vendor_service, sample_vendor_model):
        """거래처 목록 조회 성공 테스트"""
        # Given
        skip = 0
        limit = 10
        status = None
        search = None
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.all.return_value = [sample_vendor_model]
        
        # When
        vendors, total = vendor_service.get_vendors(skip, limit, status, search)
        
        # Then
        assert len(vendors) == 1
        assert total == 1
        assert vendors[0].name == sample_vendor_model.name
        assert vendors[0].business_number == sample_vendor_model.business_number
    
    def test_get_vendors_with_status_filter(self, vendor_service, sample_vendor_model):
        """상태 필터가 있는 거래처 목록 조회 테스트"""
        # Given
        skip = 0
        limit = 10
        status = "활성"
        search = None
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.all.return_value = [sample_vendor_model]
        
        # When
        vendors, total = vendor_service.get_vendors(skip, limit, status, search)
        
        # Then
        assert len(vendors) == 1
        assert total == 1
        mock_query.filter.assert_called()
    
    def test_get_vendors_with_search(self, vendor_service, sample_vendor_model):
        """검색어가 있는 거래처 목록 조회 테스트"""
        # Given
        skip = 0
        limit = 10
        status = None
        search = "테스트"
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.all.return_value = [sample_vendor_model]
        
        # When
        vendors, total = vendor_service.get_vendors(skip, limit, status, search)
        
        # Then
        assert len(vendors) == 1
        assert total == 1
        mock_query.filter.assert_called()
    
    def test_get_vendors_database_error(self, vendor_service):
        """데이터베이스 오류로 거래처 목록 조회 실패 테스트"""
        # Given
        vendor_service.db.query.side_effect = Exception("Database error")
        
        # When & Then
        with pytest.raises(ValidationException, match="거래처 목록 조회 중 오류 발생"):
            vendor_service.get_vendors()
    
    def test_get_vendor_success(self, vendor_service, sample_vendor_model):
        """거래처 상세 조회 성공 테스트"""
        # Given
        vendor_id = 1
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_vendor_model
        
        # When
        result = vendor_service.get_vendor(vendor_id)
        
        # Then
        assert result is not None
        assert result.name == sample_vendor_model.name
        assert result.business_number == sample_vendor_model.business_number
    
    def test_get_vendor_not_found(self, vendor_service):
        """존재하지 않는 거래처 조회 테스트"""
        # Given
        vendor_id = 999
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        # When
        result = vendor_service.get_vendor(vendor_id)
        
        # Then
        assert result is None
    
    def test_get_vendor_database_error(self, vendor_service):
        """데이터베이스 오류로 거래처 조회 실패 테스트"""
        # Given
        vendor_id = 1
        vendor_service.db.query.side_effect = Exception("Database error")
        
        # When & Then
        with pytest.raises(ValidationException, match="거래처 조회 중 오류 발생"):
            vendor_service.get_vendor(vendor_id)
    
    def test_update_vendor_success(self, vendor_service, sample_vendor_model):
        """거래처 정보 업데이트 성공 테스트"""
        # Given
        vendor_id = 1
        update_data = VendorUpdate(name="업데이트된 거래처명")
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_vendor_model
        vendor_service.db.commit.return_value = None
        vendor_service.db.refresh.return_value = None
        
        # When
        result = vendor_service.update_vendor(vendor_id, update_data)
        
        # Then
        assert result is not None
        assert result.name == "업데이트된 거래처명"
        vendor_service.db.commit.assert_called_once()
    
    def test_update_vendor_not_found(self, vendor_service):
        """존재하지 않는 거래처 업데이트 실패 테스트"""
        # Given
        vendor_id = 999
        update_data = VendorUpdate(name="업데이트된 거래처명")
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        # When
        result = vendor_service.update_vendor(vendor_id, update_data)
        
        # Then
        assert result is None
    
    def test_update_vendor_integrity_error(self, vendor_service, sample_vendor_model):
        """중복 오류로 거래처 업데이트 실패 테스트"""
        # Given
        vendor_id = 1
        update_data = VendorUpdate(name="업데이트된 거래처명")
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_vendor_model
        vendor_service.db.commit.side_effect = IntegrityError("", "", "")
        
        # When & Then
        with pytest.raises(ValidationException, match="이미 존재하는 거래처입니다"):
            vendor_service.update_vendor(vendor_id, update_data)
        vendor_service.db.rollback.assert_called_once()
    
    def test_delete_vendor_success(self, vendor_service, sample_vendor_model):
        """거래처 삭제 성공 테스트"""
        # Given
        vendor_id = 1
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_vendor_model
        vendor_service.db.delete.return_value = None
        vendor_service.db.commit.return_value = None
        
        # When
        result = vendor_service.delete_vendor(vendor_id)
        
        # Then
        assert result is True
        vendor_service.db.delete.assert_called_once_with(sample_vendor_model)
        vendor_service.db.commit.assert_called_once()
    
    def test_delete_vendor_not_found(self, vendor_service):
        """존재하지 않는 거래처 삭제 실패 테스트"""
        # Given
        vendor_id = 999
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        # When
        result = vendor_service.delete_vendor(vendor_id)
        
        # Then
        assert result is False
    
    def test_delete_vendor_database_error(self, vendor_service, sample_vendor_model):
        """데이터베이스 오류로 거래처 삭제 실패 테스트"""
        # Given
        vendor_id = 1
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_vendor_model
        vendor_service.db.delete.side_effect = Exception("Database error")
        
        # When & Then
        with pytest.raises(ValidationException, match="거래처 삭제 중 오류 발생"):
            vendor_service.delete_vendor(vendor_id)
        vendor_service.db.rollback.assert_called_once()
    
    def test_create_vendor_document_success(self, vendor_service):
        """거래처 문서 생성 성공 테스트"""
        # Given
        vendor_id = 1
        document_data = VendorDocumentCreate(
            name="사업자등록증",
            document_type="사업자등록증",
            file_name="사업자등록증.pdf",
            description="사업자등록증 문서"
        )
        new_document = Mock(spec=VendorDocument)
        new_document.id = 1
        new_document.name = document_data.name
        new_document.document_type = document_data.document_type
        new_document.file_name = document_data.file_name
        new_document.description = document_data.description
        new_document.vendor_id = vendor_id
        
        # Mock 설정
        vendor_service.db.add.return_value = None
        vendor_service.db.commit.return_value = None
        vendor_service.db.refresh.return_value = None
        
        # When
        result = vendor_service.create_vendor_document(vendor_id, document_data)
        
        # Then
        assert result is not None
        assert result.name == document_data.name
        assert result.file_path == document_data.file_path
        vendor_service.db.add.assert_called_once()
        vendor_service.db.commit.assert_called_once()
    
    def test_create_vendor_document_database_error(self, vendor_service):
        """데이터베이스 오류로 거래처 문서 생성 실패 테스트"""
        # Given
        vendor_id = 1
        document_data = VendorDocumentCreate(
            document_type="사업자등록증",
            file_name="사업자등록증.pdf",
            description="사업자등록증 문서"
        )
        
        # Mock 설정
        vendor_service.db.add.side_effect = Exception("Database error")
        
        # When & Then
        with pytest.raises(ValidationException, match="거래처 문서 생성 중 오류 발생"):
            vendor_service.create_vendor_document(vendor_id, document_data)
        vendor_service.db.rollback.assert_called_once()
    
    def test_get_vendor_documents_success(self, vendor_service):
        """거래처 문서 목록 조회 성공 테스트"""
        # Given
        vendor_id = 1
        document1 = Mock(spec=VendorDocument)
        document1.id = 1
        document1.name = "사업자등록증"
        document1.file_path = "/path/to/doc1.pdf"
        document1.document_type = "사업자등록증"
        
        document2 = Mock(spec=VendorDocument)
        document2.id = 2
        document2.name = "계약서"
        document2.file_path = "/path/to/doc2.pdf"
        document2.document_type = "계약서"
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [document1, document2]
        
        # When
        result = vendor_service.get_vendor_documents(vendor_id)
        
        # Then
        assert len(result) == 2
        assert result[0].name == "사업자등록증"
        assert result[1].name == "계약서"
    
    def test_get_vendor_documents_empty(self, vendor_service):
        """거래처 문서가 없는 경우 테스트"""
        # Given
        vendor_id = 1
        
        # Mock 설정
        mock_query = Mock()
        vendor_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []
        
        # When
        result = vendor_service.get_vendor_documents(vendor_id)
        
        # Then
        assert len(result) == 0 