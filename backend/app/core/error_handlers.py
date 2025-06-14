from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from app.schemas.error import (
    ErrorResponse,
    ValidationErrorResponse,
    PermissionErrorResponse,
    NotFoundErrorResponse
)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    유효성 검사 에러 처리
    """
    field_errors = {}
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"])
        field_errors[field] = error["msg"]
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ValidationErrorResponse(
            code="VALIDATION_ERROR",
            message="입력값이 유효하지 않습니다",
            field_errors=field_errors
        ).dict()
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    데이터베이스 무결성 에러 처리
    """
    error_message = str(exc.orig)
    if "unique constraint" in error_message.lower():
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                code="DUPLICATE_ENTRY",
                message="이미 존재하는 데이터입니다",
                details={"error": error_message}
            ).dict()
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            code="DATABASE_ERROR",
            message="데이터베이스 오류가 발생했습니다",
            details={"error": error_message}
        ).dict()
    )

async def permission_error_handler(request: Request, exc: PermissionErrorResponse):
    """
    권한 관련 에러 처리
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=exc.dict()
    )

async def not_found_error_handler(request: Request, exc: NotFoundErrorResponse):
    """
    리소스를 찾을 수 없는 경우의 에러 처리
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.dict()
    )

async def general_exception_handler(request: Request, exc: Exception):
    """
    일반적인 예외 처리
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            code="INTERNAL_SERVER_ERROR",
            message="서버 내부 오류가 발생했습니다",
            details={"error": str(exc)}
        ).dict()
    ) 