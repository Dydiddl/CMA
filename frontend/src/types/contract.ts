export interface Contract {
  id: string;
  name: string;
  contractNumber: string;
  contractAmount: number;
  contractDate: string;
  startDate?: string;
  endDate?: string;
  clientName: string;
  clientContact?: string;
  status: ContractStatus;
  description?: string;
  vendorId: string;
  createdAt: string;
  updatedAt: string;
}

export type ContractStatus = '진행중' | '완료' | '중단' | '취소';

export interface ContractCreate {
  name: string;
  contractNumber: string;
  contractAmount: number;
  contractDate: string;
  startDate?: string;
  endDate?: string;
  clientName: string;
  clientContact?: string;
  status?: ContractStatus;
  description?: string;
  vendorId: string;
}

export interface ContractUpdate {
  name?: string;
  contractNumber?: string;
  contractAmount?: number;
  contractDate?: string;
  startDate?: string;
  endDate?: string;
  clientName?: string;
  clientContact?: string;
  status?: ContractStatus;
  description?: string;
  vendorId?: string;
}

export interface ContractListResponse {
  status: 'success' | 'error';
  data: Contract[];
  total: number;
  page: number;
  size: number;
  message?: string;
}

export interface ContractResponse {
  status: 'success' | 'error';
  data: Contract;
  message?: string;
}

export interface ContractFilters {
  page?: number;
  size?: number;
  search?: string;
  status?: string;
  startDate?: string;
  endDate?: string;
  vendorId?: string;
} 