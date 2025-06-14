# 인증 (Authentication)

## JWT 인증

### 토큰 정보
- 토큰 타입: JWT (JSON Web Token)
- 인증 방식: Bearer 토큰
- 토큰 만료 시간: 30분
- 갱신 토큰: 지원 (만료 24시간 전 갱신 가능)

### 토큰 구조
```json
{
    "header": {
        "alg": "HS256",
        "typ": "JWT"
    },
    "payload": {
        "sub": "user-id",
        "role": "user",
        "iat": 1516239022,
        "exp": 1516240822
    }
}
```

### 인증 헤더
```
Authorization: Bearer <token>
```

### 토큰 갱신
```http
POST /auth/refresh
Authorization: Bearer <refresh_token>
```

## API 키 인증

### API 키 발급
- 관리자 페이지에서 발급
- 발급 시 권한 설정 가능
- IP 제한 설정 가능

### API 키 사용
```
X-API-Key: <api-key>
```

## 보안 정책
- HTTPS 필수 사용
- 토큰은 안전한 저장소에 보관
- 정기적인 토큰 순환
- 실패한 인증 시도 로깅 