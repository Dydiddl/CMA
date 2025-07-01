#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
프로젝트 API 테스트
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from app.main import app
from app.schemas.project import ProjectStatus, ProjectType

client = TestClient(app)

class TestProjectAPI:
    """프로젝트 API 테스트"""
    
    @pytest.fixture
    def sample_project_data(self):
        return {
            "name": "테스트 프로젝트",
            "project_number": "PRJ-2024-001",
            "description": "테스트용 프로젝트입니다.",
            "project_type": ProjectType.RESIDENTIAL.value,
            "status": ProjectStatus.PLANNING.value,
            "location": "서울시 강남구",
            "address": "서울시 강남구 테헤란로 123",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "total_budget": 100000000,
            "project_manager": "김매니저",
            "client_name": "테스트 발주처",
            "client_contact": "010-1234-5678"
        }
    
    @pytest.fixture
    def mock_current_user(self):
        return Mock(id="test-user-id", email="test@example.com")
    
    def test_create_project_success(self, sample_project_data, mock_current_user):
        """프로젝트 생성 성공 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.create_project") as mock_create:
                mock_project = Mock()
                mock_project.id = "test-project-id"
                mock_project.name = sample_project_data["name"]
                mock_project.project_number = sample_project_data["project_number"]
                mock_project.calculate_progress.return_value = 0.0
                mock_project.calculate_budget_usage.return_value = 0.0
                mock_create.return_value = mock_project
                
                response = client.post("/api/v1/projects/", json=sample_project_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["name"] == sample_project_data["name"]
                assert data["project_number"] == sample_project_data["project_number"]
    
    def test_create_project_duplicate_number(self, sample_project_data, mock_current_user):
        """중복 프로젝트 번호 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.create_project") as mock_create:
                mock_create.side_effect = ValueError("이미 존재하는 프로젝트 번호입니다.")
                
                response = client.post("/api/v1/projects/", json=sample_project_data)
                
                assert response.status_code == 400
                assert "이미 존재하는 프로젝트 번호입니다" in response.json()["detail"]
    
    def test_get_projects_success(self, mock_current_user):
        """프로젝트 목록 조회 성공 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.get_projects") as mock_get:
                mock_projects = []
                for i in range(3):
                    mock_project = Mock()
                    mock_project.id = f"project-{i}"
                    mock_project.name = f"프로젝트 {i}"
                    mock_project.calculate_progress.return_value = 25.0 * (i + 1)
                    mock_project.calculate_budget_usage.return_value = 10.0 * (i + 1)
                    mock_projects.append(mock_project)
                
                mock_get.return_value = (mock_projects, 3)
                
                response = client.get("/api/v1/projects/")
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert data["total"] == 3
                assert len(data["data"]) == 3
    
    def test_get_projects_with_filters(self, mock_current_user):
        """필터가 있는 프로젝트 목록 조회 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.get_projects") as mock_get:
                mock_projects = []
                mock_project = Mock()
                mock_project.id = "project-1"
                mock_project.name = "테스트 프로젝트"
                mock_project.calculate_progress.return_value = 50.0
                mock_project.calculate_budget_usage.return_value = 30.0
                mock_projects.append(mock_project)
                
                mock_get.return_value = (mock_projects, 1)
                
                response = client.get("/api/v1/projects/?search=테스트&status=in_progress")
                
                assert response.status_code == 200
                data = response.json()
                assert data["total"] == 1
                assert len(data["data"]) == 1
    
    def test_get_project_success(self, mock_current_user):
        """프로젝트 상세 조회 성공 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.get_project_by_id") as mock_get:
                mock_project = Mock()
                mock_project.id = "test-project-id"
                mock_project.name = "테스트 프로젝트"
                mock_project.calculate_progress.return_value = 75.0
                mock_project.calculate_budget_usage.return_value = 60.0
                mock_get.return_value = mock_project
                
                response = client.get("/api/v1/projects/test-project-id")
                
                assert response.status_code == 200
                data = response.json()
                assert data["name"] == "테스트 프로젝트"
    
    def test_get_project_not_found(self, mock_current_user):
        """프로젝트 상세 조회 실패 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.get_project_by_id", return_value=None):
                response = client.get("/api/v1/projects/non-existent-id")
                
                assert response.status_code == 404
                assert "프로젝트를 찾을 수 없습니다" in response.json()["detail"]
    
    def test_update_project_success(self, mock_current_user):
        """프로젝트 수정 성공 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.update_project") as mock_update:
                mock_project = Mock()
                mock_project.id = "test-project-id"
                mock_project.name = "수정된 프로젝트"
                mock_project.calculate_progress.return_value = 80.0
                mock_project.calculate_budget_usage.return_value = 70.0
                mock_update.return_value = mock_project
                
                update_data = {"name": "수정된 프로젝트"}
                response = client.put("/api/v1/projects/test-project-id", json=update_data)
                
                assert response.status_code == 200
                data = response.json()
                assert data["name"] == "수정된 프로젝트"
    
    def test_update_project_not_found(self, mock_current_user):
        """프로젝트 수정 실패 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.update_project", return_value=None):
                update_data = {"name": "수정된 프로젝트"}
                response = client.put("/api/v1/projects/non-existent-id", json=update_data)
                
                assert response.status_code == 404
                assert "프로젝트를 찾을 수 없습니다" in response.json()["detail"]
    
    def test_delete_project_success(self, mock_current_user):
        """프로젝트 삭제 성공 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.delete_project", return_value=True):
                response = client.delete("/api/v1/projects/test-project-id")
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert "성공적으로 삭제되었습니다" in data["message"]
    
    def test_delete_project_not_found(self, mock_current_user):
        """프로젝트 삭제 실패 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.delete_project", return_value=False):
                response = client.delete("/api/v1/projects/non-existent-id")
                
                assert response.status_code == 404
                assert "프로젝트를 찾을 수 없습니다" in response.json()["detail"]
    
    def test_get_project_statistics(self, mock_current_user):
        """프로젝트 통계 조회 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.get_project_statistics") as mock_stats:
                mock_stats.return_value = {
                    "total_projects": 10,
                    "active_projects": 5,
                    "completed_projects": 3,
                    "total_budget": 1000000000,
                    "total_spent": 500000000,
                    "average_progress": 65.5,
                    "projects_by_status": {"planning": 2, "in_progress": 5, "completed": 3},
                    "projects_by_type": {"residential": 6, "commercial": 4}
                }
                
                response = client.get("/api/v1/projects/statistics/overview")
                
                assert response.status_code == 200
                data = response.json()
                assert data["total_projects"] == 10
                assert data["active_projects"] == 5
                assert data["completed_projects"] == 3
                assert data["total_budget"] == 1000000000
                assert data["total_spent"] == 500000000
                assert data["average_progress"] == 65.5
    
    def test_create_project_document_success(self, mock_current_user):
        """프로젝트 문서 생성 성공 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.create_project_document") as mock_create:
                mock_document = Mock()
                mock_document.id = "doc-1"
                mock_document.title = "테스트 문서"
                mock_document.file_name = "test.pdf"
                mock_create.return_value = mock_document
                
                document_data = {
                    "title": "테스트 문서",
                    "file_name": "test.pdf",
                    "file_path": "/uploads/test.pdf",
                    "project_id": "test-project-id"
                }
                
                response = client.post("/api/v1/projects/test-project-id/documents", json=document_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["title"] == "테스트 문서"
                assert data["file_name"] == "test.pdf"
    
    def test_get_project_documents_success(self, mock_current_user):
        """프로젝트 문서 목록 조회 성공 테스트"""
        with patch("app.api.v1.endpoints.projects.get_current_user", return_value=mock_current_user):
            with patch("app.services.project.ProjectService.get_project_documents") as mock_get:
                mock_documents = []
                for i in range(2):
                    mock_doc = Mock()
                    mock_doc.id = f"doc-{i}"
                    mock_doc.title = f"문서 {i}"
                    mock_documents.append(mock_doc)
                
                mock_get.return_value = (mock_documents, 2)
                
                response = client.get("/api/v1/projects/test-project-id/documents")
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert data["total"] == 2
                assert len(data["data"]) == 2 