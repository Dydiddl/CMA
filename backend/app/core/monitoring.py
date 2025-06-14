from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps
from fastapi import Request
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

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

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

DB_CONNECTIONS = Gauge(
    'db_connections',
    'Number of active database connections'
)

# 로깅 설정
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'app.log',
                maxBytes=10000000,
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        if hasattr(record, "extra"):
            log_record.update(record.extra)
        return json.dumps(log_record)

# 모니터링 미들웨어
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # 요청 처리 시간 측정
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        # 요청 수 카운트
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        return response
    except Exception as e:
        # 에러 발생 시 로깅
        logging.error(f"Request failed: {str(e)}", exc_info=True)
        raise

# 성능 모니터링 데코레이터
def monitor_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            
            # 함수 실행 시간 로깅
            logging.info(
                f"Function {func.__name__} executed in {duration:.2f} seconds",
                extra={
                    "function": func.__name__,
                    "duration": duration,
                    "args": str(args),
                    "kwargs": str(kwargs)
                }
            )
            return result
        except Exception as e:
            # 에러 발생 시 로깅
            logging.error(
                f"Function {func.__name__} failed: {str(e)}",
                exc_info=True,
                extra={
                    "function": func.__name__,
                    "args": str(args),
                    "kwargs": str(kwargs)
                }
            )
            raise
    return wrapper

# 데이터베이스 모니터링
def monitor_db_connections(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        DB_CONNECTIONS.inc()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            DB_CONNECTIONS.dec()
    return wrapper 