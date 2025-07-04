import { apiClient } from './apiClient';
import { 
  FinancialRecord, 
  FinancialCreate, 
  FinancialUpdate, 
  FinancialListResponse, 
  FinancialResponse,
  FinancialFilters,
  FinancialStats,
  CategoryStats,
  MonthlyStats
} from '../types/financial';

export class FinancialService {
  private static readonly BASE_URL = '/api/v1/financial';

  /**
   * 재무 기록 목록 조회
   */
  static async getFinancialRecords(params: FinancialFilters = {}): Promise<FinancialListResponse> {
    const { page = 1, size = 10, type, category, search, startDate, endDate, contractId } = params;
    const skip = (page - 1) * size;
    
    const queryParams = new URLSearchParams({
      skip: skip.toString(),
      limit: size.toString(),
    });
    
    if (type) queryParams.append('type', type);
    if (category) queryParams.append('category', category);
    if (search) queryParams.append('search', search);
    if (startDate) queryParams.append('start_date', startDate);
    if (endDate) queryParams.append('end_date', endDate);
    if (contractId) queryParams.append('contract_id', contractId);
    
    const response = await apiClient.get<FinancialListResponse>(
      `${this.BASE_URL}/?${queryParams.toString()}`
    );
    return response.data;
  }

  /**
   * 재무 기록 상세 조회
   */
  static async getFinancialRecord(id: string): Promise<FinancialResponse> {
    const response = await apiClient.get<FinancialResponse>(`${this.BASE_URL}/${id}`);
    return response.data;
  }

  /**
   * 재무 기록 생성
   */
  static async createFinancialRecord(record: FinancialCreate): Promise<FinancialResponse> {
    const response = await apiClient.post<FinancialResponse>(this.BASE_URL, record);
    return response.data;
  }

  /**
   * 재무 기록 수정
   */
  static async updateFinancialRecord(id: string, record: FinancialUpdate): Promise<FinancialResponse> {
    const response = await apiClient.put<FinancialResponse>(`${this.BASE_URL}/${id}`, record);
    return response.data;
  }

  /**
   * 재무 기록 삭제
   */
  static async deleteFinancialRecord(id: string): Promise<{ status: string; message: string }> {
    const response = await apiClient.delete(`${this.BASE_URL}/${id}`);
    return response.data;
  }

  /**
   * 재무 통계 조회
   */
  static async getFinancialStats(params?: {
    startDate?: string;
    endDate?: string;
    contractId?: string;
  }): Promise<FinancialStats> {
    const queryParams = new URLSearchParams();
    if (params?.startDate) queryParams.append('start_date', params.startDate);
    if (params?.endDate) queryParams.append('end_date', params.endDate);
    if (params?.contractId) queryParams.append('contract_id', params.contractId);
    
    const response = await apiClient.get<FinancialStats>(
      `${this.BASE_URL}/stats?${queryParams.toString()}`
    );
    return response.data;
  }

  /**
   * 카테고리별 통계 조회
   */
  static async getCategoryStats(params?: {
    type?: '수입' | '지출';
    startDate?: string;
    endDate?: string;
  }): Promise<CategoryStats[]> {
    const queryParams = new URLSearchParams();
    if (params?.type) queryParams.append('type', params.type);
    if (params?.startDate) queryParams.append('start_date', params.startDate);
    if (params?.endDate) queryParams.append('end_date', params.endDate);
    
    const response = await apiClient.get<CategoryStats[]>(
      `${this.BASE_URL}/category-stats?${queryParams.toString()}`
    );
    return response.data;
  }

  /**
   * 월별 통계 조회
   */
  static async getMonthlyStats(year: number): Promise<MonthlyStats[]> {
    const response = await apiClient.get<MonthlyStats[]>(`${this.BASE_URL}/monthly-stats/${year}`);
    return response.data;
  }

  /**
   * 계약별 재무 기록 조회
   */
  static async getFinancialRecordsByContract(contractId: string): Promise<FinancialRecord[]> {
    const response = await apiClient.get<FinancialRecord[]>(`${this.BASE_URL}/contract/${contractId}`);
    return response.data;
  }
} 