#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사용자 서비스 단위 테스트
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.exc import IntegrityError
from app.services.user import UserService
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import ValidationException


class TestUserService:
    """사용자 서비스 테스트 클래스"""

    @pytest.fixture
    def mock_db(self):
        """Mock 데이터베이스 세션"""
        return Mock()

    @pytest.fixture
    def user_service(self, mock_db):
        """사용자 서비스 인스턴스"""
        return UserService(mock_db)

    @pytest.fixture
    def sample_user_data(self):
        """샘플 사용자 데이터"""
        return {
            "email": "test@example.com",
            "full_name": "테스트 사용자",
            "role": "user",
            "department": "개발팀",
            "phone": "010-1234-5678",
            "is_active": True,
            "password": "testpassword123"
        }

    @pytest.fixture
    def sample_user_model(self):
        """샘플 사용자 모델"""
        user = Mock(spec=User)
        user.id = "user-123"
        user.email = "test@example.com"
        user.full_name = "테스트 사용자"
        user.role = "user"
        user.department = "개발팀"
        user.phone = "010-1234-5678"
        user.is_active = True
        user.password_hash = "hashed_password"
        user.created_at = "2024-01-01T00:00:00"
        user.updated_at = "2024-01-01T00:00:00"
        return user

    def test_get_password_hash_success(self, user_service):
        """비밀번호 해싱 성공 테스트"""
        # Given
        password = "testpassword123"

        # When
        result = user_service.get_password_hash(password)

        # Then
        assert result is not None
        assert result != password
        assert len(result) > 0

    def test_verify_password_success(self, user_service):
        """비밀번호 검증 성공 테스트"""
        # Given
        password = "testpassword123"
        hashed_password = user_service.get_password_hash(password)

        # When
        result = user_service.verify_password(password, hashed_password)

        # Then
        assert result is True

    def test_verify_password_failure(self, user_service):
        """비밀번호 검증 실패 테스트"""
        # Given
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed_password = user_service.get_password_hash(password)

        # When
        result = user_service.verify_password(wrong_password, hashed_password)

        # Then
        assert result is False

    def test_get_users_success(self, user_service, sample_user_model):
        """사용자 목록 조회 성공 테스트"""
        # Given
        users = [sample_user_model]
        total_count = 1

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = users
        mock_query.count.return_value = total_count

        # When
        result, total = user_service.get_users(skip=0, limit=10)

        # Then
        assert len(result) == 1
        assert total == 1
        assert result[0].email == sample_user_model.email

    def test_get_users_with_search(self, user_service, sample_user_model):
        """검색 조건으로 사용자 목록 조회 테스트"""
        # Given
        users = [sample_user_model]
        total_count = 1
        search = "테스트"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = users
        mock_query.count.return_value = total_count

        # When
        result, total = user_service.get_users(skip=0, limit=10, search=search)

        # Then
        assert len(result) == 1
        assert total == 1

    def test_get_users_database_error(self, user_service):
        """데이터베이스 오류로 사용자 목록 조회 실패 테스트"""
        # Given
        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.side_effect = Exception("Database error")

        # When & Then
        with pytest.raises(ValidationException):
            user_service.get_users()

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, user_service, mock_db):
        """사용자 ID로 조회 성공 테스트"""
        # Given
        user_id = "user-test-123"
        mock_user = Mock()
        mock_user.id = "user-test-123"
        mock_user.email = "test@example.com"
        mock_user.password_hash = "hashed_password"
        mock_user.full_name = "테스트 사용자"
        mock_user.role = "user"
        mock_user.department = "개발팀"
        mock_user.phone = "010-1234-5678"
        mock_user.is_active = True
        mock_user.created_at = "2024-01-01T00:00:00"
        mock_user.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # When
        result = await user_service.get_user_by_id(user_id)
        
        # Then
        assert result is not None
        assert result.id == user_id
        assert result.email == "test@example.com"
        assert result.full_name == "테스트 사용자"
        mock_db.query.assert_called_once()

    def test_get_user_by_id_not_found(self, user_service):
        """존재하지 않는 ID로 사용자 조회 실패 테스트"""
        # Given
        user_id = "nonexistent-id"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        # When
        result = user_service.get_user_by_id(user_id)

        # Then
        assert result is None

    def test_get_user_by_id_database_error(self, user_service):
        """데이터베이스 오류로 사용자 조회 실패 테스트"""
        # Given
        user_id = "user-123"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.side_effect = Exception("Database error")

        # When & Then
        with pytest.raises(ValidationException):
            user_service.get_user_by_id(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(self, user_service, mock_db):
        """이메일로 사용자 조회 성공 테스트"""
        # Given
        email = "test@example.com"
        mock_user = Mock()
        mock_user.id = "user-test-123"
        mock_user.email = "test@example.com"
        mock_user.password_hash = "hashed_password"
        mock_user.full_name = "테스트 사용자"
        mock_user.role = "user"
        mock_user.department = "개발팀"
        mock_user.phone = "010-1234-5678"
        mock_user.is_active = True
        mock_user.created_at = "2024-01-01T00:00:00"
        mock_user.updated_at = "2024-01-01T00:00:00"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # When
        result = await user_service.get_user_by_email(email)
        
        # Then
        assert result is not None
        assert result.email == email
        assert result.full_name == "테스트 사용자"
        mock_db.query.assert_called_once()

    def test_get_user_by_email_not_found(self, user_service):
        """존재하지 않는 이메일로 사용자 조회 실패 테스트"""
        # Given
        email = "nonexistent@example.com"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        # When
        result = user_service.get_user_by_email(email)

        # Then
        assert result is None

    def test_create_user_success(self, user_service, sample_user_data):
        """사용자 생성 성공 테스트"""
        # Given
        user_data = UserCreate(**sample_user_data)

        # Mock 설정
        with patch.object(user_service, 'get_user_by_email', return_value=None):
            user_service.db.add.return_value = None
            user_service.db.commit.return_value = None

            # refresh 시뮬레이션 개선
            def mock_refresh(user):
                user.id = "user-123"
                user.email = user_data.email
                user.full_name = user_data.full_name
                user.role = user_data.role
                user.department = user_data.department
                user.phone = user_data.phone
                user.is_active = user_data.is_active
                user.password_hash = "hashed_password"
                user.created_at = "2024-01-01T00:00:00"
                user.updated_at = "2024-01-01T00:00:00"

            user_service.db.refresh.side_effect = mock_refresh

            # When
            result = user_service.create_user(user_data)

            # Then
            assert result is not None
            assert result.email == user_data.email
            assert result.full_name == user_data.full_name
            assert result.id == "user-123"
            user_service.db.add.assert_called_once()
            user_service.db.commit.assert_called_once()

    def test_create_user_duplicate_email(self, user_service, sample_user_data):
        """중복 이메일로 사용자 생성 실패 테스트"""
        # Given
        user_data = UserCreate(**sample_user_data)
        existing_user = Mock()

        # Mock 설정
        with patch.object(user_service, 'get_user_by_email', return_value=existing_user):

            # When & Then
            with pytest.raises(ValidationException, match="이미 존재하는 이메일입니다"):
                user_service.create_user(user_data)

    def test_create_user_database_error(self, user_service, sample_user_data):
        """데이터베이스 오류로 사용자 생성 실패 테스트"""
        # Given
        user_data = UserCreate(**sample_user_data)

        # Mock 설정
        with patch.object(user_service, 'get_user_by_email', return_value=None):
            user_service.db.add.side_effect = IntegrityError("", "", "")

            # When & Then
            with pytest.raises(ValidationException, match="이미 존재하는 이메일입니다"):
                user_service.create_user(user_data)
            user_service.db.rollback.assert_called_once()

    def test_update_user_success(self, user_service, sample_user_model):
        """사용자 정보 업데이트 성공 테스트"""
        # Given
        user_id = "user-123"
        update_data = UserUpdate(full_name="업데이트된 이름")

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_user_model
        user_service.db.commit.return_value = None

        # When
        result = user_service.update_user(user_id, update_data)

        # Then
        assert result is not None
        assert result.full_name == "업데이트된 이름"
        user_service.db.commit.assert_called_once()

    def test_update_user_not_found(self, user_service):
        """존재하지 않는 사용자 업데이트 실패 테스트"""
        # Given
        user_id = "nonexistent-id"
        update_data = UserUpdate(full_name="업데이트된 이름")

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        # When
        result = user_service.update_user(user_id, update_data)

        # Then
        assert result is None

    def test_delete_user_success(self, user_service, sample_user_model):
        """사용자 삭제 성공 테스트"""
        # Given
        user_id = "user-123"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_user_model
        user_service.db.delete.return_value = None
        user_service.db.commit.return_value = None

        # When
        result = user_service.delete_user(user_id)

        # Then
        assert result is True
        user_service.db.delete.assert_called_once_with(sample_user_model)
        user_service.db.commit.assert_called_once()

    def test_delete_user_not_found(self, user_service):
        """존재하지 않는 사용자 삭제 실패 테스트"""
        # Given
        user_id = "nonexistent-id"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        # When
        result = user_service.delete_user(user_id)

        # Then
        assert result is False

    def test_activate_user_success(self, user_service, sample_user_model):
        """사용자 활성화 성공 테스트"""
        # Given
        user_id = "user-123"
        sample_user_model.is_active = False

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_user_model
        user_service.db.commit.return_value = None

        # When
        result = user_service.activate_user(user_id)

        # Then
        assert result is True
        assert sample_user_model.is_active is True
        user_service.db.commit.assert_called_once()

    def test_activate_user_not_found(self, user_service):
        """존재하지 않는 사용자 활성화 실패 테스트"""
        # Given
        user_id = "nonexistent-id"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        # When
        result = user_service.activate_user(user_id)

        # Then
        assert result is False

    def test_deactivate_user_success(self, user_service, sample_user_model):
        """사용자 비활성화 성공 테스트"""
        # Given
        user_id = "user-123"
        sample_user_model.is_active = True

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_user_model
        user_service.db.commit.return_value = None

        # When
        result = user_service.deactivate_user(user_id)

        # Then
        assert result is True
        assert sample_user_model.is_active is False
        user_service.db.commit.assert_called_once()

    def test_deactivate_user_not_found(self, user_service):
        """존재하지 않는 사용자 비활성화 실패 테스트"""
        # Given
        user_id = "nonexistent-id"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        # When
        result = user_service.deactivate_user(user_id)

        # Then
        assert result is False

    def test_update_user_password_success(self, user_service, sample_user_model):
        """사용자 비밀번호 업데이트 성공 테스트"""
        # Given
        user_id = "user-123"
        current_password = "oldpassword"
        new_password = "newpassword123"

        # Mock 설정
        with patch.object(user_service, 'verify_password', return_value=True):
            mock_query = Mock()
            user_service.db.query.return_value = mock_query
            mock_query.filter.return_value = mock_query
            mock_query.first.return_value = sample_user_model
            user_service.db.commit.return_value = None

            # When
            result = user_service.update_user_password(
                user_id, current_password, new_password
            )

            # Then
            assert result is True
            user_service.db.commit.assert_called_once()

    def test_update_user_password_wrong_current_password(self, user_service, sample_user_model):
        """잘못된 현재 비밀번호로 업데이트 실패 테스트"""
        # Given
        user_id = "user-123"
        current_password = "wrongpassword"
        new_password = "newpassword123"

        # Mock 설정
        with patch.object(user_service, 'verify_password', return_value=False):
            mock_query = Mock()
            user_service.db.query.return_value = mock_query
            mock_query.filter.return_value = mock_query
            mock_query.first.return_value = sample_user_model

            # When & Then
            with pytest.raises(ValidationException, match="현재 비밀번호가 올바르지 않습니다"):
                user_service.update_user_password(user_id, current_password, new_password)

    def test_update_user_password_user_not_found(self, user_service):
        """존재하지 않는 사용자 비밀번호 업데이트 실패 테스트"""
        # Given
        user_id = "nonexistent-id"
        current_password = "oldpassword"
        new_password = "newpassword123"

        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        # When & Then
        with pytest.raises(ValidationException, match="사용자를 찾을 수 없습니다"):
            user_service.update_user_password(user_id, current_password, new_password)

    def test_get_user_stats_success(self, user_service):
        """사용자 통계 조회 성공 테스트"""
        # Given
        # Mock 설정
        mock_query = Mock()
        user_service.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 10
        mock_query.with_entities.return_value.scalar.return_value = 5

        # When
        stats = user_service.get_user_stats()

        # Then
        assert "total_users" in stats
        assert "active_users" in stats
        assert stats["total_users"] == 10
        assert stats["active_users"] == 5 