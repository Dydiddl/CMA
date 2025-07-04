import pytest
from unittest.mock import Mock
from app.services.project import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.core.exceptions import NotFoundException as ProjectNotFoundException


class TestProjectService:
    """프로젝트 서비스 테스트"""

    @pytest.fixture
    def mock_db(self):
        return Mock()

    @pytest.fixture
    def project_service(self, mock_db):
        return ProjectService(mock_db)

    @pytest.fixture
    def sample_project_data(self):
        return {
            "name": "테스트 프로젝트",
            "description": "테스트 프로젝트 설명",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "budget": 10000000,
            "status": "in_progress",
            "project_number": "PRJ-2024-001"
        }

    def test_create_project_success(self, project_service, mock_db, sample_project_data):
        """프로젝트 생성 성공 테스트"""
        # Given
        project_create = ProjectCreate(**sample_project_data)
        mock_project = Mock()
        mock_project.id = "test-project-id"
        mock_project.name = sample_project_data["name"]
        mock_project.status = sample_project_data["status"]
        mock_project.created_at = "2024-01-01T00:00:00"
        mock_project.updated_at = "2024-01-01T00:00:00"
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        # When
        result = project_service.create_project(project_create)

        # Then
        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_get_projects_success(self, project_service, mock_db):
        """프로젝트 목록 조회 성공 테스트"""
        # Given
        mock_project1 = Mock()
        mock_project1.id = "id1"
        mock_project1.name = "프로젝트1"
        mock_project1.status = "in_progress"
        mock_project1.created_at = "2024-01-01T00:00:00"
        mock_project1.updated_at = "2024-01-01T00:00:00"
        mock_project2 = Mock()
        mock_project2.id = "id2"
        mock_project2.name = "프로젝트2"
        mock_project2.status = "completed"
        mock_project2.created_at = "2024-01-01T00:00:00"
        mock_project2.updated_at = "2024-01-01T00:00:00"
        mock_projects = [mock_project1, mock_project2]
        mock_db.query.return_value.filter.return_value.offset.return_value.\
            limit.return_value.all.return_value = mock_projects
        mock_db.query.return_value.filter.return_value.count.return_value = 2

        # When
        projects, total = project_service.get_projects(skip=0, limit=10)

        # Then
        assert len(projects) == 2
        assert total == 2
        mock_db.query.assert_called()

    def test_get_project_by_id_success(self, project_service, mock_db):
        """프로젝트 ID로 조회 성공 테스트"""
        # Given
        project_id = "test-project-id"
        mock_project = Mock()
        mock_project.id = project_id
        mock_project.name = "테스트 프로젝트"
        mock_project.status = "in_progress"
        mock_project.created_at = "2024-01-01T00:00:00"
        mock_project.updated_at = "2024-01-01T00:00:00"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_project

        # When
        result = project_service.get_project_by_id(project_id)

        # Then
        assert result is not None
        assert result.id == project_id

    def test_get_project_by_id_not_found(self, project_service, mock_db):
        """존재하지 않는 프로젝트 조회 테스트"""
        # Given
        project_id = "non-existent-id"
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # When & Then
        with pytest.raises(ProjectNotFoundException):
            project_service.get_project_by_id(project_id)

    def test_update_project_success(self, project_service, mock_db):
        """프로젝트 수정 성공 테스트"""
        # Given
        project_id = "test-project-id"
        mock_project = Mock()
        mock_project.id = project_id
        mock_project.name = "수정 전 프로젝트명"
        mock_project.status = "in_progress"
        mock_project.created_at = "2024-01-01T00:00:00"
        mock_project.updated_at = "2024-01-01T00:00:00"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_project
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        update_data = ProjectUpdate(name="수정된 프로젝트명")

        # When
        result = project_service.update_project(project_id, update_data)

        # Then
        assert result is not None
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_update_project_not_found(self, project_service, mock_db):
        """존재하지 않는 프로젝트 수정 테스트"""
        # Given
        project_id = "non-existent-id"
        mock_db.query.return_value.filter.return_value.first.return_value = None

        update_data = ProjectUpdate(name="수정된 프로젝트명")

        # When & Then
        with pytest.raises(ProjectNotFoundException):
            project_service.update_project(project_id, update_data)

    def test_delete_project_success(self, project_service, mock_db):
        """프로젝트 삭제 성공 테스트"""
        # Given
        project_id = "test-project-id"
        mock_project = Mock()
        mock_project.id = project_id
        mock_project.name = "삭제할 프로젝트"
        mock_project.status = "in_progress"
        mock_project.created_at = "2024-01-01T00:00:00"
        mock_project.updated_at = "2024-01-01T00:00:00"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_project
        mock_db.delete.return_value = None
        mock_db.commit.return_value = None

        # When
        result = project_service.delete_project(project_id)

        # Then
        assert result is True
        mock_db.delete.assert_called_once_with(mock_project)
        mock_db.commit.assert_called_once()

    def test_search_projects_by_name(self, project_service, mock_db):
        """프로젝트명으로 검색 테스트"""
        # Given
        search_term = "테스트"
        mock_projects = [Mock(), Mock()]
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_projects
        mock_db.query.return_value.filter.return_value.count.return_value = 2
        
        # When
        projects, total = project_service.get_projects(search=search_term)
        
        # Then
        assert len(projects) == 2
        assert total == 2
        mock_db.query.assert_called()
    
    def test_filter_projects_by_status(self, project_service, mock_db):
        """프로젝트 상태로 필터링 테스트"""
        # Given
        status = "진행중"
        mock_projects = [Mock()]
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_projects
        mock_db.query.return_value.filter.return_value.count.return_value = 1
        
        # When
        projects, total = project_service.get_projects(status=status)
        
        # Then
        assert len(projects) == 1
        assert total == 1
        mock_db.query.assert_called()
    
    def test_get_project_statistics(self, project_service, mock_db):
        """프로젝트 통계 조회 테스트"""
        # Given
        mock_db.query.return_value.filter.return_value.count.return_value = 5
        mock_db.query.return_value.with_entities.return_value.scalar.return_value = 50000000
        
        # When
        stats = project_service.get_project_statistics()
        
        # Then
        assert "total_projects" in stats
        assert "total_budget" in stats
        assert stats["total_projects"] == 5
        assert stats["total_budget"] == 50000000 