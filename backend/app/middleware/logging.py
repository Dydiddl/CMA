"""
로깅 미들웨어
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# 로거 설정
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    로깅 미들웨어 클래스
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # 요청 시작 시간
        start_time = time.time()

        # 요청 정보 로깅
        logger.info(f"Request started: {request.method} {request.url.path}")

        try:
            # 요청 처리
            response = await call_next(request)

            # 응답 시간 계산
            process_time = time.time() - start_time

            # 응답 정보 로깅
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Time: {process_time:.2f}s"
            )

            return response

        except Exception as e:
            # 에러 로깅
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"Error: {str(e)}"
            )
            raise 