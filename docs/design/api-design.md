# API 설계 문서

## 1. API 기본 정보

### 1.1 기본 URL
- 개발: `http://localhost:8000/api/v1`
- 프로덕션: `https://api.example.com/api/v1`

### 1.2 인증 방식
- JWT (JSON Web Token) 기반 인증
- Bearer 토큰 사용
- 토큰 만료 시간: 30분

### 1.3 응답 형식
```json
{
    "status": "success",
    "data": {
        // 응답 데이터
    },
    "message": "성공적으로 처리되었습니다."
}
```

## 2. API 엔드포인트

### 2.1 사용자 관리 API

#### 사용자 등록
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

#### 사용자 로그인
```http
POST /users/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

### 2.2 거래처 관리 API

#### 거래처 목록 조회
```http
GET /vendors
Authorization: Bearer {token}
```

#### 거래처 상세 조회
```http
GET /vendors/{vendor_id}
Authorization: Bearer {token}
```

#### 거래처 등록
```http
POST /vendors
Authorization: Bearer {token}
Content-Type: application/json

{
    "company_name": "건설회사",
    "business_number": "123-45-67890",
    "representative": "김대표",
    "address": "서울시 강남구",
    "contact": "02-1234-5678",
    "bank_info": {
        "bank_name": "국민은행",
        "account_number": "123-456-789012"
    }
}
```

### 2.3 계약 관리 API

#### 계약 목록 조회
```http
GET /contracts
Authorization: Bearer {token}
```

#### 계약 상세 조회
```http
GET /contracts/{contract_id}
Authorization: Bearer {token}
```

#### 계약 등록
```http
POST /contracts
Authorization: Bearer {token}
Content-Type: application/json

{
    "project_name": "아파트 신축공사",
    "contract_amount": 1000000000,
    "contract_date": "2024-03-20",
    "vendor_id": "vendor-uuid",
    "status": "진행중",
    "documents": {
        "contract_file": "계약서.pdf"
    }
}
```

### 2.4 노무비 관리 API

#### 노무비 목록 조회
```http
GET /labor-costs
Authorization: Bearer {token}
```

#### 노무비 등록
```http
POST /labor-costs
Authorization: Bearer {token}
Content-Type: application/json

{
    "contract_id": "contract-uuid",
    "worker_name": "김일용",
    "work_date": "2024-03-20",
    "daily_wage": 150000,
    "work_type": "철근공사"
}
```

### 2.5 매출/지출 관리 API

#### 거래 목록 조회
```http
GET /transactions
Authorization: Bearer {token}
```

#### 거래 등록
```http
POST /transactions
Authorization: Bearer {token}
Content-Type: application/json

{
    "contract_id": "contract-uuid",
    "transaction_type": "income",
    "amount": 50000000,
    "transaction_date": "2024-03-20",
    "category": "계약금",
    "description": "1차 계약금 입금"
}
```

## 3. 에러 처리

### 3.1 에러 응답 형식
```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "에러 메시지"
    }
}
```

### 3.2 주요 에러 코드
- `AUTH_REQUIRED`: 인증 필요
- `INVALID_TOKEN`: 유효하지 않은 토큰
- `PERMISSION_DENIED`: 권한 없음
- `RESOURCE_NOT_FOUND`: 리소스를 찾을 수 없음
- `VALIDATION_ERROR`: 입력값 검증 실패

## 4. 보안

### 4.1 API 보안 정책
- HTTPS 사용
- Rate Limiting 적용
- CORS 설정
- 입력값 검증
- SQL Injection 방지

### 4.2 접근 제어
- 역할 기반 접근 제어 (RBAC)
- API 키 관리
- IP 화이트리스트

## 5. 성능 최적화

### 5.1 캐싱 전략
- Redis를 사용한 응답 캐싱
- 캐시 만료 시간 설정
- 조건부 캐싱

### 5.2 페이지네이션
- 기본 페이지 크기: 20
- 커서 기반 페이지네이션
- 정렬 옵션 지원 