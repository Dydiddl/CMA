# API 엔드포인트 문서

## 인증 API

### 로그인
- **POST** `/api/auth/login`
- **설명**: 사용자 로그인
- **요청 본문**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **응답**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

### 회원가입
- **POST** `/api/auth/register`
- **설명**: 새로운 사용자 등록
- **요청 본문**:
  ```json
  {
    "email": "string",
    "password": "string",
    "full_name": "string",
    "role": "string",
    "department": "string",
    "phone": "string"
  }
  ```

## 계약 API

### 계약 목록 조회
- **GET** `/api/contracts/`
- **설명**: 모든 계약 목록 조회
- **쿼리 파라미터**:
  - `skip`: int (기본값: 0)
  - `limit`: int (기본값: 100)
  - `status`: string (선택)
- **응답**:
  ```json
  [
    {
      "id": "uuid",
      "contract_number": "string",
      "project_name": "string",
      "contract_amount": "float",
      "start_date": "date",
      "end_date": "date",
      "status": "string",
      "client": {
        "id": "uuid",
        "company_name": "string"
      }
    }
  ]
  ```

### 계약 상세 조회
- **GET** `/api/contracts/{contract_id}`
- **설명**: 특정 계약의 상세 정보 조회

### 계약 생성
- **POST** `/api/contracts/`
- **설명**: 새로운 계약 생성
- **요청 본문**:
  ```json
  {
    "contract_number": "string",
    "client_id": "uuid",
    "project_name": "string",
    "contract_amount": "float",
    "start_date": "date",
    "end_date": "date",
    "contract_type": "string"
  }
  ```

### 계약 수정
- **PUT** `/api/contracts/{contract_id}`
- **설명**: 기존 계약 정보 수정

### 계약 삭제
- **DELETE** `/api/contracts/{contract_id}`
- **설명**: 계약 삭제

## 인건비 API

### 인건비 목록 조회
- **GET** `/api/labor-costs/`
- **설명**: 인건비 목록 조회
- **쿼리 파라미터**:
  - `contract_id`: uuid (선택)
  - `worker_id`: uuid (선택)
  - `start_date`: date (선택)
  - `end_date`: date (선택)

### 인건비 등록
- **POST** `/api/labor-costs/`
- **설명**: 새로운 인건비 등록
- **요청 본문**:
  ```json
  {
    "contract_id": "uuid",
    "worker_id": "uuid",
    "work_date": "date",
    "hours_worked": "float",
    "hourly_rate": "float"
  }
  ```

### 인건비 수정
- **PUT** `/api/labor-costs/{labor_cost_id}`
- **설명**: 인건비 정보 수정

### 인건비 삭제
- **DELETE** `/api/labor-costs/{labor_cost_id}`
- **설명**: 인건비 삭제

## 비용 API

### 비용 목록 조회
- **GET** `/api/expenses/`
- **설명**: 비용 목록 조회
- **쿼리 파라미터**:
  - `contract_id`: uuid (선택)
  - `category`: string (선택)
  - `start_date`: date (선택)
  - `end_date`: date (선택)

### 비용 등록
- **POST** `/api/expenses/`
- **설명**: 새로운 비용 등록
- **요청 본문**:
  ```json
  {
    "contract_id": "uuid",
    "category": "string",
    "amount": "float",
    "expense_date": "date",
    "description": "string"
  }
  ```

### 비용 수정
- **PUT** `/api/expenses/{expense_id}`
- **설명**: 비용 정보 수정

### 비용 삭제
- **DELETE** `/api/expenses/{expense_id}`
- **설명**: 비용 삭제

## 수입 API

### 수입 목록 조회
- **GET** `/api/revenues/`
- **설명**: 수입 목록 조회
- **쿼리 파라미터**:
  - `contract_id`: uuid (선택)
  - `start_date`: date (선택)
  - `end_date`: date (선택)

### 수입 등록
- **POST** `/api/revenues/`
- **설명**: 새로운 수입 등록
- **요청 본문**:
  ```json
  {
    "contract_id": "uuid",
    "amount": "float",
    "payment_date": "date",
    "payment_type": "string",
    "description": "string"
  }
  ```

### 수입 수정
- **PUT** `/api/revenues/{revenue_id}`
- **설명**: 수입 정보 수정

### 수입 삭제
- **DELETE** `/api/revenues/{revenue_id}`
- **설명**: 수입 삭제

## 문서 API

### 문서 목록 조회
- **GET** `/api/documents/`
- **설명**: 문서 목록 조회
- **쿼리 파라미터**:
  - `contract_id`: uuid (선택)
  - `document_type`: string (선택)

### 문서 업로드
- **POST** `/api/documents/upload`
- **설명**: 새로운 문서 업로드
- **Content-Type**: `multipart/form-data`
- **요청 본문**:
  ```
  file: file
  contract_id: uuid
  document_type: string
  ```

### 문서 다운로드
- **GET** `/api/documents/{document_id}/download`
- **설명**: 문서 파일 다운로드

### 문서 삭제
- **DELETE** `/api/documents/{document_id}`
- **설명**: 문서 삭제

## 작업자 API

### 작업자 목록 조회
- **GET** `/api/workers/`
- **설명**: 작업자 목록 조회
- **쿼리 파라미터**:
  - `is_active`: boolean (선택)

### 작업자 등록
- **POST** `/api/workers/`
- **설명**: 새로운 작업자 등록
- **요청 본문**:
  ```json
  {
    "full_name": "string",
    "phone": "string",
    "id_number": "string",
    "bank_account": "string",
    "bank_name": "string",
    "hourly_rate": "float"
  }
  ```

### 작업자 수정
- **PUT** `/api/workers/{worker_id}`
- **설명**: 작업자 정보 수정

### 작업자 삭제
- **DELETE** `/api/workers/{worker_id}`
- **설명**: 작업자 삭제

## 거래처 API

### 거래처 목록 조회
- **GET** `/api/clients/`
- **설명**: 거래처 목록 조회

### 거래처 등록
- **POST** `/api/clients/`
- **설명**: 새로운 거래처 등록
- **요청 본문**:
  ```json
  {
    "company_name": "string",
    "business_number": "string",
    "representative_name": "string",
    "contact_person": "string",
    "phone": "string",
    "email": "string",
    "address": "string"
  }
  ```

### 거래처 수정
- **PUT** `/api/clients/{client_id}`
- **설명**: 거래처 정보 수정

### 거래처 삭제
- **DELETE** `/api/clients/{client_id}`
- **설명**: 거래처 삭제 