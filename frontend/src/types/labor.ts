export interface Labor {
  id: string;
  workerName: string;
  workerId: string;
  position: string;
  hourlyRate: number;
  dailyRate: number;
  contractId: string;
  startDate: string;
  endDate?: string;
  status: LaborStatus;
  phoneNumber?: string;
  email?: string;
  address?: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export type LaborStatus = '활성' | '비활성' | '퇴사' | '휴직';

export interface LaborCreate {
  workerName: string;
  workerId: string;
  position: string;
  hourlyRate: number;
  dailyRate: number;
  contractId: string;
  startDate: string;
  endDate?: string;
  status?: LaborStatus;
  phoneNumber?: string;
  email?: string;
  address?: string;
  notes?: string;
}

export interface LaborUpdate {
  workerName?: string;
  workerId?: string;
  position?: string;
  hourlyRate?: number;
  dailyRate?: number;
  contractId?: string;
  startDate?: string;
  endDate?: string;
  status?: LaborStatus;
  phoneNumber?: string;
  email?: string;
  address?: string;
  notes?: string;
}

export interface LaborListResponse {
  status: 'success' | 'error';
  data: Labor[];
  total: number;
  page: number;
  size: number;
  message?: string;
}

export interface LaborResponse {
  status: 'success' | 'error';
  data: Labor;
  message?: string;
}

export interface LaborFilters {
  page?: number;
  size?: number;
  search?: string;
  status?: LaborStatus;
  position?: string;
  contractId?: string;
  startDate?: string;
  endDate?: string;
}

// 작업 시간 기록
export interface WorkTime {
  id: string;
  laborId: string;
  date: string;
  startTime: string;
  endTime: string;
  breakTime: number; // 분 단위
  totalHours: number;
  hourlyRate: number;
  totalAmount: number;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface WorkTimeCreate {
  laborId: string;
  date: string;
  startTime: string;
  endTime: string;
  breakTime: number;
  notes?: string;
}

export interface WorkTimeUpdate {
  date?: string;
  startTime?: string;
  endTime?: string;
  breakTime?: number;
  notes?: string;
}

// 노무 통계
export interface LaborStats {
  totalWorkers: number;
  activeWorkers: number;
  totalWorkHours: number;
  totalLaborCost: number;
  averageHourlyRate: number;
}

export interface PositionStats {
  position: string;
  count: number;
  averageRate: number;
  totalCost: number;
}

export interface MonthlyLaborStats {
  month: string;
  totalHours: number;
  totalCost: number;
  workerCount: number;
} 