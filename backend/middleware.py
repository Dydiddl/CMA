import time
from fastapi import Request
from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from .config import settings
from .logger import api_logger

# 메트릭 정의
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 요청 처리
        response = await call_next(request)
        
        # 지연 시간 계산
        latency = time.time() - start_time
        
        # 메트릭 업데이트
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(latency)
        
        # 로깅
        api_logger.info(
            f"Method: {request.method}, "
            f"Path: {request.url.path}, "
            f"Status: {response.status_code}, "
            f"Latency: {latency:.3f}s"
        )
        
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 요청 시작 로깅
        api_logger.info(f"Request started: {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            # 요청 완료 로깅
            api_logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"Status: {response.status_code}"
            )
            return response
        except Exception as e:
            # 에러 로깅
            api_logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"Error: {str(e)}"
            )
            raise

def get_metrics():
    """Prometheus 메트릭을 반환합니다."""
    return generate_latest() 