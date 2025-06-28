import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export interface TOCStructure {
  chapters: Array<{
    title: string;
    page: number;
    children?: Array<{
      title: string;
      page: number;
    }>;
  }>;
}

export interface PDFExtractionResult {
  text: string;
  pages: number;
  structure?: TOCStructure;
}

export interface StandardPriceResult {
  year: number;
  status: string;
  file_path?: string;
}

export interface ValidationResult {
  is_valid: boolean;
  errors: string[];
  warnings: string[];
}

const ascrService = {
  // PDF 목차 추출
  extractTOC: async (file: File, year?: number): Promise<TOCStructure> => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (year) {
        formData.append('year', year.toString());
      }

      const response = await axios.post(`${API_URL}/ascr/extract-toc`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data.data;
    } catch (error) {
      console.error('목차 추출 실패:', error);
      throw error;
    }
  },

  // PDF 텍스트 추출
  extractText: async (file: File, pages?: number[]): Promise<PDFExtractionResult> => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (pages) {
        formData.append('pages', JSON.stringify(pages));
      }

      const response = await axios.post(`${API_URL}/ascr/extract-text`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data.data;
    } catch (error) {
      console.error('텍스트 추출 실패:', error);
      throw error;
    }
  },

  // PDF 분할
  splitPDF: async (file: File, tocStructure: TOCStructure): Promise<string[]> => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('toc_structure', JSON.stringify(tocStructure));

      const response = await axios.post(`${API_URL}/ascr/split-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data.data;
    } catch (error) {
      console.error('PDF 분할 실패:', error);
      throw error;
    }
  },

  // 표준 가격 목록 다운로드
  downloadStandardPrice: async (year: number, forceUpdate: boolean = false): Promise<StandardPriceResult> => {
    try {
      const response = await axios.post(`${API_URL}/ascr/download-standard-price`, {
        year,
        force_update: forceUpdate,
      });

      return response.data.data;
    } catch (error) {
      console.error('표준 가격 목록 다운로드 실패:', error);
      throw error;
    }
  },

  // 표준 가격 목록 검증
  validatePriceList: async (year: number): Promise<ValidationResult> => {
    try {
      const response = await axios.post(`${API_URL}/ascr/validate-price-list`, {
        year,
      });

      return response.data.data;
    } catch (error) {
      console.error('표준 가격 목록 검증 실패:', error);
      throw error;
    }
  },

  // 지반 진실 데이터 분석
  analyzeGroundTruth: async (file: File, analysisType: string = 'comprehensive'): Promise<any> => {
    try {
      const formData = new FormData();
      formData.append('data_file', file);
      formData.append('analysis_type', analysisType);

      const response = await axios.post(`${API_URL}/ascr/analyze-ground-truth`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data.data;
    } catch (error) {
      console.error('지반 진실 데이터 분석 실패:', error);
      throw error;
    }
  },

  // 계층 구조 수정
  fixHierarchy: async (file: File, fixType: string = 'dots_to_commas'): Promise<any> => {
    try {
      const formData = new FormData();
      formData.append('structure_file', file);
      formData.append('fix_type', fixType);

      const response = await axios.post(`${API_URL}/ascr/fix-hierarchy`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data.data;
    } catch (error) {
      console.error('계층 구조 수정 실패:', error);
      throw error;
    }
  },

  // ASCR 상태 확인
  getStatus: async (): Promise<any> => {
    try {
      const response = await axios.get(`${API_URL}/ascr/status`);
      return response.data.data;
    } catch (error) {
      console.error('ASCR 상태 확인 실패:', error);
      throw error;
    }
  },
};

export default ascrService; 