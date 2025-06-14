# 계약 관리 API 문서

## 개요
계약 관리 API는 건설 프로젝트의 계약 정보를 관리하는 엔드포인트를 제공합니다. 계약의 생성, 조회, 수정, 삭제 및 버전 관리 기능을 포함합니다.

## 인증
모든 API 요청에는 JWT 토큰이 필요합니다. 헤더에 다음과 같이 포함해야 합니다:
```
Authorization: Bearer <token>
```

## 엔드포인트

### 계약 목록 조회
```http
GET /api/v1/contracts/
```

#### 쿼리 파라미터
- `skip` (int, 선택): 건너뛸 항목 수 (기본값: 0)
- `limit` (int, 선택): 반환할 항목 수 (기본값: 100)
- `status` (string, 선택): 계약 상태 필터 (DRAFT, PENDING, ACTIVE, COMPLETED, TERMINATED)
- `project_id` (int, 선택): 프로젝트 ID로 필터링

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "name": "건설 계약서",
      "description": "프로젝트 계약 내용",
      "status": "ACTIVE",
      "start_date": "2024-01-01",
      "end_date": "2024-12-31",
      "project_id": 1,
      "created_at": "2024-03-20T10:00:00",
      "updated_at": "2024-03-20T10:00:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### 계약 상세 조회
```http
GET /api/v1/contracts/{contract_id}
```

#### 경로 파라미터
- `contract_id` (int, 필수): 계약 ID

#### 응답
```json
{
  "id": 1,
  "name": "건설 계약서",
  "description": "프로젝트 계약 내용",
  "status": "ACTIVE",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "project_id": 1,
  "created_at": "2024-03-20T10:00:00",
  "updated_at": "2024-03-20T10:00:00",
  "versions": [
    {
      "id": 1,
      "version": "1.0.0",
      "content": "계약 내용",
      "changes": "초기 버전",
      "status": "PUBLISHED",
      "created_at": "2024-03-20T10:00:00"
    }
  ]
}
```

### 계약 생성
```http
POST /api/v1/contracts/
```

#### 요청 본문
```json
{
  "name": "건설 계약서",
  "description": "프로젝트 계약 내용",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "project_id": 1,
  "status": "DRAFT"
}
```

#### 응답
```json
{
  "id": 1,
  "name": "건설 계약서",
  "description": "프로젝트 계약 내용",
  "status": "DRAFT",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "project_id": 1,
  "created_at": "2024-03-20T10:00:00",
  "updated_at": "2024-03-20T10:00:00"
}
```

### 계약 수정
```http
PUT /api/v1/contracts/{contract_id}
```

#### 경로 파라미터
- `contract_id` (int, 필수): 계약 ID

#### 요청 본문
```json
{
  "name": "수정된 계약서",
  "description": "수정된 계약 내용",
  "status": "ACTIVE"
}
```

#### 응답
```json
{
  "id": 1,
  "name": "수정된 계약서",
  "description": "수정된 계약 내용",
  "status": "ACTIVE",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "project_id": 1,
  "created_at": "2024-03-20T10:00:00",
  "updated_at": "2024-03-20T11:00:00"
}
```

### 계약 삭제
```http
DELETE /api/v1/contracts/{contract_id}
```

#### 경로 파라미터
- `contract_id` (int, 필수): 계약 ID

#### 응답
```json
{
  "message": "계약이 성공적으로 삭제되었습니다."
}
```

### 계약 버전 생성
```http
POST /api/v1/contracts/{contract_id}/versions
```

#### 경로 파라미터
- `contract_id` (int, 필수): 계약 ID

#### 요청 본문
```json
{
  "version": "1.1.0",
  "content": "수정된 계약 내용",
  "changes": "계약 조건 변경",
  "status": "DRAFT"
}
```

#### 응답
```json
{
  "id": 2,
  "version": "1.1.0",
  "content": "수정된 계약 내용",
  "changes": "계약 조건 변경",
  "status": "DRAFT",
  "created_at": "2024-03-20T12:00:00"
}
```

### 계약 버전 목록 조회
```http
GET /api/v1/contracts/{contract_id}/versions
```

#### 경로 파라미터
- `contract_id` (int, 필수): 계약 ID

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "version": "1.0.0",
      "content": "계약 내용",
      "changes": "초기 버전",
      "status": "PUBLISHED",
      "created_at": "2024-03-20T10:00:00"
    },
    {
      "id": 2,
      "version": "1.1.0",
      "content": "수정된 계약 내용",
      "changes": "계약 조건 변경",
      "status": "DRAFT",
      "created_at": "2024-03-20T12:00:00"
    }
  ]
}
```

## 에러 응답
모든 API는 다음과 같은 에러 응답을 반환할 수 있습니다:

```json
{
  "detail": "에러 메시지"
}
```

### 일반적인 에러 코드
- 400: 잘못된 요청
- 401: 인증되지 않은 요청
- 403: 권한이 없는 요청
- 404: 리소스를 찾을 수 없음
- 422: 유효성 검사 실패
- 500: 서버 내부 오류

## 권한 요구사항
- 계약 조회: 모든 인증된 사용자
- 계약 생성: 프로젝트 관리자, 시스템 관리자
- 계약 수정: 프로젝트 관리자, 시스템 관리자
- 계약 삭제: 시스템 관리자
- 버전 관리: 프로젝트 관리자, 시스템 관리자 