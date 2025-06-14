# 에러 처리 (Error Handling)

## 에러 응답 형식

### 기본 형식
```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "에러 메시지",
        "details": {
            "field": "에러가 발생한 필드",
            "reason": "상세 에러 원인"
        }
    }
}
```

## HTTP 상태 코드

### 2xx - 성공
- 200: OK
- 201: Created
- 204: No Content

### 4xx - 클라이언트 에러
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity

### 5xx - 서버 에러
- 500: Internal Server Error
- 503: Service Unavailable

## 에러 코드 목록

### 인증 관련 (AUTH_*)
- AUTH_REQUIRED: 인증 필요
- AUTH_INVALID_TOKEN: 유효하지 않은 토큰
- AUTH_TOKEN_EXPIRED: 토큰 만료
- AUTH_PERMISSION_DENIED: 권한 없음

### 리소스 관련 (RESOURCE_*)
- RESOURCE_NOT_FOUND: 리소스를 찾을 수 없음
- RESOURCE_ALREADY_EXISTS: 리소스가 이미 존재함
- RESOURCE_CONFLICT: 리소스 충돌

### 유효성 검사 (VALIDATION_*)
- VALIDATION_ERROR: 입력값 검증 실패
- VALIDATION_REQUIRED: 필수 필드 누락
- VALIDATION_INVALID_FORMAT: 잘못된 형식

### 시스템 관련 (SYSTEM_*)
- SYSTEM_ERROR: 시스템 에러
- SYSTEM_MAINTENANCE: 시스템 점검 중
- SYSTEM_RATE_LIMIT: 요청 제한 초과 