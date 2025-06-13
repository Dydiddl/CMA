export interface User {
  id: number;
  username: string;
  email: string;
  role: '관리자' | '일반사용자';
  department: string;
  position: string;
  createdAt: string;
  updatedAt: string;
}

export interface UserFormData {
  username: string;
  email: string;
  password: string;
  role: '관리자' | '일반사용자';
  department: string;
  position: string;
}

export interface UserState {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

export interface LoginFormData {
  email: string;
  password: string;
} 