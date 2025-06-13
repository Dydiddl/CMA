import { useState, useCallback } from 'react';
import { Project } from '../types';
import { apiService } from '../services/api';

export const useProjects = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiService.projects.getAll();
      setProjects(response.data);
      setError(null);
    } catch (err) {
      setError('프로젝트 목록을 불러오는데 실패했습니다');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  const createProject = useCallback(async (projectData: Omit<Project, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      setLoading(true);
      const response = await apiService.projects.create(projectData);
      setProjects(prev => [...prev, response.data]);
      setError(null);
      return response.data;
    } catch (err) {
      setError('프로젝트 생성에 실패했습니다');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateProject = useCallback(async (id: number, projectData: Partial<Project>) => {
    try {
      setLoading(true);
      const response = await apiService.projects.update(id, projectData);
      setProjects(prev => prev.map(p => p.id === id ? response.data : p));
      setError(null);
      return response.data;
    } catch (err) {
      setError('프로젝트 수정에 실패했습니다');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteProject = useCallback(async (id: number) => {
    try {
      setLoading(true);
      await apiService.projects.delete(id);
      setProjects(prev => prev.filter(p => p.id !== id));
      setError(null);
    } catch (err) {
      setError('프로젝트 삭제에 실패했습니다');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    projects,
    loading,
    error,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject
  };
}; 