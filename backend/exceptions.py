from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BaseAPIException(HTTPException):
    """기본 API 예외 클래스"""
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class DatabaseException(BaseAPIException):
    """데이터베이스 관련 예외"""
    def __init__(self, detail: str = "데이터베이스 오류가 발생했습니다."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class ValidationException(BaseAPIException):
    """데이터 검증 관련 예외"""
    def __init__(self, detail: str = "입력 데이터가 유효하지 않습니다."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class AuthenticationException(BaseAPIException):
    """인증 관련 예외"""
    def __init__(self, detail: str = "인증에 실패했습니다."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationException(BaseAPIException):
    """권한 관련 예외"""
    def __init__(self, detail: str = "접근 권한이 없습니다."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class ResourceNotFoundException(BaseAPIException):
    """리소스 없음 예외"""
    def __init__(self, detail: str = "요청한 리소스를 찾을 수 없습니다."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class BusinessLogicException(BaseAPIException):
    """비즈니스 로직 관련 예외"""
    def __init__(self, detail: str = "비즈니스 로직 오류가 발생했습니다."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class ExternalServiceException(BaseAPIException):
    """외부 서비스 연동 관련 예외"""
    def __init__(self, detail: str = "외부 서비스 연동 중 오류가 발생했습니다."):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )

class RateLimitException(BaseAPIException):
    """요청 제한 관련 예외"""
    def __init__(self, detail: str = "요청 제한에 도달했습니다."):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail
        ) 