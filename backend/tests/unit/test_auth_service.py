#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인증 서비스 테스트
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.exc import IntegrityError
from app.services.auth import AuthService
from app.schemas.auth import RegisterRequest
from app.models.user import User
from app.core.exceptions import AuthenticationException


class TestAuthService:
    """인증 서비스 테스트 클래스"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock 데이터베이스 세션"""
        return Mock()
    
    @pytest.fixture
    def auth_service(self, mock_db):
        """인증 서비스 인스턴스"""
        return AuthService(mock_db)
    
    @pytest.fixture
    def sample_user_data(self):
        """샘플 사용자 데이터"""
        return {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "테스트 사용자"
        }
    
    @pytest.fixture
    def sample_user(self):
        """샘플 사용자 모델"""
        user = Mock(spec=User)
        user.id = "user-123"
        user.email = "test@example.com"
        user.password_hash = "$5$rounds=535000$test_hash$hashed_password"
        user.full_name = "테스트 사용자"
        user.role = "user"
        user.is_active = True
        return user
    
    def test_verify_password_success(self, auth_service):
        """비밀번호 검증 성공 테스트"""
        # Given
        plain_password = "testpassword123"
        hashed_password = auth_service.get_password_hash(plain_password)
        
        # When
        result = auth_service.verify_password(plain_password, hashed_password)
        
        # Then
        assert result is True
    
    def test_verify_password_failure(self, auth_service):
        """비밀번호 검증 실패 테스트"""
        # Given
        plain_password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed_password = auth_service.get_password_hash(plain_password)
        
        # When
        result = auth_service.verify_password(wrong_password, hashed_password)
        
        # Then
        assert result is False
    
    def test_get_password_hash_success(self, auth_service):
        """비밀번호 해싱 성공 테스트"""
        # Given
        password = "testpassword123"
        
        # When
        hashed = auth_service.get_password_hash(password)
        
        # Then
        assert hashed != password
        assert len(hashed) > len(password)
        assert hashed.startswith("$5$")
    
    def test_get_password_hash_empty_password(self, auth_service):
        """빈 비밀번호 해싱 테스트"""
        # Given
        password = ""
        
        # When & Then
        with pytest.raises(ValueError):
            auth_service.get_password_hash(password)
    
    def test_authenticate_user_success(self, auth_service, sample_user):
        """사용자 인증 성공 테스트"""
        # Given
        email = "test@example.com"
        password = "testpassword123"
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = sample_user
        with patch.object(auth_service, 'verify_password', return_value=True):
            
            # When
            result = auth_service.authenticate_user(email, password)
            
            # Then
            assert result == sample_user
            auth_service.db.query.assert_called_once()
    
    def test_authenticate_user_invalid_email(self, auth_service):
        """잘못된 이메일로 인증 실패 테스트"""
        # Given
        email = "nonexistent@example.com"
        password = "testpassword123"
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = None
        
        # When
        result = auth_service.authenticate_user(email, password)
        
        # Then
        assert result is None
    
    def test_authenticate_user_invalid_password(self, auth_service, sample_user):
        """잘못된 비밀번호로 인증 실패 테스트"""
        # Given
        email = "test@example.com"
        password = "wrongpassword"
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = sample_user
        with patch.object(auth_service, 'verify_password', return_value=False):
            
            # When
            result = auth_service.authenticate_user(email, password)
            
            # Then
            assert result is None
    
    def test_create_user_success(self, auth_service, sample_user_data):
        """사용자 생성 성공 테스트"""
        # Given
        register_data = RegisterRequest(**sample_user_data)
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = None
        auth_service.db.add.return_value = None
        auth_service.db.commit.return_value = None
        auth_service.db.refresh.return_value = None
        
        # When
        result = auth_service.create_user(register_data)
        
        # Then
        assert result is not None
        assert result.email == sample_user_data["email"]
        assert result.full_name == sample_user_data["name"]
        auth_service.db.add.assert_called_once()
        auth_service.db.commit.assert_called_once()
    
    def test_create_user_duplicate_email(self, auth_service, sample_user_data):
        """중복 이메일로 사용자 생성 실패 테스트"""
        # Given
        register_data = RegisterRequest(**sample_user_data)
        existing_user = Mock()
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = existing_user
        
        # When & Then
        with pytest.raises(ValueError, match="이미 존재하는 이메일입니다"):
            auth_service.create_user(register_data)
    
    def test_create_user_database_error(self, auth_service, sample_user_data):
        """데이터베이스 오류로 사용자 생성 실패 테스트"""
        # Given
        register_data = RegisterRequest(**sample_user_data)
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = None
        auth_service.db.add.side_effect = IntegrityError("", "", "")
        
        # When & Then
        with pytest.raises(ValueError, match="이미 존재하는 이메일입니다"):
            auth_service.create_user(register_data)
        auth_service.db.rollback.assert_called_once()
    
    def test_get_user_by_email_success(self, auth_service, sample_user):
        """이메일로 사용자 조회 성공 테스트"""
        # Given
        email = "test@example.com"
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = sample_user
        
        # When
        result = auth_service.get_user_by_email(email)
        
        # Then
        assert result == sample_user
        auth_service.db.query.assert_called_once()
    
    def test_get_user_by_email_not_found(self, auth_service):
        """존재하지 않는 이메일로 사용자 조회 테스트"""
        # Given
        email = "nonexistent@example.com"
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = None
        
        # When
        result = auth_service.get_user_by_email(email)
        
        # Then
        assert result is None
    
    def test_get_user_by_id_success(self, auth_service, sample_user):
        """ID로 사용자 조회 성공 테스트"""
        # Given
        user_id = "user-123"
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = sample_user
        
        # When
        result = auth_service.get_user_by_id(user_id)
        
        # Then
        assert result == sample_user
        auth_service.db.query.assert_called_once()
    
    def test_get_user_by_id_not_found(self, auth_service):
        """존재하지 않는 ID로 사용자 조회 테스트"""
        # Given
        user_id = "nonexistent-id"
        
        # Mock 설정
        auth_service.db.query.return_value.filter.return_value.first.return_value = None
        
        # When
        result = auth_service.get_user_by_id(user_id)
        
        # Then
        assert result is None
    
    def test_update_user_password_success(self, auth_service, sample_user):
        """사용자 비밀번호 업데이트 성공 테스트"""
        # Given
        user_id = "user-123"
        new_password = "newpassword123"
        
        # Mock 설정
        with patch.object(auth_service, 'get_user_by_id', return_value=sample_user):
            
            # When
            result = auth_service.update_user_password(user_id, new_password)
            
            # Then
            assert result is True
            assert sample_user.password_hash != "$5$rounds=535000$test_hash$hashed_password"
            auth_service.db.commit.assert_called_once()
    
    def test_update_user_password_user_not_found(self, auth_service):
        """존재하지 않는 사용자 비밀번호 업데이트 실패 테스트"""
        # Given
        user_id = "nonexistent-id"
        new_password = "newpassword123"
        
        # Mock 설정
        with patch.object(auth_service, 'get_user_by_id', return_value=None):
            
            # When
            result = auth_service.update_user_password(user_id, new_password)
            
            # Then
            assert result is False
    
    def test_update_user_password_database_error(self, auth_service, sample_user):
        """데이터베이스 오류로 비밀번호 업데이트 실패 테스트"""
        # Given
        user_id = "user-123"
        new_password = "newpassword123"
        
        # Mock 설정
        with patch.object(auth_service, 'get_user_by_id', return_value=sample_user):
            auth_service.db.commit.side_effect = Exception("Database error")
            
            # When & Then
            with pytest.raises(ValueError, match="비밀번호 업데이트 중 오류 발생"):
                auth_service.update_user_password(user_id, new_password)
            auth_service.db.rollback.assert_called_once()
    
    def test_deactivate_user_success(self, auth_service, sample_user):
        """사용자 비활성화 성공 테스트"""
        # Given
        user_id = "user-123"
        
        # Mock 설정
        with patch.object(auth_service, 'get_user_by_id', return_value=sample_user):
            
            # When
            result = auth_service.deactivate_user(user_id)
            
            # Then
            assert result is True
            assert sample_user.is_active is False
            auth_service.db.commit.assert_called_once()
    
    def test_deactivate_user_not_found(self, auth_service):
        """존재하지 않는 사용자 비활성화 실패 테스트"""
        # Given
        user_id = "nonexistent-id"
        
        # Mock 설정
        with patch.object(auth_service, 'get_user_by_id', return_value=None):
            
            # When
            result = auth_service.deactivate_user(user_id)
            
            # Then
            assert result is False
    
    def test_activate_user_success(self, auth_service, sample_user):
        """사용자 활성화 성공 테스트"""
        # Given
        user_id = "user-123"
        sample_user.is_active = False
        
        # Mock 설정
        with patch.object(auth_service, 'get_user_by_id', return_value=sample_user):
            
            # When
            result = auth_service.activate_user(user_id)
            
            # Then
            assert result is True
            assert sample_user.is_active is True
            auth_service.db.commit.assert_called_once()
    
    def test_activate_user_not_found(self, auth_service):
        """존재하지 않는 사용자 활성화 실패 테스트"""
        # Given
        user_id = "nonexistent-id"
        
        # Mock 설정
        with patch.object(auth_service, 'get_user_by_id', return_value=None):
            
            # When
            result = auth_service.activate_user(user_id)
            
            # Then
            assert result is False
    
    def test_authenticate_user_database_error(self, auth_service):
        """데이터베이스 오류로 인증 실패 테스트"""
        # Given
        email = "test@example.com"
        password = "testpassword123"
        
        # Mock 설정
        auth_service.db.query.side_effect = Exception("Database error")
        
        # When
        result = auth_service.authenticate_user(email, password)
        
        # Then
        assert result is None
    
    def test_get_user_by_email_database_error(self, auth_service):
        """데이터베이스 오류로 사용자 조회 실패 테스트"""
        # Given
        email = "test@example.com"
        
        # Mock 설정
        auth_service.db.query.side_effect = Exception("Database error")
        
        # When
        result = auth_service.get_user_by_email(email)
        
        # Then
        assert result is None
    
    def test_get_user_by_id_database_error(self, auth_service):
        """데이터베이스 오류로 사용자 ID 조회 실패 테스트"""
        # Given
        user_id = "user-123"
        
        # Mock 설정
        auth_service.db.query.side_effect = Exception("Database error")
        
        # When
        result = auth_service.get_user_by_id(user_id)
        
        # Then
        assert result is None 