import { invoke } from '@tauri-apps/api/tauri';
import { Task, TaskFormData } from '../types/task';

export const getTasks = async (projectId?: number): Promise<Task[]> => {
  try {
    const params = projectId ? { projectId } : {};
    return await invoke<Task[]>('get_tasks', params);
  } catch (error) {
    console.error('Failed to fetch tasks:', error);
    throw error;
  }
};

export const getTask = async (id: number): Promise<Task> => {
  try {
    return await invoke<Task>('get_task', { id });
  } catch (error) {
    console.error('Failed to fetch task:', error);
    throw error;
  }
};

export const createTask = async (taskData: TaskFormData): Promise<Task> => {
  try {
    return await invoke<Task>('create_task', { taskData });
  } catch (error) {
    console.error('Failed to create task:', error);
    throw error;
  }
};

export const updateTask = async (id: number, taskData: TaskFormData): Promise<Task> => {
  try {
    return await invoke<Task>('update_task', { id, taskData });
  } catch (error) {
    console.error('Failed to update task:', error);
    throw error;
  }
};

export const deleteTask = async (id: number): Promise<void> => {
  try {
    await invoke('delete_task', { id });
  } catch (error) {
    console.error('Failed to delete task:', error);
    throw error;
  }
}; 