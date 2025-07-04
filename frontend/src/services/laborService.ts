import { apiClient } from './apiClient';
import { 
  Labor, 
  LaborCreate, 
  LaborUpdate, 
  LaborListResponse, 
  LaborResponse,
  LaborFilters,
  WorkTime,
  WorkTimeCreate,
  WorkTimeUpdate,
  LaborStats,
  PositionStats,
  MonthlyLaborStats
} from '../types/labor';

export class LaborService {
  private static readonly BASE_URL = '/api/v1/labor';

  /**
   * 노무 목록 조회
   */
  static async getLaborList(params: LaborFilters = {}): Promise<LaborListResponse> {
    const { page = 1, size = 10, search, status, position, contractId, startDate, endDate } = params;
    const skip = (page - 1) * size;
    
    const queryParams = new URLSearchParams({
      skip: skip.toString(),
      limit: size.toString(),
    });
    
    if (search) queryParams.append('search', search);
    if (status) queryParams.append('status', status);
    if (position) queryParams.append('position', position);
    if (contractId) queryParams.append('contract_id', contractId);
    if (startDate) queryParams.append('start_date', startDate);
    if (endDate) queryParams.append('end_date', endDate);
    
    const response = await apiClient.get<LaborListResponse>(
      `${this.BASE_URL}/?${queryParams.toString()}`
    );
    return response.data;
  }

  /**
   * 노무 상세 조회
   */
  static async getLabor(id: string): Promise<LaborResponse> {
    const response = await apiClient.get<LaborResponse>(`${this.BASE_URL}/${id}`);
    return response.data;
  }

  /**
   * 노무 생성
   */
  static async createLabor(labor: LaborCreate): Promise<LaborResponse> {
    const response = await apiClient.post<LaborResponse>(this.BASE_URL, labor);
    return response.data;
  }

  /**
   * 노무 수정
   */
  static async updateLabor(id: string, labor: LaborUpdate): Promise<LaborResponse> {
    const response = await apiClient.put<LaborResponse>(`${this.BASE_URL}/${id}`, labor);
    return response.data;
  }

  /**
   * 노무 삭제
   */
  static async deleteLabor(id: string): Promise<{ status: string; message: string }> {
    const response = await apiClient.delete(`${this.BASE_URL}/${id}`);
    return response.data;
  }

  /**
   * 노무 통계 조회
   */
  static async getLaborStats(params?: {
    contractId?: string;
    startDate?: string;
    endDate?: string;
  }): Promise<LaborStats> {
    const queryParams = new URLSearchParams();
    if (params?.contractId) queryParams.append('contract_id', params.contractId);
    if (params?.startDate) queryParams.append('start_date', params.startDate);
    if (params?.endDate) queryParams.append('end_date', params.endDate);
    
    const response = await apiClient.get<LaborStats>(
      `${this.BASE_URL}/stats?${queryParams.toString()}`
    );
    return response.data;
  }

  /**
   * 직종별 통계 조회
   */
  static async getPositionStats(params?: {
    contractId?: string;
    startDate?: string;
    endDate?: string;
  }): Promise<PositionStats[]> {
    const queryParams = new URLSearchParams();
    if (params?.contractId) queryParams.append('contract_id', params.contractId);
    if (params?.startDate) queryParams.append('start_date', params.startDate);
    if (params?.endDate) queryParams.append('end_date', params.endDate);
    
    const response = await apiClient.get<PositionStats[]>(
      `${this.BASE_URL}/position-stats?${queryParams.toString()}`
    );
    return response.data;
  }

  /**
   * 월별 노무 통계 조회
   */
  static async getMonthlyLaborStats(year: number): Promise<MonthlyLaborStats[]> {
    const response = await apiClient.get<MonthlyLaborStats[]>(`${this.BASE_URL}/monthly-stats/${year}`);
    return response.data;
  }

  // 작업 시간 기록 관련 API
  /**
   * 작업 시간 기록 목록 조회
   */
  static async getWorkTimeList(laborId: string, params?: {
    startDate?: string;
    endDate?: string;
  }): Promise<WorkTime[]> {
    const queryParams = new URLSearchParams();
    if (params?.startDate) queryParams.append('start_date', params.startDate);
    if (params?.endDate) queryParams.append('end_date', params.endDate);
    
    const response = await apiClient.get<WorkTime[]>(
      `${this.BASE_URL}/${laborId}/work-time?${queryParams.toString()}`
    );
    return response.data;
  }

  /**
   * 작업 시간 기록 생성
   */
  static async createWorkTime(laborId: string, workTime: WorkTimeCreate): Promise<WorkTime> {
    const response = await apiClient.post<WorkTime>(`${this.BASE_URL}/${laborId}/work-time`, workTime);
    return response.data;
  }

  /**
   * 작업 시간 기록 수정
   */
  static async updateWorkTime(laborId: string, workTimeId: string, workTime: WorkTimeUpdate): Promise<WorkTime> {
    const response = await apiClient.put<WorkTime>(`${this.BASE_URL}/${laborId}/work-time/${workTimeId}`, workTime);
    return response.data;
  }

  /**
   * 작업 시간 기록 삭제
   */
  static async deleteWorkTime(laborId: string, workTimeId: string): Promise<{ status: string; message: string }> {
    const response = await apiClient.delete(`${this.BASE_URL}/${laborId}/work-time/${workTimeId}`);
    return response.data;
  }

  /**
   * 계약별 노무 목록 조회
   */
  static async getLaborByContract(contractId: string): Promise<Labor[]> {
    const response = await apiClient.get<Labor[]>(`${this.BASE_URL}/contract/${contractId}`);
    return response.data;
  }
} 