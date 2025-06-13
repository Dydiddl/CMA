import { useState, useCallback } from 'react';
import { Task } from '../types';
import { apiService } from '../services/api';

export const useTasks = (projectId: number) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiService.tasks.getAll(projectId);
      setTasks(response.data);
      setError(null);
    } catch (err) {
      setError('태스크 목록을 불러오는데 실패했습니다');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  const createTask = useCallback(async (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      setLoading(true);
      const response = await apiService.tasks.create(taskData);
      setTasks(prev => [...prev, response.data]);
      setError(null);
      return response.data;
    } catch (err) {
      setError('태스크 생성에 실패했습니다');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateTask = useCallback(async (id: number, taskData: Partial<Task>) => {
    try {
      setLoading(true);
      const response = await apiService.tasks.update(id, taskData);
      setTasks(prev => prev.map(t => t.id === id ? response.data : t));
      setError(null);
      return response.data;
    } catch (err) {
      setError('태스크 수정에 실패했습니다');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteTask = useCallback(async (id: number) => {
    try {
      setLoading(true);
      await apiService.tasks.delete(id);
      setTasks(prev => prev.filter(t => t.id !== id));
      setError(null);
    } catch (err) {
      setError('태스크 삭제에 실패했습니다');
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask
  };
}; 