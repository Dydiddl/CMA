import { invoke } from '@tauri-apps/api/tauri';
import { getProjects, getProject, createProject, updateProject, deleteProject } from '../services/projectService';
import { Project, ProjectFormData } from '../types';

// Mock Tauri invoke
jest.mock('@tauri-apps/api/tauri', () => ({
  invoke: jest.fn(),
}));

describe('Project Service', () => {
  const mockProject: Project = {
    id: 1,
    name: '테스트 프로젝트',
    description: '테스트 설명',
    status: '진행중',
    startDate: '2024-01-01',
    endDate: '2024-12-31',
    progress: 0,
    manager: '홍길동',
    budget: 1000000,
    location: '서울',
    createdAt: '2024-01-01',
    updatedAt: '2024-01-01',
  };

  const mockProjectFormData: ProjectFormData = {
    name: '테스트 프로젝트',
    description: '테스트 설명',
    status: '진행중',
    startDate: '2024-01-01',
    endDate: '2024-12-31',
    manager: '홍길동',
    budget: 1000000,
    location: '서울',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getProjects', () => {
    it('should fetch all projects successfully', async () => {
      const mockProjects = [mockProject];
      (invoke as jest.Mock).mockResolvedValueOnce(mockProjects);

      const result = await getProjects();

      expect(invoke).toHaveBeenCalledWith('get_projects');
      expect(result).toEqual(mockProjects);
    });

    it('should handle errors when fetching projects', async () => {
      const error = new Error('Failed to fetch projects');
      (invoke as jest.Mock).mockRejectedValueOnce(error);

      await expect(getProjects()).rejects.toThrow('Failed to fetch projects');
    });
  });

  describe('getProject', () => {
    it('should fetch a single project successfully', async () => {
      (invoke as jest.Mock).mockResolvedValueOnce(mockProject);

      const result = await getProject(1);

      expect(invoke).toHaveBeenCalledWith('get_project', { id: 1 });
      expect(result).toEqual(mockProject);
    });

    it('should handle errors when fetching a project', async () => {
      const error = new Error('Failed to fetch project');
      (invoke as jest.Mock).mockRejectedValueOnce(error);

      await expect(getProject(1)).rejects.toThrow('Failed to fetch project');
    });
  });

  describe('createProject', () => {
    it('should create a project successfully', async () => {
      (invoke as jest.Mock).mockResolvedValueOnce(mockProject);

      const result = await createProject(mockProjectFormData);

      expect(invoke).toHaveBeenCalledWith('create_project', { project: mockProjectFormData });
      expect(result).toEqual(mockProject);
    });

    it('should handle errors when creating a project', async () => {
      const error = new Error('Failed to create project');
      (invoke as jest.Mock).mockRejectedValueOnce(error);

      await expect(createProject(mockProjectFormData)).rejects.toThrow('Failed to create project');
    });
  });

  describe('updateProject', () => {
    it('should update a project successfully', async () => {
      const updatedProject = { ...mockProject, name: 'Updated Project' };
      (invoke as jest.Mock).mockResolvedValueOnce(updatedProject);

      const result = await updateProject(1, mockProjectFormData);

      expect(invoke).toHaveBeenCalledWith('update_project', { id: 1, project: mockProjectFormData });
      expect(result).toEqual(updatedProject);
    });

    it('should handle errors when updating a project', async () => {
      const error = new Error('Failed to update project');
      (invoke as jest.Mock).mockRejectedValueOnce(error);

      await expect(updateProject(1, mockProjectFormData)).rejects.toThrow('Failed to update project');
    });
  });

  describe('deleteProject', () => {
    it('should delete a project successfully', async () => {
      (invoke as jest.Mock).mockResolvedValueOnce(undefined);

      await deleteProject(1);

      expect(invoke).toHaveBeenCalledWith('delete_project', { id: 1 });
    });

    it('should handle errors when deleting a project', async () => {
      const error = new Error('Failed to delete project');
      (invoke as jest.Mock).mockRejectedValueOnce(error);

      await expect(deleteProject(1)).rejects.toThrow('Failed to delete project');
    });
  });
}); 