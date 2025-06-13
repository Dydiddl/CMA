import axios from 'axios';
import { invoke } from '@tauri-apps/api/tauri';
import { Project, Task, User, ApiResponse } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Tauri API를 사용하는 서비스
export const apiService = {
  projects: {
    getAll: () => invoke<ApiResponse<Project[]>>('get_projects'),
    getById: (id: number) => invoke<ApiResponse<Project>>('get_project', { id }),
    create: (project: Omit<Project, 'id' | 'createdAt' | 'updatedAt'>) => 
      invoke<ApiResponse<Project>>('create_project', { project }),
    update: (id: number, project: Partial<Project>) => 
      invoke<ApiResponse<Project>>('update_project', { id, project }),
    delete: (id: number) => invoke<ApiResponse<void>>('delete_project', { id })
  },
  tasks: {
    getAll: (projectId: number) => invoke<ApiResponse<Task[]>>('get_tasks', { projectId }),
    getById: (id: number) => invoke<ApiResponse<Task>>('get_task', { id }),
    create: (task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => 
      invoke<ApiResponse<Task>>('create_task', { task }),
    update: (id: number, task: Partial<Task>) => 
      invoke<ApiResponse<Task>>('update_task', { id, task }),
    delete: (id: number) => invoke<ApiResponse<void>>('delete_task', { id })
  },
  auth: {
    login: (username: string, password: string) => 
      invoke<ApiResponse<{ token: string; user: User }>>('login', { username, password }),
    register: (userData: Omit<User, 'id' | 'createdAt' | 'updatedAt'>) => 
      invoke<ApiResponse<User>>('register', { userData }),
    logout: () => invoke<ApiResponse<void>>('logout'),
    getCurrentUser: () => invoke<ApiResponse<User>>('get_current_user')
  }
};

export const getProjects = async (): Promise<Project[]> => {
  try {
    const projects = await invoke<Project[]>('get_projects');
    return projects;
  } catch (error) {
    console.error('프로젝트 목록을 가져오는데 실패했습니다:', error);
    throw error;
  }
};