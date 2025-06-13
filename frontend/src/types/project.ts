export interface Project {
  id: number;
  name: string;
  description: string;
  status: '진행중' | '완료' | '대기중';
  startDate: string;
  endDate: string;
  progress: number;
  manager: string;
  budget: number;
  location: string;
  createdAt: string;
  updatedAt: string;
}

export interface ProjectFormData {
  name: string;
  description: string;
  status: '진행중' | '완료' | '대기중';
  startDate: string;
  endDate: string;
  manager: string;
  budget: number;
  location: string;
}

export interface ProjectState {
  projects: Project[];
  loading: boolean;
  error: string | null;
  selectedProject: Project | null;
} 