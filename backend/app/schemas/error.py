from typing import Optional, Any, Dict
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """
    표준화된 에러 응답 스키마
    """
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ValidationErrorResponse(ErrorResponse):
    """
    유효성 검사 에러 응답 스키마
    """
    field_errors: Dict[str, str]

class PermissionErrorResponse(ErrorResponse):
    """
    권한 관련 에러 응답 스키마
    """
    required_permissions: list[str]

class NotFoundErrorResponse(ErrorResponse):
    """
    리소스를 찾을 수 없는 경우의 에러 응답 스키마
    """
    resource_type: str
    resource_id: Any 