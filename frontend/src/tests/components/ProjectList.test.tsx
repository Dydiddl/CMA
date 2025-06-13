import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ProjectProvider } from '../../contexts/ProjectContext';
import ProjectList from '../../pages/ProjectList';
import * as projectService from '../../services/projectService';

// Mock project service
jest.mock('../../services/projectService');

describe('ProjectList Component', () => {
  const mockProjects = [
    {
      id: 1,
      name: '테스트 프로젝트 1',
      description: '테스트 설명 1',
      status: '진행중' as const,
      startDate: '2024-01-01',
      endDate: '2024-12-31',
      progress: 0,
      manager: '홍길동',
      budget: 1000000,
      location: '서울',
      createdAt: '2024-01-01',
      updatedAt: '2024-01-01',
    },
    {
      id: 2,
      name: '테스트 프로젝트 2',
      description: '테스트 설명 2',
      status: '완료' as const,
      startDate: '2024-01-01',
      endDate: '2024-12-31',
      progress: 100,
      manager: '김철수',
      budget: 2000000,
      location: '부산',
      createdAt: '2024-01-01',
      updatedAt: '2024-01-01',
    },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    (projectService.getProjects as jest.Mock).mockResolvedValue(mockProjects);
  });

  const renderComponent = () => {
    return render(
      <BrowserRouter>
        <ProjectProvider>
          <ProjectList />
        </ProjectProvider>
      </BrowserRouter>
    );
  };

  it('should render project list correctly', async () => {
    renderComponent();

    // Loading state
    expect(screen.getByText('프로젝트 목록을 불러오는 중...')).toBeInTheDocument();

    // Wait for projects to load
    await waitFor(() => {
      expect(screen.getByText('테스트 프로젝트 1')).toBeInTheDocument();
      expect(screen.getByText('테스트 프로젝트 2')).toBeInTheDocument();
    });

    // Check project details
    expect(screen.getByText('진행중')).toBeInTheDocument();
    expect(screen.getByText('완료')).toBeInTheDocument();
    expect(screen.getByText('홍길동')).toBeInTheDocument();
    expect(screen.getByText('김철수')).toBeInTheDocument();
  });

  it('should handle search functionality', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('테스트 프로젝트 1')).toBeInTheDocument();
    });

    const searchInput = screen.getByPlaceholderText('프로젝트 검색...');
    fireEvent.change(searchInput, { target: { value: '프로젝트 1' } });

    expect(screen.getByText('테스트 프로젝트 1')).toBeInTheDocument();
    expect(screen.queryByText('테스트 프로젝트 2')).not.toBeInTheDocument();
  });

  it('should handle error state', async () => {
    const error = new Error('Failed to fetch projects');
    (projectService.getProjects as jest.Mock).mockRejectedValueOnce(error);

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('프로젝트 목록을 불러오는데 실패했습니다')).toBeInTheDocument();
    });
  });

  it('should navigate to project detail page when clicking on a project', async () => {
    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('테스트 프로젝트 1')).toBeInTheDocument();
    });

    const projectCard = screen.getByText('테스트 프로젝트 1').closest('div');
    fireEvent.click(projectCard!);

    // Check if navigation occurred
    expect(window.location.pathname).toBe('/projects/1');
  });
}); 