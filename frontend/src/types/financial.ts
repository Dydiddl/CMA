export interface FinancialRecord {
  id: string;
  type: FinancialType;
  category: string;
  description: string;
  amount: number;
  date: string;
  paymentMethod: string;
  contractId?: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export type FinancialType = '수입' | '지출';

export interface FinancialCreate {
  type: FinancialType;
  category: string;
  description: string;
  amount: number;
  date: string;
  paymentMethod: string;
  contractId?: string;
  notes?: string;
}

export interface FinancialUpdate {
  type?: FinancialType;
  category?: string;
  description?: string;
  amount?: number;
  date?: string;
  paymentMethod?: string;
  contractId?: string;
  notes?: string;
}

export interface FinancialListResponse {
  status: 'success' | 'error';
  data: FinancialRecord[];
  total: number;
  page: number;
  size: number;
  message?: string;
}

export interface FinancialResponse {
  status: 'success' | 'error';
  data: FinancialRecord;
  message?: string;
}

export interface FinancialFilters {
  page?: number;
  size?: number;
  type?: FinancialType;
  category?: string;
  search?: string;
  startDate?: string;
  endDate?: string;
  contractId?: string;
}

export interface FinancialStats {
  totalIncome: number;
  totalExpense: number;
  netAmount: number;
  incomeCount: number;
  expenseCount: number;
  totalCount: number;
}

export interface CategoryStats {
  category: string;
  amount: number;
  count: number;
  percentage: number;
}

export interface MonthlyStats {
  month: string;
  income: number;
  expense: number;
  netAmount: number;
} 