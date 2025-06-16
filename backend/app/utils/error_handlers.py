"""
에러 처리 유틸리티 함수
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request

class AppException(HTTPException):
    """
    애플리케이션 예외 클래스
    """
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class ValidationError(AppException):
    """
    데이터 검증 예외
    """
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class AuthenticationError(AppException):
    """
    인증 예외
    """
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationError(AppException):
    """
    권한 예외
    """
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    검증 예외 핸들러
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    """
    인증 예외 핸들러
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )

async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    """
    권한 예외 핸들러
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    ) 