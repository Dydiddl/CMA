import { useState, useCallback } from 'react';
import { AxiosError } from 'axios';

interface ErrorState {
  message: string;
  code?: string;
  details?: unknown;
}

export const useApiErrorHandling = () => {
  const [error, setError] = useState<ErrorState | null>(null);

  const handleError = useCallback((error: unknown) => {
    if (error instanceof AxiosError) {
      const response = error.response;
      const errorMessage = response?.data?.message || error.message;
      const errorCode = response?.data?.code || error.code;
      
      setError({
        message: errorMessage,
        code: errorCode,
        details: response?.data,
      });

      // 에러 로깅
      console.error('[API Error]', {
        message: errorMessage,
        code: errorCode,
        status: response?.status,
        url: error.config?.url,
        method: error.config?.method,
        details: response?.data,
      });
    } else {
      const errorMessage = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다';
      setError({
        message: errorMessage,
        details: error,
      });

      // 에러 로깅
      console.error('[Unknown Error]', {
        message: errorMessage,
        details: error,
      });
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    error,
    handleError,
    clearError,
  };
}; 