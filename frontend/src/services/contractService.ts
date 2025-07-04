import { apiClient } from './apiClient';
import { 
  Contract, 
  ContractCreate, 
  ContractUpdate, 
  ContractListResponse, 
  ContractResponse,
  ContractFilters
} from '../types/contract';

export class ContractService {
  private static readonly BASE_URL = '/api/v1/contracts';

  /**
   * 계약 목록 조회
   */
  static async getContracts(params: ContractFilters = {}): Promise<ContractListResponse> {
    const { page = 1, size = 10, search, status, startDate, endDate, vendorId } = params;
    const skip = (page - 1) * size;
    
    const queryParams = new URLSearchParams({
      skip: skip.toString(),
      limit: size.toString(),
    });
    
    if (search) queryParams.append('search', search);
    if (status) queryParams.append('status', status);
    if (startDate) queryParams.append('start_date', startDate);
    if (endDate) queryParams.append('end_date', endDate);
    if (vendorId) queryParams.append('vendor_id', vendorId);
    
    const response = await apiClient.get<ContractListResponse>(
      `${this.BASE_URL}/?${queryParams.toString()}`
    );
    return response.data;
  }

  /**
   * 계약 상세 조회
   */
  static async getContract(id: string): Promise<ContractResponse> {
    const response = await apiClient.get<ContractResponse>(`${this.BASE_URL}/${id}`);
    return response.data;
  }

  /**
   * 계약 생성
   */
  static async createContract(contract: ContractCreate): Promise<ContractResponse> {
    const response = await apiClient.post<ContractResponse>(this.BASE_URL, contract);
    return response.data;
  }

  /**
   * 계약 수정
   */
  static async updateContract(id: string, contract: ContractUpdate): Promise<ContractResponse> {
    const response = await apiClient.put<ContractResponse>(`${this.BASE_URL}/${id}`, contract);
    return response.data;
  }

  /**
   * 계약 삭제
   */
  static async deleteContract(id: string): Promise<{ status: string; message: string }> {
    const response = await apiClient.delete(`${this.BASE_URL}/${id}`);
    return response.data;
  }

  /**
   * 계약 통계 조회
   */
  static async getContractStats(): Promise<{
    total: number;
    active: number;
    completed: number;
    totalAmount: number;
  }> {
    const response = await apiClient.get(`${this.BASE_URL}/stats`);
    return response.data;
  }

  /**
   * 계약 상태별 개수 조회
   */
  static async getContractStatusCounts(): Promise<{
    진행중: number;
    완료: number;
    중단: number;
    취소: number;
  }> {
    const response = await apiClient.get(`${this.BASE_URL}/status-counts`);
    return response.data;
  }

  /**
   * 월별 계약 금액 조회
   */
  static async getMonthlyContractAmounts(year: number): Promise<{
    month: number;
    amount: number;
  }[]> {
    const response = await apiClient.get(`${this.BASE_URL}/monthly-amounts/${year}`);
    return response.data;
  }
} 