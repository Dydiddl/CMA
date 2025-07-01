# 🔗 CMA 엔드포인트 상세 문서

## 📋 개요

이 문서는 CMA 시스템의 모든 API 엔드포인트에 대한 상세한 설명을 제공합니다. 각 엔드포인트의 기능, 요청/응답 형식, 예시, 에러 처리 등을 포함합니다.

## 🏗️ 엔드포인트 구조

### 전체 엔드포인트 맵
```
/api/v1/
├── /auth/                    # 인증 관련
│   ├── POST /login          # 로그인
│   ├── POST /refresh        # 토큰 갱신
│   └── POST /logout         # 로그아웃
├── /users/                   # 사용자 관리
│   ├── GET /                # 사용자 목록
│   ├── POST /               # 사용자 생성
│   ├── GET /{user_id}       # 사용자 상세
│   ├── PUT /{user_id}       # 사용자 수정
│   └── DELETE /{user_id}    # 사용자 삭제
├── /contracts/               # 계약 관리
│   ├── GET /                # 계약 목록
│   ├── POST /               # 계약 생성
│   ├── GET /{contract_id}   # 계약 상세
│   ├── PUT /{contract_id}   # 계약 수정
│   └── DELETE /{contract_id}# 계약 삭제
├── /labor/                   # 노무 관리
│   ├── GET /                # 노무 기록 목록
│   ├── POST /               # 노무 기록 생성
│   ├── GET /{labor_id}      # 노무 기록 상세
│   ├── PUT /{labor_id}      # 노무 기록 수정
│   └── DELETE /{labor_id}   # 노무 기록 삭제
├── /vendors/                 # 거래처 관리
│   ├── GET /                # 거래처 목록
│   ├── POST /               # 거래처 생성
│   ├── GET /{vendor_id}     # 거래처 상세
│   ├── PUT /{vendor_id}     # 거래처 수정
│   └── DELETE /{vendor_id}  # 거래처 삭제
├── /finance/                 # 재무 관리
│   ├── GET /                # 재무 기록 목록
│   ├── POST /               # 재무 기록 생성
│   ├── GET /{record_id}     # 재무 기록 상세
│   ├── PUT /{record_id}     # 재무 기록 수정
│   └── DELETE /{record_id}  # 재무 기록 삭제
└── /ascr/                    # ASCR 모듈
    ├── POST /extract-toc     # PDF 목차 추출
    ├── POST /split-pdf       # PDF 분할
    └── POST /generate-excel  # Excel 내역서 생성
```

## 🔐 인증 엔드포인트 (`/api/v1/auth`)

### 1. 로그인
```http
POST /api/v1/auth/login
```

**설명:** 사용자 인증 및 JWT 토큰 발급

**요청 본문:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**응답 (성공):**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "ADMIN"
    }
  },
  "message": "로그인이 성공했습니다."
}
```

**응답 (실패):**
```json
{
  "status": "error",
  "data": null,
  "message": "잘못된 사용자명 또는 비밀번호입니다.",
  "error_code": "AUTHENTICATION_ERROR"
}
```

### 2. 토큰 갱신
```http
POST /api/v1/auth/refresh
```

**설명:** 만료된 액세스 토큰을 갱신

**요청 헤더:**
```http
Authorization: Bearer <refresh_token>
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  },
  "message": "토큰이 갱신되었습니다."
}
```

### 3. 로그아웃
```http
POST /api/v1/auth/logout
```

**설명:** 사용자 로그아웃 및 토큰 무효화

**요청 헤더:**
```http
Authorization: Bearer <access_token>
```

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "로그아웃이 완료되었습니다."
}
```

## 👥 사용자 관리 엔드포인트 (`/api/v1/users`)

### 1. 사용자 목록 조회
```http
GET /api/v1/users/?skip=0&limit=10&search=admin&role=ADMIN
```

**설명:** 사용자 목록을 페이징과 검색으로 조회

**쿼리 파라미터:**
- `skip` (int): 건너뛸 레코드 수 (기본값: 0)
- `limit` (int): 가져올 레코드 수 (기본값: 10, 최대: 100)
- `search` (string): 검색어 (선택사항)
- `role` (string): 역할 필터 (선택사항)

**응답:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "ADMIN",
      "is_active": true,
      "created_at": "2024-01-23T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "message": null
}
```

### 2. 사용자 생성
```http
POST /api/v1/users/
```

**설명:** 새로운 사용자 생성 (관리자만 가능)

**요청 본문:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "password123",
  "role": "USER",
  "is_active": true
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": 2,
    "username": "newuser",
    "email": "newuser@example.com",
    "role": "USER",
    "is_active": true,
    "created_at": "2024-01-23T10:30:00Z"
  },
  "message": "사용자가 성공적으로 생성되었습니다."
}
```

### 3. 사용자 상세 조회
```http
GET /api/v1/users/{user_id}
```

**설명:** 특정 사용자의 상세 정보 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "ADMIN",
    "is_active": true,
    "last_login": "2024-01-23T10:30:00Z",
    "created_at": "2024-01-23T10:30:00Z",
    "updated_at": "2024-01-23T10:30:00Z"
  },
  "message": null
}
```

### 4. 사용자 수정
```http
PUT /api/v1/users/{user_id}
```

**설명:** 사용자 정보 수정

**요청 본문:**
```json
{
  "email": "updated@example.com",
  "role": "MANAGER",
  "is_active": true
}
```

### 5. 사용자 삭제
```http
DELETE /api/v1/users/{user_id}
```

**설명:** 사용자 삭제 (소프트 삭제)

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "사용자가 성공적으로 삭제되었습니다."
}
```

## 📋 계약 관리 엔드포인트 (`/api/v1/contracts`)

### 1. 계약 목록 조회
```http
GET /api/v1/contracts/?skip=0&limit=10&search=테스트&status=진행중&vendor_id=1
```

**설명:** 계약 목록을 다양한 필터로 조회

**쿼리 파라미터:**
- `skip` (int): 건너뛸 레코드 수
- `limit` (int): 가져올 레코드 수
- `search` (string): 검색어 (계약명, 계약번호, 발주처명)
- `status` (string): 상태 필터
- `vendor_id` (int): 거래처 ID 필터
- `start_date` (date): 시작일 필터
- `end_date` (date): 종료일 필터

**응답:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "테스트 계약",
      "contract_number": "CON-2024-001",
      "contract_amount": 1000000,
      "status": "진행중",
      "client_name": "테스트 발주처",
      "vendor_name": "테스트 거래처",
      "contract_date": "2024-01-23T00:00:00Z",
      "created_at": "2024-01-23T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "message": null
}
```

### 2. 계약 생성
```http
POST /api/v1/contracts/
```

**설명:** 새로운 계약 생성

**요청 본문:**
```json
{
  "name": "테스트 계약",
  "contract_number": "CON-2024-001",
  "contract_amount": 1000000,
  "contract_date": "2024-01-23T00:00:00Z",
  "start_date": "2024-01-23T00:00:00Z",
  "end_date": "2024-12-31T00:00:00Z",
  "client_name": "테스트 발주처",
  "client_contact": "010-1234-5678",
  "status": "진행중",
  "description": "테스트 계약입니다.",
  "vendor_id": 1
}
```

**검증 규칙:**
- `contract_number`: 고유해야 함
- `contract_amount`: 0보다 커야 함
- `end_date`: `start_date`보다 늦어야 함
- `client_name`: 필수 입력

### 3. 계약 상세 조회
```http
GET /api/v1/contracts/{contract_id}
```

**설명:** 계약 상세 정보 및 관련 데이터 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "테스트 계약",
    "contract_number": "CON-2024-001",
    "contract_amount": 1000000,
    "contract_date": "2024-01-23T00:00:00Z",
    "start_date": "2024-01-23T00:00:00Z",
    "end_date": "2024-12-31T00:00:00Z",
    "client_name": "테스트 발주처",
    "client_contact": "010-1234-5678",
    "status": "진행중",
    "description": "테스트 계약입니다.",
    "vendor_id": 1,
    "vendor_name": "테스트 거래처",
    "created_at": "2024-01-23T10:30:00Z",
    "updated_at": "2024-01-23T10:30:00Z"
  },
  "documents": [
    {
      "id": 1,
      "document_type": "계약서",
      "file_name": "contract.pdf",
      "upload_date": "2024-01-23T10:30:00Z",
      "description": "계약서 파일"
    }
  ],
  "financial_summary": {
    "total_income": 500000,
    "total_expense": 300000,
    "profit": 200000
  },
  "labor_summary": {
    "total_hours": 160,
    "total_cost": 2400000
  },
  "message": null
}
```

### 4. 계약 수정
```http
PUT /api/v1/contracts/{contract_id}
```

**설명:** 계약 정보 수정

**요청 본문:**
```json
{
  "name": "수정된 계약명",
  "status": "완료",
  "description": "수정된 설명",
  "end_date": "2024-06-30T00:00:00Z"
}
```

### 5. 계약 삭제
```http
DELETE /api/v1/contracts/{contract_id}
```

**설명:** 계약 삭제 (관련 데이터도 함께 삭제)

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "계약이 성공적으로 삭제되었습니다."
}
```

## 💰 재무 관리 엔드포인트 (`/api/v1/finance`)

### 1. 재무 기록 목록 조회
```http
GET /api/v1/finance/?skip=0&limit=10&type=지출&category=자재비&contract_id=1
```

**설명:** 재무 기록을 다양한 필터로 조회

**쿼리 파라미터:**
- `skip` (int): 건너뛸 레코드 수
- `limit` (int): 가져올 레코드 수
- `type` (string): 거래 유형 (수입/지출)
- `category` (string): 카테고리
- `contract_id` (int): 계약 ID
- `vendor_id` (int): 거래처 ID
- `start_date` (date): 시작일
- `end_date` (date): 종료일
- `status` (string): 지급 상태

**응답:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "contract_id": 1,
      "contract_name": "테스트 계약",
      "transaction_date": "2024-01-23",
      "amount": 500000,
      "type": "지출",
      "category": "자재비",
      "description": "시멘트 구매",
      "payment_method": "계좌이체",
      "status": "지급완료",
      "vendor_name": "테스트 거래처",
      "created_at": "2024-01-23T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "summary": {
    "total_income": 1000000,
    "total_expense": 500000,
    "net_profit": 500000
  },
  "message": null
}
```

### 2. 재무 기록 생성
```http
POST /api/v1/finance/
```

**설명:** 새로운 재무 기록 생성

**요청 본문:**
```json
{
  "contract_id": 1,
  "transaction_date": "2024-01-23",
  "amount": 500000,
  "type": "지출",
  "category": "자재비",
  "description": "시멘트 구매",
  "payment_method": "계좌이체",
  "status": "지급완료",
  "vendor_id": 1
}
```

**검증 규칙:**
- `amount`: 0보다 커야 함
- `type`: "수입" 또는 "지출"이어야 함
- `transaction_date`: 유효한 날짜여야 함

### 3. 재무 기록 상세 조회
```http
GET /api/v1/finance/{record_id}
```

**설명:** 재무 기록 상세 정보 및 관련 문서 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "contract_id": 1,
    "contract_name": "테스트 계약",
    "transaction_date": "2024-01-23",
    "amount": 500000,
    "type": "지출",
    "category": "자재비",
    "description": "시멘트 구매",
    "payment_method": "계좌이체",
    "status": "지급완료",
    "vendor_id": 1,
    "vendor_name": "테스트 거래처",
    "created_at": "2024-01-23T10:30:00Z",
    "updated_at": "2024-01-23T10:30:00Z"
  },
  "documents": [
    {
      "id": 1,
      "document_type": "영수증",
      "file_name": "receipt.pdf",
      "upload_date": "2024-01-23T10:30:00Z",
      "description": "시멘트 구매 영수증"
    }
  ],
  "message": null
}
```

### 4. 재무 기록 수정
```http
PUT /api/v1/finance/{record_id}
```

**설명:** 재무 기록 수정

**요청 본문:**
```json
{
  "amount": 550000,
  "description": "수정된 시멘트 구매",
  "status": "지급완료"
}
```

### 5. 재무 기록 삭제
```http
DELETE /api/v1/finance/{record_id}
```

**설명:** 재무 기록 삭제

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "재무 기록이 성공적으로 삭제되었습니다."
}
```

## 👷 노무 관리 엔드포인트 (`/api/v1/labor`)

### 1. 노무 기록 목록 조회
```http
GET /api/v1/labor/?skip=0&limit=10&contract_id=1&worker_id=1&work_date=2024-01-23
```

**설명:** 노무 기록을 다양한 필터로 조회

**쿼리 파라미터:**
- `skip` (int): 건너뛸 레코드 수
- `limit` (int): 가져올 레코드 수
- `contract_id` (int): 계약 ID
- `worker_id` (int): 근로자 ID
- `work_date` (date): 작업일
- `work_type` (string): 작업 유형
- `status` (string): 지급 상태

**응답:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "contract_id": 1,
      "contract_name": "테스트 계약",
      "worker_id": 1,
      "worker_name": "홍길동",
      "work_date": "2024-01-23",
      "hours_worked": 8.0,
      "hourly_rate": 15000,
      "total_amount": 120000,
      "work_type": "일반공사",
      "description": "콘크리트 타설 작업",
      "status": "미지급",
      "created_at": "2024-01-23T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "summary": {
    "total_hours": 8.0,
    "total_cost": 120000,
    "average_hourly_rate": 15000
  },
  "message": null
}
```

### 2. 노무 기록 생성
```http
POST /api/v1/labor/
```

**설명:** 새로운 노무 기록 생성

**요청 본문:**
```json
{
  "contract_id": 1,
  "worker_id": 1,
  "work_date": "2024-01-23",
  "hours_worked": 8.0,
  "hourly_rate": 15000,
  "total_amount": 120000,
  "work_type": "일반공사",
  "description": "콘크리트 타설 작업",
  "status": "미지급"
}
```

**검증 규칙:**
- `hours_worked`: 0보다 크고 24 이하여야 함
- `hourly_rate`: 0 이상이어야 함
- `total_amount`: `hours_worked * hourly_rate`와 일치해야 함

### 3. 노무 기록 상세 조회
```http
GET /api/v1/labor/{labor_id}
```

**설명:** 노무 기록 상세 정보 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "contract_id": 1,
    "contract_name": "테스트 계약",
    "worker_id": 1,
    "worker_name": "홍길동",
    "worker_position": "일반공",
    "work_date": "2024-01-23",
    "hours_worked": 8.0,
    "hourly_rate": 15000,
    "total_amount": 120000,
    "work_type": "일반공사",
    "description": "콘크리트 타설 작업",
    "status": "미지급",
    "created_at": "2024-01-23T10:30:00Z",
    "updated_at": "2024-01-23T10:30:00Z"
  },
  "message": null
}
```

### 4. 노무 기록 수정
```http
PUT /api/v1/labor/{labor_id}
```

**설명:** 노무 기록 수정

**요청 본문:**
```json
{
  "hours_worked": 9.0,
  "total_amount": 135000,
  "description": "수정된 콘크리트 타설 작업",
  "status": "지급완료"
}
```

### 5. 노무 기록 삭제
```http
DELETE /api/v1/labor/{labor_id}
```

**설명:** 노무 기록 삭제

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "노무 기록이 성공적으로 삭제되었습니다."
}
```

## 🏢 거래처 관리 엔드포인트 (`/api/v1/vendors`)

### 1. 거래처 목록 조회
```http
GET /api/v1/vendors/?skip=0&limit=10&search=테스트&vendor_type=자재업체
```

**설명:** 거래처 목록을 다양한 필터로 조회

**쿼리 파라미터:**
- `skip` (int): 건너뛸 레코드 수
- `limit` (int): 가져올 레코드 수
- `search` (string): 검색어 (거래처명, 연락처)
- `vendor_type` (string): 거래처 유형
- `status` (string): 상태 필터

**응답:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "테스트 거래처",
      "contact_person": "김철수",
      "contact_number": "010-1234-5678",
      "email": "test@vendor.com",
      "vendor_type": "자재업체",
      "status": "활성",
      "created_at": "2024-01-23T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "message": null
}
```

### 2. 거래처 생성
```http
POST /api/v1/vendors/
```

**설명:** 새로운 거래처 생성

**요청 본문:**
```json
{
  "name": "테스트 거래처",
  "contact_person": "김철수",
  "contact_number": "010-1234-5678",
  "email": "test@vendor.com",
  "address": "서울시 강남구 테스트로 123",
  "business_number": "123-45-67890",
  "vendor_type": "자재업체",
  "status": "활성"
}
```

### 3. 거래처 상세 조회
```http
GET /api/v1/vendors/{vendor_id}
```

**설명:** 거래처 상세 정보 및 관련 계약 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "테스트 거래처",
    "contact_person": "김철수",
    "contact_number": "010-1234-5678",
    "email": "test@vendor.com",
    "address": "서울시 강남구 테스트로 123",
    "business_number": "123-45-67890",
    "vendor_type": "자재업체",
    "status": "활성",
    "created_at": "2024-01-23T10:30:00Z",
    "updated_at": "2024-01-23T10:30:00Z"
  },
  "contracts": [
    {
      "id": 1,
      "name": "테스트 계약",
      "contract_number": "CON-2024-001",
      "contract_amount": 1000000,
      "status": "진행중"
    }
  ],
  "financial_summary": {
    "total_transactions": 5,
    "total_amount": 2500000
  },
  "message": null
}
```

### 4. 거래처 수정
```http
PUT /api/v1/vendors/{vendor_id}
```

**설명:** 거래처 정보 수정

**요청 본문:**
```json
{
  "contact_person": "이영희",
  "contact_number": "010-9876-5432",
  "email": "updated@vendor.com",
  "status": "활성"
}
```

### 5. 거래처 삭제
```http
DELETE /api/v1/vendors/{vendor_id}
```

**설명:** 거래처 삭제 (관련 계약이 없을 때만 가능)

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "거래처가 성공적으로 삭제되었습니다."
}
```

## 📄 ASCR 모듈 엔드포인트 (`/api/v1/ascr`)

### 1. PDF 목차 추출
```http
POST /api/v1/ascr/extract-toc
```

**설명:** PDF 파일에서 목차를 자동으로 추출

**요청 본문 (multipart/form-data):**
```
file: PDF 파일 (최대 50MB)
year: 2025 (선택사항)
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "year": 2025,
    "output_file": "/output/toc_2025.md",
    "extracted_sections": [
      {
        "section": "공통부문",
        "start_page": 1,
        "end_page": 50,
        "chapters": [
          {
            "title": "제1장 적용기준",
            "page": 3
          },
          {
            "title": "제2장 가설공사",
            "page": 33
          }
        ]
      },
      {
        "section": "토목부문",
        "start_page": 51,
        "end_page": 100,
        "chapters": [
          {
            "title": "제1장 토공",
            "page": 53
          }
        ]
      }
    ],
    "processing_time": 2.5,
    "file_size": "15.2MB",
    "total_pages": 150
  },
  "message": "목차 추출이 완료되었습니다."
}
```

### 2. PDF 분할
```http
POST /api/v1/ascr/split-pdf
```

**설명:** PDF 파일을 부문별로 분할

**요청 본문:**
```json
{
  "input_file": "/input/standard_2025.pdf",
  "sections": [
    {
      "name": "공통부문",
      "start_page": 1,
      "end_page": 50,
      "output_filename": "공통부문_2025.pdf"
    },
    {
      "name": "토목부문",
      "start_page": 51,
      "end_page": 100,
      "output_filename": "토목부문_2025.pdf"
    },
    {
      "name": "건축부문",
      "start_page": 101,
      "end_page": 150,
      "output_filename": "건축부문_2025.pdf"
    }
  ]
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "input_file": "/input/standard_2025.pdf",
    "output_files": [
      {
        "name": "공통부문",
        "filename": "공통부문_2025.pdf",
        "file_path": "/output/공통부문_2025.pdf",
        "pages": 50,
        "file_size": "5.2MB"
      },
      {
        "name": "토목부문",
        "filename": "토목부문_2025.pdf",
        "file_path": "/output/토목부문_2025.pdf",
        "pages": 50,
        "file_size": "4.8MB"
      },
      {
        "name": "건축부문",
        "filename": "건축부문_2025.pdf",
        "file_path": "/output/건축부문_2025.pdf",
        "pages": 50,
        "file_size": "5.5MB"
      }
    ],
    "processing_time": 8.3,
    "total_pages": 150
  },
  "message": "PDF 분할이 완료되었습니다."
}
```

### 3. Excel 내역서 생성
```http
POST /api/v1/ascr/generate-excel
```

**설명:** 계약 정보를 바탕으로 Excel 내역서 생성

**요청 본문:**
```json
{
  "contract_id": 1,
  "sections": ["공통부문", "토목부문"],
  "template_type": "standard",
  "include_pricing": true,
  "include_descriptions": true
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "contract_id": 1,
    "contract_name": "테스트 계약",
    "output_file": "/output/내역서_CON-2024-001.xlsx",
    "sections": ["공통부문", "토목부문"],
    "total_items": 150,
    "file_size": "2.1MB",
    "processing_time": 3.2,
    "generated_at": "2024-01-23T10:30:00Z"
  },
  "message": "Excel 내역서가 성공적으로 생성되었습니다."
}
```

## 📊 통계 및 대시보드 엔드포인트

### 1. 전체 통계 조회
```http
GET /api/v1/dashboard/stats
```

**설명:** 시스템 전체 통계 정보 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "contracts": {
      "total": 25,
      "active": 15,
      "completed": 8,
      "cancelled": 2,
      "total_amount": 50000000
    },
    "financial": {
      "total_income": 45000000,
      "total_expense": 35000000,
      "net_profit": 10000000,
      "pending_payments": 5000000
    },
    "labor": {
      "total_workers": 45,
      "total_hours": 3200,
      "total_cost": 48000000,
      "average_hourly_rate": 15000
    },
    "vendors": {
      "total": 12,
      "active": 10,
      "inactive": 2
    }
  },
  "message": null
}
```

### 2. 계약별 통계
```http
GET /api/v1/dashboard/contracts/{contract_id}/stats
```

**설명:** 특정 계약의 상세 통계 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "contract_info": {
      "id": 1,
      "name": "테스트 계약",
      "contract_amount": 10000000,
      "status": "진행중"
    },
    "financial_summary": {
      "total_income": 8000000,
      "total_expense": 6000000,
      "profit_margin": 25.0,
      "payment_status": "지급완료"
    },
    "labor_summary": {
      "total_workers": 8,
      "total_hours": 640,
      "total_cost": 9600000,
      "efficiency_rate": 96.0
    },
    "progress": {
      "physical_progress": 75.0,
      "financial_progress": 80.0,
      "schedule_progress": 70.0
    }
  },
  "message": null
}
```

## 🔧 유틸리티 엔드포인트

### 1. 파일 업로드
```http
POST /api/v1/utils/upload
```

**설명:** 파일 업로드 (문서, 이미지 등)

**요청 본문 (multipart/form-data):**
```
file: 파일
category: 문서 유형 (contract, financial, labor)
description: 파일 설명 (선택사항)
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "file_id": "uuid-string",
    "filename": "document.pdf",
    "file_path": "/uploads/contracts/document.pdf",
    "file_size": 1024000,
    "mime_type": "application/pdf",
    "upload_date": "2024-01-23T10:30:00Z"
  },
  "message": "파일이 성공적으로 업로드되었습니다."
}
```

### 2. 파일 다운로드
```http
GET /api/v1/utils/download/{file_id}
```

**설명:** 업로드된 파일 다운로드

**응답:** 파일 바이너리 데이터

### 3. 시스템 상태 확인
```http
GET /api/v1/utils/health
```

**설명:** 시스템 상태 및 서비스 가용성 확인

**응답:**
```json
{
  "status": "success",
  "data": {
    "system": "healthy",
    "database": "connected",
    "cache": "connected",
    "storage": "available",
    "version": "1.0.0",
    "uptime": 86400,
    "timestamp": "2024-01-23T10:30:00Z"
  },
  "message": "시스템이 정상적으로 작동 중입니다."
}
```

## 📋 에러 처리 및 응답 코드

### 공통 에러 응답 형식
```json
{
  "status": "error",
  "data": null,
  "message": "에러 메시지",
  "error_code": "ERROR_CODE",
  "details": {
    "field": "에러가 발생한 필드",
    "value": "문제가 된 값",
    "constraint": "위반된 제약조건"
  },
  "timestamp": "2024-01-23T10:30:00Z"
}
```

### 주요 에러 코드
```python
ERROR_CODES = {
    # 인증 관련
    "AUTHENTICATION_ERROR": "인증 실패",
    "AUTHORIZATION_ERROR": "권한 없음",
    "TOKEN_EXPIRED": "토큰 만료",
    "INVALID_TOKEN": "유효하지 않은 토큰",
    
    # 데이터 검증
    "VALIDATION_ERROR": "입력 데이터 검증 실패",
    "REQUIRED_FIELD_MISSING": "필수 필드 누락",
    "INVALID_FORMAT": "잘못된 형식",
    "DUPLICATE_VALUE": "중복된 값",
    
    # 리소스 관련
    "RESOURCE_NOT_FOUND": "리소스를 찾을 수 없음",
    "RESOURCE_ALREADY_EXISTS": "리소스가 이미 존재함",
    "RESOURCE_IN_USE": "리소스가 사용 중임",
    
    # 비즈니스 로직
    "INSUFFICIENT_PERMISSIONS": "권한 부족",
    "BUSINESS_RULE_VIOLATION": "비즈니스 규칙 위반",
    "INVALID_STATE_TRANSITION": "잘못된 상태 전환",
    
    # 시스템 오류
    "DATABASE_ERROR": "데이터베이스 오류",
    "FILE_PROCESSING_ERROR": "파일 처리 오류",
    "EXTERNAL_SERVICE_ERROR": "외부 서비스 오류",
    "INTERNAL_SERVER_ERROR": "내부 서버 오류"
}
```

이 엔드포인트 문서를 통해 **완전하고 일관된** API 서비스를 제공할 수 있습니다. 