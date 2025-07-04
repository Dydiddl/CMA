# CMA 백엔드 API 설계 문서

## 🎯 API 설계 원칙

### 1. RESTful API 설계
- **HTTP 메서드 활용**: GET, POST, PUT, DELETE
- **리소스 중심 설계**: URL이 리소스를 명확히 표현
- **상태 없는 통신**: 각 요청이 독립적으로 처리
- **일관된 응답 형식**: 표준화된 JSON 응답 구조

### 2. 응답 형식 표준화
```json
{
  "status": "success|error",
  "data": {}, // 실제 데이터
  "message": "사용자 메시지",
  "code": "ERROR_CODE", // 오류 코드 (선택사항)
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. 오류 처리 표준화
```json
{
  "status": "error",
  "data": null,
  "message": "계약을 찾을 수 없습니다.",
  "code": "CONTRACT_NOT_FOUND",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 📋 API 엔드포인트 구조

### 1. 계약 관리 API

#### 계약 목록 조회
```http
GET /api/v1/contracts/
```

**Query Parameters:**
- `page`: 페이지 번호 (기본값: 1)
- `size`: 페이지 크기 (기본값: 10, 최대: 100)
- `search`: 검색어 (계약명, 계약번호, 발주처명)
- `status`: 상태 필터 (진행중, 완료, 중단, 취소)
- `start_date`: 시작일 필터
- `end_date`: 종료일 필터

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "contract-001",
      "name": "서울시 도로 공사",
      "contract_number": "CON-2024-001",
      "contract_amount": 1000000000,
      "contract_date": "2024-01-15T00:00:00Z",
      "start_date": "2024-02-01T00:00:00Z",
      "end_date": "2024-12-31T00:00:00Z",
      "client_name": "서울시청",
      "client_contact": "02-1234-5678",
      "status": "진행중",
      "description": "서울시 주요 도로 확장 공사",
      "vendor_id": "vendor-001",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10
}
```

#### 계약 상세 조회
```http
GET /api/v1/contracts/{contract_id}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": "contract-001",
    "name": "서울시 도로 공사",
    "contract_number": "CON-2024-001",
    "contract_amount": 1000000000,
    "contract_date": "2024-01-15T00:00:00Z",
    "start_date": "2024-02-01T00:00:00Z",
    "end_date": "2024-12-31T00:00:00Z",
    "client_name": "서울시청",
    "client_contact": "02-1234-5678",
    "status": "진행중",
    "description": "서울시 주요 도로 확장 공사",
    "vendor_id": "vendor-001",
    "vendor": {
      "id": "vendor-001",
      "name": "ABC 건설",
      "contact": "02-9876-5432"
    },
    "documents": [
      {
        "id": "doc-001",
        "name": "계약서.pdf",
        "file_path": "/uploads/contracts/contract-001.pdf",
        "upload_date": "2024-01-15T10:30:00Z"
      }
    ],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 계약 생성
```http
POST /api/v1/contracts/
```

**Request Body:**
```json
{
  "name": "서울시 도로 공사",
  "contract_number": "CON-2024-001",
  "contract_amount": 1000000000,
  "contract_date": "2024-01-15T00:00:00Z",
  "start_date": "2024-02-01T00:00:00Z",
  "end_date": "2024-12-31T00:00:00Z",
  "client_name": "서울시청",
  "client_contact": "02-1234-5678",
  "status": "진행중",
  "description": "서울시 주요 도로 확장 공사",
  "vendor_id": "vendor-001"
}
```

#### 계약 수정
```http
PUT /api/v1/contracts/{contract_id}
```

#### 계약 삭제
```http
DELETE /api/v1/contracts/{contract_id}
```

### 2. 노무 관리 API

#### 노무 목록 조회
```http
GET /api/v1/labor/
```

**Query Parameters:**
- `page`: 페이지 번호
- `size`: 페이지 크기
- `search`: 검색어 (근로자명, 직책)
- `contract_id`: 계약별 필터
- `work_date`: 작업일 필터

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "labor-001",
      "worker_name": "홍길동",
      "position": "현장소장",
      "contract_id": "contract-001",
      "daily_wage": 150000,
      "work_hours": 8,
      "work_date": "2024-01-15T00:00:00Z",
      "overtime_hours": 2,
      "total_wage": 165000,
      "notes": "도로 공사 현장 관리",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10
}
```

#### 노무 상세 조회
```http
GET /api/v1/labor/{labor_id}
```

#### 노무 등록
```http
POST /api/v1/labor/
```

**Request Body:**
```json
{
  "worker_name": "홍길동",
  "position": "현장소장",
  "contract_id": "contract-001",
  "daily_wage": 150000,
  "work_hours": 8,
  "work_date": "2024-01-15T00:00:00Z",
  "overtime_hours": 2,
  "notes": "도로 공사 현장 관리"
}
```

#### 노무 수정
```http
PUT /api/v1/labor/{labor_id}
```

#### 노무 삭제
```http
DELETE /api/v1/labor/{labor_id}
```

### 3. 재무 관리 API

#### 재무 목록 조회
```http
GET /api/v1/financial/
```

**Query Parameters:**
- `page`: 페이지 번호
- `size`: 페이지 크기
- `type`: 거래 유형 (수입, 지출)
- `contract_id`: 계약별 필터
- `start_date`: 시작일 필터
- `end_date`: 종료일 필터

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "financial-001",
      "transaction_date": "2024-01-15T00:00:00Z",
      "type": "수입",
      "amount": 50000000,
      "description": "1월 공사 대금",
      "contract_id": "contract-001",
      "category": "공사 대금",
      "payment_method": "계좌이체",
      "reference_number": "REF-2024-001",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10
}
```

#### 재무 통계 조회
```http
GET /api/v1/financial/statistics
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_revenue": 500000000,
    "total_expenses": 300000000,
    "net_profit": 200000000,
    "monthly_revenue": [
      {"month": "2024-01", "amount": 50000000},
      {"month": "2024-02", "amount": 60000000}
    ],
    "expense_by_category": [
      {"category": "인건비", "amount": 150000000},
      {"category": "자재비", "amount": 100000000},
      {"category": "기타", "amount": 50000000}
    ]
  }
}
```

### 4. 문서 관리 API

#### 문서 목록 조회
```http
GET /api/v1/documents/
```

#### 문서 업로드
```http
POST /api/v1/documents/upload
```

**Request (multipart/form-data):**
- `file`: 업로드할 파일
- `contract_id`: 관련 계약 ID
- `document_type`: 문서 유형
- `description`: 문서 설명

#### 문서 다운로드
```http
GET /api/v1/documents/{document_id}/download
```

## 🔐 인증 및 권한

### 1. JWT 토큰 인증
```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "username": "admin@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": "user-001",
      "username": "admin@example.com",
      "email": "admin@example.com",
      "role": "admin",
      "permissions": ["read", "write", "delete"]
    }
  }
}
```

### 2. 권한 기반 접근 제어
- **Admin**: 모든 기능 접근 가능
- **Manager**: 계약 관리, 노무 관리, 재무 조회
- **Worker**: 노무 기록, 문서 조회
- **Viewer**: 조회만 가능

## 📊 API 성능 지표

### 1. 응답 시간 목표
- **GET 요청**: 200ms 이내
- **POST 요청**: 500ms 이내
- **PUT/DELETE 요청**: 300ms 이내
- **대용량 데이터 조회**: 2초 이내

### 2. 동시 사용자 지원
- **개발 환경**: 10명 동시 접속
- **테스트 환경**: 50명 동시 접속
- **프로덕션 환경**: 100명 이상 동시 접속

### 3. 데이터 처리량
- **초당 요청 처리**: 1000+ requests/second
- **파일 업로드**: 10MB 이내 파일 5초 이내 처리
- **대용량 데이터 내보내기**: 10,000건 이내 30초 이내

## 🔧 API 버전 관리

### 1. URL 기반 버전 관리
```
/api/v1/contracts/  # 현재 버전
/api/v2/contracts/  # 향후 버전
```

### 2. 호환성 정책
- **메이저 버전**: 하위 호환성 보장
- **마이너 버전**: 새로운 기능 추가
- **패치 버전**: 버그 수정

### 3. Deprecation 정책
- **Deprecation Notice**: 6개월 전 공지
- **Migration Guide**: 마이그레이션 가이드 제공
- **Support Period**: 최소 1년간 지원

## 📝 API 문서화

### 1. 자동 문서화
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### 2. 코드 문서화
```python
@router.get("/contracts/", response_model=ContractListResponse)
async def get_contracts(
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 레코드 수"),
    search: Optional[str] = Query(None, description="검색어"),
    db: Session = Depends(get_db)
):
    """
    계약 목록을 조회합니다.
    
    - **skip**: 건너뛸 레코드 수 (페이징용)
    - **limit**: 가져올 레코드 수 (최대 100)
    - **search**: 계약명, 계약번호, 발주처명으로 검색
    """
    pass
```

## 🧪 API 테스트

### 1. 단위 테스트
```python
def test_get_contracts():
    """계약 목록 조회 테스트"""
    response = client.get("/api/v1/contracts/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

### 2. 통합 테스트
```python
def test_contract_crud():
    """계약 CRUD 통합 테스트"""
    # 생성
    contract_data = {"name": "테스트 계약", "contract_number": "TEST-001"}
    response = client.post("/api/v1/contracts/", json=contract_data)
    assert response.status_code == 201
    
    # 조회
    contract_id = response.json()["data"]["id"]
    response = client.get(f"/api/v1/contracts/{contract_id}")
    assert response.status_code == 200
    
    # 수정
    update_data = {"name": "수정된 계약"}
    response = client.put(f"/api/v1/contracts/{contract_id}", json=update_data)
    assert response.status_code == 200
    
    # 삭제
    response = client.delete(f"/api/v1/contracts/{contract_id}")
    assert response.status_code == 200
```

### 3. 성능 테스트
```python
def test_api_performance():
    """API 성능 테스트"""
    start_time = time.time()
    response = client.get("/api/v1/contracts/")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 0.5  # 500ms 이내
```

이 API 설계 문서는 CMA 백엔드 시스템의 모든 API 엔드포인트와 사용법을 상세히 설명합니다. 