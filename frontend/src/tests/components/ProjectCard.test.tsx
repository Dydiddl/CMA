import { render, screen } from '@testing-library/react';
import { ProjectCard } from '../../components/project/ProjectCard';

const mockProject = {
  id: 1,
  name: '테스트 프로젝트',
  description: '테스트 설명',
  status: 'IN_PROGRESS',
  startDate: '2024-01-01',
  endDate: '2024-12-31',
  progress: 50,
  createdAt: '2024-01-01T00:00:00Z',
  updatedAt: '2024-01-01T00:00:00Z',
};

describe('ProjectCard', () => {
  it('프로젝트 정보를 올바르게 렌더링한다', () => {
    render(<ProjectCard project={mockProject} />);

    expect(screen.getByText('테스트 프로젝트')).toBeInTheDocument();
    expect(screen.getByText('테스트 설명')).toBeInTheDocument();
    expect(screen.getByText('진행중')).toBeInTheDocument();
    expect(screen.getByText('50%')).toBeInTheDocument();
  });

  it('진행률이 0일 때 올바르게 표시된다', () => {
    const projectWithZeroProgress = {
      ...mockProject,
      progress: 0,
    };

    render(<ProjectCard project={projectWithZeroProgress} />);
    expect(screen.getByText('0%')).toBeInTheDocument();
  });

  it('진행률이 100일 때 올바르게 표시된다', () => {
    const projectWithFullProgress = {
      ...mockProject,
      progress: 100,
    };

    render(<ProjectCard project={projectWithFullProgress} />);
    expect(screen.getByText('100%')).toBeInTheDocument();
  });
}); 