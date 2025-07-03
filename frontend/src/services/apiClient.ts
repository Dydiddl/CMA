import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// API 기본 설정
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Axios 인스턴스 생성
const apiClient: AxiosInstance = axios.create({
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
  (error) => {
    console.error('[API Response Error]', error);
    
    // 401 에러 시 토큰 제거
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      // 로그인 페이지로 리다이렉트 (필요시)
      // window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export { apiClient };
export default apiClient; 