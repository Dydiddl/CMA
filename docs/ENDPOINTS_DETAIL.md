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

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "username": "admin",
    "email": "updated@example.com",
    "role": "MANAGER",
    "is_active": true,
    "updated_at": "2024-01-23T10:30:00Z"
  },
  "message": "사용자 정보가 성공적으로 수정되었습니다."
}
```

### 5. 사용자 삭제
```http
DELETE /api/v1/users/{user_id}
```

**설명:** 사용자 삭제 (관리자만 가능)

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
GET /api/v1/contracts/?page=1&limit=20&search=아파트&status=진행중
```

**설명:** 계약 목록을 페이징과 검색으로 조회

**쿼리 파라미터:**
- `page` (int): 페이지 번호 (기본값: 1)
- `limit` (int): 페이지당 항목 수 (기본값: 20)
- `search` (string): 검색어 (프로젝트명)
- `status` (string): 계약 상태 (진행중, 완료, 취소)
- `vendor_id` (string): 거래처 ID
- `start_date` (date): 시작일
- `end_date` (date): 종료일
- `sort` (string): 정렬 기준 (created_at, contract_date, contract_amount)
- `order` (string): 정렬 방향 (asc, desc)

**응답:**
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "contract-uuid",
        "project_name": "아파트 신축공사",
        "contract_amount": 1000000000,
        "contract_date": "2024-03-20",
        "vendor": {
          "id": "vendor-uuid",
          "company_name": "건설회사"
        },
        "status": "진행중",
        "created_at": "2024-03-20T10:00:00Z"
      }
    ],
    "total": 200,
    "page": 1,
    "limit": 20
  },
  "message": "계약 목록을 성공적으로 조회했습니다."
}
```

### 2. 계약 상세 조회
```http
GET /api/v1/contracts/{contract_id}
```

**설명:** 특정 계약의 상세 정보 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "contract-uuid",
    "project_name": "아파트 신축공사",
    "contract_amount": 1000000000,
    "contract_date": "2024-03-20",
    "vendor": {
      "id": "vendor-uuid",
      "company_name": "건설회사",
      "representative": "김대표"
    },
    "status": "진행중",
    "documents": {
      "contract_file": "계약서.pdf",
      "attachments": [
        "부록1.pdf",
        "부록2.pdf"
      ]
    },
    "payments": [
      {
        "id": "payment-uuid",
        "amount": 300000000,
        "due_date": "2024-04-20",
        "status": "미지급"
      }
    ],
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T15:30:00Z"
  },
  "message": "계약 정보를 성공적으로 조회했습니다."
}
```

### 3. 계약 생성
```http
POST /api/v1/contracts
```

**설명:** 새로운 계약 생성

**요청 본문:**
```json
{
  "project_name": "아파트 신축공사",
  "contract_amount": 1000000000,
  "contract_date": "2024-03-20",
  "vendor_id": "vendor-uuid",
  "status": "진행중",
  "documents": {
    "contract_file": "계약서.pdf",
    "attachments": [
      "부록1.pdf",
      "부록2.pdf"
    ]
  }
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "contract-uuid",
    "project_name": "아파트 신축공사",
    "contract_amount": 1000000000,
    "contract_date": "2024-03-20",
    "vendor": {
      "id": "vendor-uuid",
      "company_name": "건설회사"
    },
    "status": "진행중",
    "documents": {
      "contract_file": "계약서.pdf",
      "attachments": [
        "부록1.pdf",
        "부록2.pdf"
      ]
    },
    "created_at": "2024-03-20T10:00:00Z"
  },
  "message": "계약이 성공적으로 등록되었습니다."
}
```

### 4. 계약 수정
```http
PUT /api/v1/contracts/{contract_id}
```

**설명:** 기존 계약 정보 수정

**요청 본문:**
```json
{
  "status": "완료",
  "documents": {
    "attachments": [
      "부록1.pdf",
      "부록2.pdf",
      "부록3.pdf"
    ]
  }
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "contract-uuid",
    "project_name": "아파트 신축공사",
    "contract_amount": 1000000000,
    "contract_date": "2024-03-20",
    "vendor": {
      "id": "vendor-uuid",
      "company_name": "건설회사"
    },
    "status": "완료",
    "documents": {
      "contract_file": "계약서.pdf",
      "attachments": [
        "부록1.pdf",
        "부록2.pdf",
        "부록3.pdf"
      ]
    },
    "updated_at": "2024-03-20T16:00:00Z"
  },
  "message": "계약 정보가 성공적으로 수정되었습니다."
}
```

### 5. 계약 삭제
```http
DELETE /api/v1/contracts/{contract_id}
```

**설명:** 계약 삭제

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "계약이 성공적으로 삭제되었습니다."
}
```

## 👷 노무 관리 엔드포인트 (`/api/v1/labor-costs`)

### 1. 노무비 목록 조회
```http
GET /api/v1/labor-costs/?page=1&limit=20&contract_id=contract-uuid&worker_name=김일용
```

**설명:** 노무비 목록을 페이징과 검색으로 조회

**쿼리 파라미터:**
- `page` (int): 페이지 번호 (기본값: 1)
- `limit` (int): 페이지당 항목 수 (기본값: 20)
- `contract_id` (string): 계약 ID
- `worker_name` (string): 작업자 이름
- `work_type` (string): 작업 유형
- `start_date` (date): 시작일
- `end_date` (date): 종료일
- `sort` (string): 정렬 기준 (work_date, daily_wage)
- `order` (string): 정렬 방향 (asc, desc)

**응답:**
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "labor-cost-uuid",
        "contract": {
          "id": "contract-uuid",
          "project_name": "아파트 신축공사"
        },
        "worker_name": "김일용",
        "work_date": "2024-03-20",
        "daily_wage": 150000,
        "work_type": "철근공사",
        "created_at": "2024-03-20T10:00:00Z"
      }
    ],
    "total": 200,
    "page": 1,
    "limit": 20
  },
  "message": "노무비 목록을 성공적으로 조회했습니다."
}
```

### 2. 노무비 상세 조회
```http
GET /api/v1/labor-costs/{labor_cost_id}
```

**설명:** 특정 노무비의 상세 정보 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "labor-cost-uuid",
    "contract": {
      "id": "contract-uuid",
      "project_name": "아파트 신축공사",
      "vendor": {
        "id": "vendor-uuid",
        "company_name": "건설회사"
      }
    },
    "worker_name": "김일용",
    "work_date": "2024-03-20",
    "daily_wage": 150000,
    "work_type": "철근공사",
    "work_details": "1층 철근 배근 작업",
    "payment_status": "미지급",
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T15:30:00Z"
  },
  "message": "노무비 정보를 성공적으로 조회했습니다."
}
```

### 3. 노무비 생성
```http
POST /api/v1/labor-costs
```

**설명:** 새로운 노무비 기록 생성

**요청 본문:**
```json
{
  "contract_id": "contract-uuid",
  "worker_name": "김일용",
  "work_date": "2024-03-20",
  "daily_wage": 150000,
  "work_type": "철근공사",
  "work_details": "1층 철근 배근 작업"
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "labor-cost-uuid",
    "contract": {
      "id": "contract-uuid",
      "project_name": "아파트 신축공사"
    },
    "worker_name": "김일용",
    "work_date": "2024-03-20",
    "daily_wage": 150000,
    "work_type": "철근공사",
    "work_details": "1층 철근 배근 작업",
    "payment_status": "미지급",
    "created_at": "2024-03-20T10:00:00Z"
  },
  "message": "노무비가 성공적으로 등록되었습니다."
}
```

### 4. 노무비 수정
```http
PUT /api/v1/labor-costs/{labor_cost_id}
```

**설명:** 기존 노무비 정보 수정

**요청 본문:**
```json
{
  "daily_wage": 160000,
  "work_details": "1층 철근 배근 작업 수정",
  "payment_status": "지급완료"
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "labor-cost-uuid",
    "contract": {
      "id": "contract-uuid",
      "project_name": "아파트 신축공사"
    },
    "worker_name": "김일용",
    "work_date": "2024-03-20",
    "daily_wage": 160000,
    "work_type": "철근공사",
    "work_details": "1층 철근 배근 작업 수정",
    "payment_status": "지급완료",
    "updated_at": "2024-03-20T16:00:00Z"
  },
  "message": "노무비 정보가 성공적으로 수정되었습니다."
}
```

### 5. 노무비 삭제
```http
DELETE /api/v1/labor-costs/{labor_cost_id}
```

**설명:** 노무비 기록 삭제

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "노무비가 성공적으로 삭제되었습니다."
}
```

## 🏢 거래처 관리 엔드포인트 (`/api/v1/vendors`)

### 1. 거래처 목록 조회
```http
GET /api/v1/vendors/?page=1&limit=20&search=건설&status=활성
```

**설명:** 거래처 목록을 페이징과 검색으로 조회

**쿼리 파라미터:**
- `page` (int): 페이지 번호 (기본값: 1)
- `limit` (int): 페이지당 항목 수 (기본값: 20)
- `search` (string): 검색어 (회사명, 대표자명)
- `status` (string): 상태 필터 (활성, 비활성)
- `vendor_type` (string): 거래처 유형
- `sort` (string): 정렬 기준 (company_name, created_at)
- `order` (string): 정렬 방향 (asc, desc)

**응답:**
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "vendor-uuid",
        "company_name": "건설회사",
        "business_number": "123-45-67890",
        "representative": "김대표",
        "contact_phone": "02-1234-5678",
        "status": "활성",
        "created_at": "2024-03-20T10:00:00Z"
      }
    ],
    "total": 50,
    "page": 1,
    "limit": 20
  },
  "message": "거래처 목록을 성공적으로 조회했습니다."
}
```

### 2. 거래처 상세 조회
```http
GET /api/v1/vendors/{vendor_id}
```

**설명:** 특정 거래처의 상세 정보 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "vendor-uuid",
    "company_name": "건설회사",
    "business_number": "123-45-67890",
    "representative": "김대표",
    "contact_phone": "02-1234-5678",
    "email": "contact@construction.com",
    "address": "서울시 강남구 테헤란로 123",
    "vendor_type": "건설업",
    "status": "활성",
    "contracts": [
      {
        "id": "contract-uuid",
        "project_name": "아파트 신축공사",
        "contract_amount": 1000000000,
        "status": "진행중"
      }
    ],
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T15:30:00Z"
  },
  "message": "거래처 정보를 성공적으로 조회했습니다."
}
```

### 3. 거래처 생성
```http
POST /api/v1/vendors
```

**설명:** 새로운 거래처 생성

**요청 본문:**
```json
{
  "company_name": "새로운 건설회사",
  "business_number": "987-65-43210",
  "representative": "이대표",
  "contact_phone": "02-9876-5432",
  "email": "contact@newconstruction.com",
  "address": "서울시 서초구 강남대로 456",
  "vendor_type": "건설업",
  "status": "활성"
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "vendor-uuid",
    "company_name": "새로운 건설회사",
    "business_number": "987-65-43210",
    "representative": "이대표",
    "contact_phone": "02-9876-5432",
    "email": "contact@newconstruction.com",
    "address": "서울시 서초구 강남대로 456",
    "vendor_type": "건설업",
    "status": "활성",
    "created_at": "2024-03-20T10:00:00Z"
  },
  "message": "거래처가 성공적으로 등록되었습니다."
}
```

### 4. 거래처 수정
```http
PUT /api/v1/vendors/{vendor_id}
```

**설명:** 기존 거래처 정보 수정

**요청 본문:**
```json
{
  "contact_phone": "02-9999-8888",
  "email": "updated@construction.com",
  "status": "비활성"
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "vendor-uuid",
    "company_name": "건설회사",
    "business_number": "123-45-67890",
    "representative": "김대표",
    "contact_phone": "02-9999-8888",
    "email": "updated@construction.com",
    "address": "서울시 강남구 테헤란로 123",
    "vendor_type": "건설업",
    "status": "비활성",
    "updated_at": "2024-03-20T16:00:00Z"
  },
  "message": "거래처 정보가 성공적으로 수정되었습니다."
}
```

### 5. 거래처 삭제
```http
DELETE /api/v1/vendors/{vendor_id}
```

**설명:** 거래처 삭제

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "거래처가 성공적으로 삭제되었습니다."
}
```

## 💰 재무 관리 엔드포인트 (`/api/v1/transactions`)

### 1. 거래 내역 목록 조회
```http
GET /api/v1/transactions/?page=1&limit=20&type=수입&contract_id=contract-uuid
```

**설명:** 재무 거래 내역을 페이징과 검색으로 조회

**쿼리 파라미터:**
- `page` (int): 페이지 번호 (기본값: 1)
- `limit` (int): 페이지당 항목 수 (기본값: 20)
- `type` (string): 거래 유형 (수입, 지출)
- `contract_id` (string): 계약 ID
- `category` (string): 카테고리 (자재비, 노무비, 경비 등)
- `start_date` (date): 시작일
- `end_date` (date): 종료일
- `sort` (string): 정렬 기준 (transaction_date, amount)
- `order` (string): 정렬 방향 (asc, desc)

**응답:**
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "transaction-uuid",
        "contract": {
          "id": "contract-uuid",
          "project_name": "아파트 신축공사"
        },
        "type": "수입",
        "amount": 50000000,
        "category": "계약금",
        "transaction_date": "2024-03-20",
        "description": "1차 계약금 지급",
        "status": "완료",
        "created_at": "2024-03-20T10:00:00Z"
      }
    ],
    "total": 200,
    "page": 1,
    "limit": 20
  },
  "message": "거래 내역을 성공적으로 조회했습니다."
}
```

### 2. 거래 내역 상세 조회
```http
GET /api/v1/transactions/{transaction_id}
```

**설명:** 특정 거래 내역의 상세 정보 조회

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "transaction-uuid",
    "contract": {
      "id": "contract-uuid",
      "project_name": "아파트 신축공사",
      "vendor": {
        "id": "vendor-uuid",
        "company_name": "건설회사"
      }
    },
    "type": "수입",
    "amount": 50000000,
    "category": "계약금",
    "transaction_date": "2024-03-20",
    "description": "1차 계약금 지급",
    "payment_method": "계좌이체",
    "status": "완료",
    "attachments": [
      "세금계산서.pdf",
      "입금확인서.pdf"
    ],
    "created_at": "2024-03-20T10:00:00Z",
    "updated_at": "2024-03-20T15:30:00Z"
  },
  "message": "거래 내역을 성공적으로 조회했습니다."
}
```

### 3. 거래 내역 생성
```http
POST /api/v1/transactions
```

**설명:** 새로운 거래 내역 생성

**요청 본문:**
```json
{
  "contract_id": "contract-uuid",
  "type": "수입",
  "amount": 50000000,
  "category": "계약금",
  "transaction_date": "2024-03-20",
  "description": "1차 계약금 지급",
  "payment_method": "계좌이체",
  "status": "완료"
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "transaction-uuid",
    "contract": {
      "id": "contract-uuid",
      "project_name": "아파트 신축공사"
    },
    "type": "수입",
    "amount": 50000000,
    "category": "계약금",
    "transaction_date": "2024-03-20",
    "description": "1차 계약금 지급",
    "payment_method": "계좌이체",
    "status": "완료",
    "created_at": "2024-03-20T10:00:00Z"
  },
  "message": "거래 내역이 성공적으로 등록되었습니다."
}
```

### 4. 거래 내역 수정
```http
PUT /api/v1/transactions/{transaction_id}
```

**설명:** 기존 거래 내역 정보 수정

**요청 본문:**
```json
{
  "amount": 55000000,
  "description": "1차 계약금 지급 (수정)",
  "status": "완료"
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "transaction-uuid",
    "contract": {
      "id": "contract-uuid",
      "project_name": "아파트 신축공사"
    },
    "type": "수입",
    "amount": 55000000,
    "category": "계약금",
    "transaction_date": "2024-03-20",
    "description": "1차 계약금 지급 (수정)",
    "payment_method": "계좌이체",
    "status": "완료",
    "updated_at": "2024-03-20T16:00:00Z"
  },
  "message": "거래 내역이 성공적으로 수정되었습니다."
}
```

### 5. 거래 내역 삭제
```http
DELETE /api/v1/transactions/{transaction_id}
```

**설명:** 거래 내역 삭제

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "거래 내역이 성공적으로 삭제되었습니다."
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

### API별 특정 에러 코드
```python
# 계약 관리 에러 코드
CONTRACT_ERROR_CODES = {
    "CONTRACT_NOT_FOUND": "계약을 찾을 수 없음",
    "VENDOR_NOT_FOUND": "거래처를 찾을 수 없음",
    "INVALID_STATUS": "잘못된 계약 상태"
}

# 노무 관리 에러 코드
LABOR_ERROR_CODES = {
    "LABOR_COST_NOT_FOUND": "노무비를 찾을 수 없음",
    "CONTRACT_NOT_FOUND": "계약을 찾을 수 없음",
    "INVALID_PAYMENT_STATUS": "잘못된 지급 상태"
}

# 거래처 관리 에러 코드
VENDOR_ERROR_CODES = {
    "VENDOR_NOT_FOUND": "거래처를 찾을 수 없음",
    "DUPLICATE_BUSINESS_NUMBER": "중복된 사업자등록번호"
}

# 재무 관리 에러 코드
TRANSACTION_ERROR_CODES = {
    "TRANSACTION_NOT_FOUND": "거래 내역을 찾을 수 없음",
    "INVALID_AMOUNT": "잘못된 금액",
    "INVALID_TRANSACTION_TYPE": "잘못된 거래 유형"
}
```

### API별 요청 제한
```python
RATE_LIMITS = {
    # 인증 API
    "auth_login": "1분에 5회",
    "auth_refresh": "1분에 10회",
    
    # 조회 API
    "contracts_list": "1초에 30회",
    "contracts_detail": "1초에 30회",
    "labor_costs_list": "1초에 30회",
    "labor_costs_detail": "1초에 30회",
    "vendors_list": "1초에 30회",
    "vendors_detail": "1초에 30회",
    "transactions_list": "1초에 30회",
    "transactions_detail": "1초에 30회",
    
    # 생성/수정 API
    "contracts_create": "1분에 10회",
    "contracts_update": "1분에 10회",
    "labor_costs_create": "1분에 10회",
    "labor_costs_update": "1분에 10회",
    "vendors_create": "1분에 10회",
    "vendors_update": "1분에 10회",
    "transactions_create": "1분에 10회",
    "transactions_update": "1분에 10회",
    
    # 삭제 API
    "contracts_delete": "1분에 5회",
    "labor_costs_delete": "1분에 5회",
    "vendors_delete": "1분에 5회",
    "transactions_delete": "1분에 5회"
}
```

### 성능 최적화 가이드
1. **캐싱 활용**: 자주 조회되는 데이터는 캐시 사용
2. **페이징**: 대용량 데이터는 페이징 처리
3. **필터링**: 필요한 데이터만 조회
4. **인덱스**: 자주 검색되는 필드에 인덱스 설정

이 엔드포인트 문서를 통해 **완전하고 일관된** API 서비스를 제공할 수 있습니다. 