export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE';
export type TaskPriority = 'HIGH' | 'MEDIUM' | 'LOW';

export interface Task {
  id: number;
  name: string;
  description: string;
  status: TaskStatus;
  progress: number;
  startDate: string;
  endDate: string;
  projectId: number;
  assignee: string;
  priority: TaskPriority;
  createdAt: string;
  updatedAt: string;
}

export interface TaskFormData {
  name: string;
  description: string;
  status: TaskStatus;
  progress: number;
  startDate: string;
  endDate: string;
  projectId: number;
  assignee: string;
  priority: TaskPriority;
}

export interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  selectedTask: Task | null;
} 