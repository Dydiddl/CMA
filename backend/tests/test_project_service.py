#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
프로젝트 서비스 테스트
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.services.project import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectDocumentCreate
from app.models.project import Project, ProjectDocument, ProjectStatus, ProjectType
from app.core.exceptions import NotFoundException, ValidationException

class TestProjectService:
    """프로젝트 서비스 테스트"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def project_service(self, mock_db):
        return ProjectService(mock_db)
    
    @pytest.fixture
    def sample_project_data(self):
        return ProjectCreate(
            name="테스트 프로젝트",
            project_number="PRJ-2024-001",
            description="테스트용 프로젝트입니다.",
            project_type=ProjectType.RESIDENTIAL,
            status=ProjectStatus.PLANNING,
            location="서울시 강남구",
            address="서울시 강남구 테헤란로 123",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=365),
            total_budget=100000000,
            project_manager="김매니저",
            client_name="테스트 발주처",
            client_contact="010-1234-5678"
        )
    
    def test_create_project_success(self, project_service, mock_db, sample_project_data):
        """프로젝트 생성 성공 테스트"""
        # Given
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_project = Mock(spec=Project)
        mock_project.project_number = sample_project_data.project_number
        
        # When
        with patch.object(Project, '__init__', return_value=None):
            with patch.object(Project, '__dict__', {'project_number': sample_project_data.project_number}):
                result = project_service.create_project(sample_project_data)
        
        # Then
        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_create_project_duplicate_number(self, project_service, mock_db, sample_project_data):
        """중복 프로젝트 번호 테스트"""
        # Given
        existing_project = Mock(spec=Project)
        mock_db.query.return_value.filter.return_value.first.return_value = existing_project
        
        # When & Then
        with pytest.raises(ValidationException, match="이미 존재하는 프로젝트 번호입니다"):
            project_service.create_project(sample_project_data)
    
    def test_get_projects_success(self, project_service, mock_db):
        """프로젝트 목록 조회 성공 테스트"""
        # Given
        mock_projects = [Mock(spec=Project) for _ in range(3)]
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 3
        mock_query.offset.return_value.limit.return_value.all.return_value = mock_projects
        mock_db.query.return_value = mock_query
        
        # When
        projects, total = project_service.get_projects(skip=0, limit=10)
        
        # Then
        assert len(projects) == 3
        assert total == 3
    
    def test_get_projects_with_search(self, project_service, mock_db):
        """검색 조건이 있는 프로젝트 목록 조회 테스트"""
        # Given
        mock_projects = [Mock(spec=Project)]
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.offset.return_value.limit.return_value.all.return_value = mock_projects
        mock_db.query.return_value = mock_query
        
        # When
        projects, total = project_service.get_projects(search="테스트")
        
        # Then
        assert len(projects) == 1
        assert total == 1
    
    def test_get_project_by_id_success(self, project_service, mock_db):
        """프로젝트 ID로 조회 성공 테스트"""
        # Given
        mock_project = Mock(spec=Project)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_project
        
        # When
        result = project_service.get_project_by_id("test-id")
        
        # Then
        assert result == mock_project
    
    def test_get_project_by_id_not_found(self, project_service, mock_db):
        """프로젝트 ID로 조회 실패 테스트"""
        # Given
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # When
        result = project_service.get_project_by_id("non-existent-id")
        
        # Then
        assert result is None
    
    def test_update_project_success(self, project_service, mock_db):
        """프로젝트 수정 성공 테스트"""
        # Given
        mock_project = Mock(spec=Project)
        mock_project.id = "test-id"
        mock_project.project_number = "PRJ-2024-001"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_project
        
        update_data = ProjectUpdate(name="수정된 프로젝트명")
        
        # When
        result = project_service.update_project("test-id", update_data)
        
        # Then
        assert result == mock_project
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_update_project_not_found(self, project_service, mock_db):
        """프로젝트 수정 실패 테스트"""
        # Given
        mock_db.query.return_value.filter.return_value.first.return_value = None
        update_data = ProjectUpdate(name="수정된 프로젝트명")
        
        # When
        result = project_service.update_project("non-existent-id", update_data)
        
        # Then
        assert result is None
    
    def test_delete_project_success(self, project_service, mock_db):
        """프로젝트 삭제 성공 테스트"""
        # Given
        mock_project = Mock(spec=Project)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_project
        
        # When
        result = project_service.delete_project("test-id")
        
        # Then
        assert result is True
        mock_db.delete.assert_called_once_with(mock_project)
        mock_db.commit.assert_called_once()
    
    def test_delete_project_not_found(self, project_service, mock_db):
        """프로젝트 삭제 실패 테스트"""
        # Given
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # When
        result = project_service.delete_project("non-existent-id")
        
        # Then
        assert result is False
    
    def test_get_project_statistics(self, project_service, mock_db):
        """프로젝트 통계 조회 테스트"""
        # Given
        mock_query = Mock()
        mock_query.count.return_value = 5
        mock_query.filter.return_value.count.return_value = 3
        mock_db.query.return_value = mock_query
        
        # When
        result = project_service.get_project_statistics()
        
        # Then
        assert "total_projects" in result
        assert "active_projects" in result
        assert "completed_projects" in result
        assert "total_budget" in result
        assert "total_spent" in result
        assert "average_progress" in result
        assert "projects_by_status" in result
        assert "projects_by_type" in result
    
    def test_create_project_document_success(self, project_service, mock_db):
        """프로젝트 문서 생성 성공 테스트"""
        # Given
        mock_project = Mock(spec=Project)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_project
        
        document_data = ProjectDocumentCreate(
            title="테스트 문서",
            file_name="test.pdf",
            file_path="/uploads/test.pdf",
            project_id="test-project-id"
        )
        
        # When
        with patch.object(ProjectDocument, '__init__', return_value=None):
            result = project_service.create_project_document(document_data)
        
        # Then
        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_create_project_document_project_not_found(self, project_service, mock_db):
        """프로젝트 문서 생성 실패 테스트 (프로젝트 없음)"""
        # Given
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        document_data = ProjectDocumentCreate(
            title="테스트 문서",
            file_name="test.pdf",
            file_path="/uploads/test.pdf",
            project_id="non-existent-project-id"
        )
        
        # When & Then
        with pytest.raises(NotFoundException, match="프로젝트를 찾을 수 없습니다"):
            project_service.create_project_document(document_data)
    
    def test_get_projects_by_vendor(self, project_service, mock_db):
        """거래처별 프로젝트 조회 테스트"""
        # Given
        mock_projects = [Mock(spec=Project) for _ in range(2)]
        mock_db.query.return_value.filter.return_value.all.return_value = mock_projects
        
        # When
        result = project_service.get_projects_by_vendor("test-vendor-id")
        
        # Then
        assert len(result) == 2
    
    def test_get_projects_by_date_range(self, project_service, mock_db):
        """기간별 프로젝트 조회 테스트"""
        # Given
        mock_projects = [Mock(spec=Project) for _ in range(3)]
        mock_db.query.return_value.filter.return_value.all.return_value = mock_projects
        
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=30)
        
        # When
        result = project_service.get_projects_by_date_range(start_date, end_date)
        
        # Then
        assert len(result) == 3 