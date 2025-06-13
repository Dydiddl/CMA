export * from './project';
export * from './task';
export * from './user';

export interface Project {
  id: number;
  name: string;
  description: string;
  status: 'ACTIVE' | 'COMPLETED' | 'ON_HOLD';
  startDate: string;
  endDate: string;
  createdAt: string;
  updatedAt: string;
}

export interface Task {
  id: number;
  projectId: number;
  name: string;
  description: string;
  status: 'TODO' | 'IN_PROGRESS' | 'DONE';
  progress: number;
  startDate: string;
  endDate: string;
  createdAt: string;
  updatedAt: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'ADMIN' | 'USER';
  createdAt: string;
  updatedAt: string;
}

export interface ApiResponse<T> {
  data: T;
  message: string;
  status: number;
} 