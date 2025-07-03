import { apiClient } from './apiClient';

export interface ASCRProcessingOptions {
  processingType: 'standard' | 'optimized' | 'ml_enhanced';
  year?: number;
  options?: Record<string, any>;
}

export interface ASCRProcessingResponse {
  status: 'success' | 'error';
  message: string;
  data: any;
}

export interface ASCRTaskStatus {
  task_id: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress: number;
  result?: any;
  error?: string;
  created_at: string;
  updated_at: string;
}

export class ASCRService {
  private static readonly BASE_URL = '/api/v1/ascr';

  /**
   * PDF 파일 업로드 및 처리
   */
  static async uploadAndProcess(
    formData: FormData, 
    options: ASCRProcessingOptions
  ): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/process`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        params: {
          processing_type: options.processingType,
          year: options.year,
          ...options.options
        }
      }
    );
    return response.data;
  }

  /**
   * 목차 추출
   */
  static async extractTOC(
    formData: FormData, 
    year: number
  ): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/extract-toc`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        params: { year }
      }
    );
    return response.data;
  }

  /**
   * 텍스트 추출
   */
  static async extractText(
    formData: FormData, 
    pages?: number[]
  ): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/extract-text`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        params: { pages }
      }
    );
    return response.data;
  }

  /**
   * PDF 분할
   */
  static async splitPDF(
    formData: FormData, 
    tocStructure?: any
  ): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/split-pdf`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        params: { toc_structure: JSON.stringify(tocStructure) }
      }
    );
    return response.data;
  }

  /**
   * 표준 가격 목록 다운로드
   */
  static async downloadStandardPrice(
    year: number, 
    forceUpdate: boolean = false
  ): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/download-standard-price`,
      null,
      {
        params: { year, force_update: forceUpdate }
      }
    );
    return response.data;
  }

  /**
   * 가격 목록 검증
   */
  static async validatePriceList(year: number): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/validate-price-list`,
      null,
      {
        params: { year }
      }
    );
    return response.data;
  }

  /**
   * 지반 진실 데이터 분석
   */
  static async analyzeGroundTruth(
    formData: FormData, 
    analysisType: string = 'comprehensive'
  ): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/analyze-ground-truth`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        params: { analysis_type: analysisType }
      }
    );
    return response.data;
  }

  /**
   * 계층 구조 수정
   */
  static async fixHierarchy(
    formData: FormData, 
    fixType: string = 'dots_to_commas'
  ): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/fix-hierarchy`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        params: { fix_type: fixType }
      }
    );
    return response.data;
  }

  /**
   * 작업 상태 조회
   */
  static async getTaskStatus(taskId: string): Promise<ASCRTaskStatus> {
    const response = await apiClient.get<ASCRTaskStatus>(
      `${this.BASE_URL}/status/${taskId}`
    );
    return response.data;
  }

  /**
   * 모든 작업 목록 조회
   */
  static async getAllTasks(): Promise<ASCRTaskStatus[]> {
    const response = await apiClient.get<ASCRTaskStatus[]>(
      `${this.BASE_URL}/tasks`
    );
    return response.data;
  }

  /**
   * 작업 취소
   */
  static async cancelTask(taskId: string): Promise<void> {
    await apiClient.delete(`${this.BASE_URL}/tasks/${taskId}`);
  }

  /**
   * 성능 리포트 조회
   */
  static async getPerformanceReport(): Promise<any> {
    const response = await apiClient.get(`${this.BASE_URL}/performance-report`);
    return response.data;
  }

  /**
   * 처리 통계 조회
   */
  static async getProcessingStats(): Promise<any> {
    const response = await apiClient.get(`${this.BASE_URL}/stats`);
    return response.data;
  }

  /**
   * ASCR 모듈 상태 조회
   */
  static async getStatus(): Promise<any> {
    const response = await apiClient.get(`${this.BASE_URL}/status`);
    return response.data;
  }

  /**
   * 배치 처리
   */
  static async batchProcess(
    files: string[], 
    outputDir: string, 
    options: ASCRProcessingOptions
  ): Promise<ASCRProcessingResponse> {
    const response = await apiClient.post<ASCRProcessingResponse>(
      `${this.BASE_URL}/batch`,
      {
        files,
        output_dir: outputDir,
        processing_type: options.processingType,
        options: options.options
      }
    );
    return response.data;
  }
} 