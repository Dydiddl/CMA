import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';

// API 기본 설정
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Axios 인스턴스 생성
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30초
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    // 토큰이 있으면 헤더에 추가
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`[API Response] ${response.status} ${response.config.url}`);
    return response;
  },
  (error: AxiosError) => {
    console.error('[API Response Error]', error);
    
    // 에러 처리
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          // 인증 실패 - 로그인 페이지로 리다이렉트
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
          break;
          
        case 403:
          // 권한 없음
          console.error('접근 권한이 없습니다.');
          break;
          
        case 404:
          // 리소스 없음
          console.error('요청한 리소스를 찾을 수 없습니다.');
          break;
          
        case 422:
          // 검증 오류
          console.error('입력 데이터가 올바르지 않습니다.');
          break;
          
        case 500:
          // 서버 오류
          console.error('서버 오류가 발생했습니다.');
          break;
          
        default:
          console.error(`API 오류: ${status}`);
      }
      
      // 에러 메시지 추출
      if (data && typeof data === 'object' && 'detail' in data) {
        error.message = data.detail as string;
      }
    } else if (error.request) {
      // 네트워크 오류
      error.message = '네트워크 연결을 확인해주세요.';
    } else {
      // 기타 오류
      error.message = '알 수 없는 오류가 발생했습니다.';
    }
    
    return Promise.reject(error);
  }
);

// API 응답 타입 정의
export interface ApiResponse<T = any> {
  status: 'success' | 'error';
  data: T;
  message?: string;
}

export interface ApiListResponse<T = any> extends ApiResponse<T[]> {
  total: number;
  page: number;
  size: number;
}

// API 클라이언트 래퍼 함수들
export const api = {
  // GET 요청
  get: <T = any>(url: string, params?: any): Promise<AxiosResponse<T>> => {
    return apiClient.get<T>(url, { params });
  },

  // POST 요청
  post: <T = any>(url: string, data?: any): Promise<AxiosResponse<T>> => {
    return apiClient.post<T>(url, data);
  },

  // PUT 요청
  put: <T = any>(url: string, data?: any): Promise<AxiosResponse<T>> => {
    return apiClient.put<T>(url, data);
  },

  // PATCH 요청
  patch: <T = any>(url: string, data?: any): Promise<AxiosResponse<T>> => {
    return apiClient.patch<T>(url, data);
  },

  // DELETE 요청
  delete: <T = any>(url: string): Promise<AxiosResponse<T>> => {
    return apiClient.delete<T>(url);
  },

  // 파일 업로드
  upload: <T = any>(url: string, formData: FormData): Promise<AxiosResponse<T>> => {
    return apiClient.post<T>(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // 파일 다운로드
  download: (url: string, filename?: string): Promise<void> => {
    return apiClient.get(url, {
      responseType: 'blob',
    }).then((response) => {
      const blob = new Blob([response.data]);
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename || 'download';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
    });
  },
};

export default apiClient; 