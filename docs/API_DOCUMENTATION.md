# 🔌 CMA API 문서

## 📋 개요

CMA API는 **RESTful API** 설계 원칙을 따르며, **FastAPI** 기반으로 구축되었습니다. 모든 API는 JSON 형식으로 데이터를 주고받으며, **JWT 토큰 기반 인증**을 사용합니다.

### 🎯 API 특징
- **RESTful 설계**: 표준 HTTP 메서드 사용
- **비동기 처리**: asyncio 기반 고성능 API
- **자동 문서화**: FastAPI 자동 문서 생성
- **타입 안전성**: Pydantic 스키마 검증
- **표준화된 응답**: 일관된 응답 형식

## 🔗 API 기본 정보

### 기본 URL
```
개발 환경: http://localhost:8000
프로덕션: https://api.cma-system.com
```

### API 버전
```
현재 버전: v1
기본 경로: /api/v1
```

### 인증 방식
```http
Authorization: Bearer <JWT_TOKEN>
```

### 공통 응답 형식
```json
{
  "status": "success|error",
  "data": {},
  "message": "응답 메시지",
  "timestamp": "2024-01-23T10:30:00Z"
}
```

## 📊 API 엔드포인트 목록

### 1. 계약 관리 API (`/api/v1/contracts`)

#### 계약 생성
```http
POST /api/v1/contracts/
```

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
  "vendor_id": "1"
}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "1",
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
    "vendor_id": "1",
    "created_at": "2024-01-23T10:30:00Z",
    "updated_at": "2024-01-23T10:30:00Z"
  },
  "message": "계약이 성공적으로 생성되었습니다."
}
```

#### 계약 목록 조회
```http
GET /api/v1/contracts/?skip=0&limit=10&search=테스트&status=진행중
```

**쿼리 파라미터:**
- `skip` (int): 건너뛸 레코드 수 (기본값: 0)
- `limit` (int): 가져올 레코드 수 (기본값: 10, 최대: 100)
- `search` (string): 검색어 (선택사항)
- `status` (string): 상태 필터 (선택사항)

**응답:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "1",
      "name": "테스트 계약",
      "contract_number": "CON-2024-001",
      "contract_amount": 1000000,
      "status": "진행중",
      "client_name": "테스트 발주처",
      "created_at": "2024-01-23T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "message": null
}
```

#### 계약 상세 조회
```http
GET /api/v1/contracts/{contract_id}
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": "1",
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
    "vendor_id": "1",
    "created_at": "2024-01-23T10:30:00Z",
    "updated_at": "2024-01-23T10:30:00Z"
  },
  "documents": [
    {
      "id": "1",
      "document_type": "계약서",
      "file_name": "contract.pdf",
      "upload_date": "2024-01-23T10:30:00Z"
    }
  ],
  "message": null
}
```

#### 계약 수정
```http
PUT /api/v1/contracts/{contract_id}
```

**요청 본문:**
```json
{
  "name": "수정된 계약명",
  "status": "완료",
  "description": "수정된 설명"
}
```

#### 계약 삭제
```http
DELETE /api/v1/contracts/{contract_id}
```

**응답:**
```json
{
  "status": "success",
  "data": null,
  "message": "계약이 성공적으로 삭제되었습니다."
}
```

### 2. 재무 관리 API (`/api/v1/financial`)

#### 재무 기록 생성
```http
POST /api/v1/financial/
```

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

#### 재무 기록 목록 조회
```http
GET /api/v1/financial/?skip=0&limit=10&type=지출&category=자재비&contract_id=1
```

**쿼리 파라미터:**
- `skip` (int): 건너뛸 레코드 수
- `limit` (int): 가져올 레코드 수
- `type` (string): 거래 유형 (수입/지출)
- `category` (string): 카테고리
- `start_date` (date): 시작일
- `end_date` (date): 종료일
- `contract_id` (int): 계약 ID
- `vendor_id` (int): 거래처 ID

#### 재무 기록 상세 조회
```http
GET /api/v1/financial/{record_id}
```

#### 재무 기록 수정
```http
PUT /api/v1/financial/{record_id}
```

#### 재무 기록 삭제
```http
DELETE /api/v1/financial/{record_id}
```

#### 재무 문서 추가
```http
POST /api/v1/financial/{record_id}/documents
```

**요청 본문:**
```json
{
  "document_type": "영수증",
  "file_path": "/uploads/receipt.pdf",
  "file_name": "receipt.pdf",
  "description": "시멘트 구매 영수증"
}
```

### 3. 노무 관리 API (`/api/v1/labor`)

#### 노무 기록 생성
```http
POST /api/v1/labor/
```

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

#### 노무 기록 목록 조회
```http
GET /api/v1/labor/?skip=0&limit=10&contract_id=1&worker_id=1&work_date=2024-01-23
```

#### 노무 기록 상세 조회
```http
GET /api/v1/labor/{labor_id}
```

#### 노무 기록 수정
```http
PUT /api/v1/labor/{labor_id}
```

#### 노무 기록 삭제
```http
DELETE /api/v1/labor/{labor_id}
```

### 4. ASCR API (`/api/v1/ascr`)

#### PDF 목차 추출
```http
POST /api/v1/ascr/extract-toc
```

**요청 본문 (multipart/form-data):**
```
file: PDF 파일
year: 2025
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
        "end_page": 50
      },
      {
        "section": "토목부문",
        "start_page": 51,
        "end_page": 100
      }
    ],
    "processing_time": 2.5
  },
  "message": "목차 추출이 완료되었습니다."
}
```

#### PDF 분할
```http
POST /api/v1/ascr/split-pdf
```

**요청 본문:**
```json
{
  "input_file": "/input/standard_2025.pdf",
  "sections": [
    {
      "name": "공통부문",
      "start_page": 1,
      "end_page": 50
    },
    {
      "name": "토목부문",
      "start_page": 51,
      "end_page": 100
    }
  ]
}
```

#### Excel 내역서 생성
```http
POST /api/v1/ascr/generate-excel
```

**요청 본문:**
```json
{
  "contract_id": 1,
  "sections": ["공통부문", "토목부문"],
  "template_type": "standard"
}
```

## 🔒 인증 및 권한

### JWT 토큰 발급
```http
POST /api/v1/auth/login
```

**요청 본문:**
```json
{
  "username": "admin",
  "password": "password123"
}
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
  "message": "로그인이 성공했습니다."
}
```

### 토큰 갱신
```http
POST /api/v1/auth/refresh
```

**요청 헤더:**
```http
Authorization: Bearer <refresh_token>
```

### 권한 레벨
```python
PERMISSION_LEVELS = {
    "ADMIN": {
        "description": "관리자",
        "permissions": ["READ", "WRITE", "DELETE", "MANAGE_USERS"]
    },
    "MANAGER": {
        "description": "매니저",
        "permissions": ["READ", "WRITE", "DELETE"]
    },
    "USER": {
        "description": "일반 사용자",
        "permissions": ["READ", "WRITE"]
    },
    "VIEWER": {
        "description": "조회자",
        "permissions": ["READ"]
    }
}
```

## 📊 에러 처리

### HTTP 상태 코드
- `200 OK`: 요청 성공
- `201 Created`: 리소스 생성 성공
- `400 Bad Request`: 잘못된 요청
- `401 Unauthorized`: 인증 필요
- `403 Forbidden`: 권한 없음
- `404 Not Found`: 리소스를 찾을 수 없음
- `422 Unprocessable Entity`: 유효성 검증 실패
- `500 Internal Server Error`: 서버 오류

### 에러 응답 형식
```json
{
  "status": "error",
  "data": null,
  "message": "계약을 찾을 수 없습니다.",
  "error_code": "CONTRACT_NOT_FOUND",
  "timestamp": "2024-01-23T10:30:00Z"
}
```

### 주요 에러 코드
```python
ERROR_CODES = {
    "VALIDATION_ERROR": "입력 데이터 검증 실패",
    "AUTHENTICATION_ERROR": "인증 실패",
    "AUTHORIZATION_ERROR": "권한 없음",
    "RESOURCE_NOT_FOUND": "리소스를 찾을 수 없음",
    "DUPLICATE_RESOURCE": "중복된 리소스",
    "DATABASE_ERROR": "데이터베이스 오류",
    "FILE_PROCESSING_ERROR": "파일 처리 오류",
    "EXTERNAL_SERVICE_ERROR": "외부 서비스 오류"
}
```

## 📈 성능 최적화

### 캐싱 전략
```python
# 캐시 설정
CACHE_CONFIG = {
    "contracts": {
        "ttl": 3600,  # 1시간
        "key_pattern": "contract:{contract_id}"
    },
    "financial_records": {
        "ttl": 1800,  # 30분
        "key_pattern": "financial:{record_id}"
    },
    "labor_records": {
        "ttl": 1800,  # 30분
        "key_pattern": "labor:{labor_id}"
    }
}
```

### 페이징 최적화
```python
# 페이징 설정
PAGINATION_CONFIG = {
    "default_page_size": 10,
    "max_page_size": 100,
    "default_skip": 0
}
```

### 쿼리 최적화
```python
# 쿼리 최적화 설정
QUERY_OPTIMIZATION = {
    "use_indexes": True,
    "prefetch_related": True,
    "select_related": True,
    "batch_size": 100
}
```

## 🔧 API 테스트

### curl 예시
```bash
# 계약 생성
curl -X POST "http://localhost:8000/api/v1/contracts/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "테스트 계약",
    "contract_number": "CON-2024-001",
    "contract_amount": 1000000,
    "contract_date": "2024-01-23T00:00:00Z",
    "client_name": "테스트 발주처",
    "vendor_id": "1"
  }'

# 계약 목록 조회
curl -X GET "http://localhost:8000/api/v1/contracts/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 계약 상세 조회
curl -X GET "http://localhost:8000/api/v1/contracts/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Python requests 예시
```python
import requests

# API 기본 설정
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}

# 계약 생성
def create_contract(contract_data):
    response = requests.post(
        f"{BASE_URL}/contracts/",
        json=contract_data,
        headers=HEADERS
    )
    return response.json()

# 계약 목록 조회
def get_contracts(skip=0, limit=10, search=None):
    params = {"skip": skip, "limit": limit}
    if search:
        params["search"] = search
    
    response = requests.get(
        f"{BASE_URL}/contracts/",
        params=params,
        headers=HEADERS
    )
    return response.json()
```

## 📚 API 문서 접근

### Swagger UI
```
http://localhost:8000/docs
```

### ReDoc
```
http://localhost:8000/redoc
```

### OpenAPI JSON
```
http://localhost:8000/openapi.json
```

이 API 문서를 통해 **일관되고 안정적인** API 서비스를 제공할 수 있습니다. 