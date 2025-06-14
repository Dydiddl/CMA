# 사용자 관리 API

## 기본 정보
- 엔드포인트: `/api/v1/users`
- 인증: JWT 토큰 필요 (일부 엔드포인트 제외)

## API 목록

### 1. 사용자 등록
```http
POST /users
Content-Type: application/json

{
    "email": "user@example.com",
    "name": "홍길동",
    "password": "password123",
    "role": "user"
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "user-uuid",
        "email": "user@example.com",
        "name": "홍길동",
        "role": "user",
        "created_at": "2024-03-20T10:00:00Z"
    },
    "message": "사용자가 성공적으로 등록되었습니다."
}
```

### 2. 사용자 로그인
```http
POST /users/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "access_token": "jwt-token",
        "refresh_token": "refresh-token",
        "expires_in": 1800
    },
    "message": "로그인에 성공했습니다."
}
```

### 3. 사용자 정보 조회
```http
GET /users/{user_id}
Authorization: Bearer {token}
```

#### 응답
```json
{
    "status": "success",
    "data": {
        "id": "user-uuid",
        "email": "user@example.com",
        "name": "홍길동",
        "role": "user",
        "created_at": "2024-03-20T10:00:00Z",
        "last_login": "2024-03-20T15:30:00Z"
    },
    "message": "사용자 정보를 성공적으로 조회했습니다."
}
```

## 에러 코드
- `VALIDATION_ERROR`: 입력값 검증 실패
- `USER_ALREADY_EXISTS`: 이미 존재하는 사용자
- `INVALID_CREDENTIALS`: 잘못된 로그인 정보
- `USER_NOT_FOUND`: 사용자를 찾을 수 없음

## 요청 제한
- 등록: IP당 1분에 5회
- 로그인: IP당 1분에 10회
- 정보 조회: 토큰당 1초에 30회 