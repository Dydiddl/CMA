# 인력 관리 API 문서

## 개요
인력 관리 API는 건설 현장의 작업자 관리, 안전 교육, 자격증 관리 등의 기능을 제공합니다. 작업자 등록, 안전 교육 기록, 자격증 관리 등의 기능을 포함합니다.

## 인증
모든 API 요청에는 JWT 토큰이 필요합니다. 헤더에 다음과 같이 포함해야 합니다:
```
Authorization: Bearer <token>
```

## 엔드포인트

### 작업자 등록
```http
POST /api/v1/labor/workers
```

#### 요청 본문
```json
{
  "name": "홍길동",
  "id_number": "123456-1234567",
  "phone": "010-1234-5678",
  "address": "서울시 강남구",
  "department_id": 1,
  "position": "기술자",
  "hire_date": "2024-03-20",
  "emergency_contact": {
    "name": "홍부모",
    "relationship": "부",
    "phone": "010-9876-5432"
  }
}
```

#### 응답
```json
{
  "id": 1,
  "name": "홍길동",
  "id_number": "123456-1234567",
  "phone": "010-1234-5678",
  "address": "서울시 강남구",
  "department_id": 1,
  "position": "기술자",
  "hire_date": "2024-03-20",
  "emergency_contact": {
    "name": "홍부모",
    "relationship": "부",
    "phone": "010-9876-5432"
  },
  "created_at": "2024-03-20T10:00:00"
}
```

### 작업자 목록 조회
```http
GET /api/v1/labor/workers
```

#### 쿼리 파라미터
- `skip` (int, 선택): 건너뛸 항목 수 (기본값: 0)
- `limit` (int, 선택): 반환할 항목 수 (기본값: 100)
- `department_id` (int, 선택): 부서 ID로 필터링

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "name": "홍길동",
      "id_number": "123456-1234567",
      "phone": "010-1234-5678",
      "department_id": 1,
      "position": "기술자",
      "hire_date": "2024-03-20"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### 작업자 상세 조회
```http
GET /api/v1/labor/workers/{worker_id}
```

#### 경로 파라미터
- `worker_id` (int, 필수): 작업자 ID

#### 응답
```json
{
  "id": 1,
  "name": "홍길동",
  "id_number": "123456-1234567",
  "phone": "010-1234-5678",
  "address": "서울시 강남구",
  "department_id": 1,
  "position": "기술자",
  "hire_date": "2024-03-20",
  "emergency_contact": {
    "name": "홍부모",
    "relationship": "부",
    "phone": "010-9876-5432"
  },
  "created_at": "2024-03-20T10:00:00",
  "safety_trainings": [
    {
      "id": 1,
      "type": "BASIC",
      "completed_at": "2024-03-20T10:00:00",
      "expires_at": "2025-03-20T10:00:00"
    }
  ],
  "certifications": [
    {
      "id": 1,
      "type": "건설기계조종사",
      "number": "12345",
      "issue_date": "2024-03-20",
      "expiry_date": "2029-03-20"
    }
  ]
}
```

### 작업자 정보 수정
```http
PUT /api/v1/labor/workers/{worker_id}
```

#### 경로 파라미터
- `worker_id` (int, 필수): 작업자 ID

#### 요청 본문
```json
{
  "phone": "010-9999-8888",
  "address": "서울시 서초구",
  "position": "수석기술자"
}
```

#### 응답
```json
{
  "id": 1,
  "name": "홍길동",
  "id_number": "123456-1234567",
  "phone": "010-9999-8888",
  "address": "서울시 서초구",
  "department_id": 1,
  "position": "수석기술자",
  "hire_date": "2024-03-20",
  "emergency_contact": {
    "name": "홍부모",
    "relationship": "부",
    "phone": "010-9876-5432"
  },
  "created_at": "2024-03-20T10:00:00"
}
```

### 작업자 퇴사 처리
```http
PUT /api/v1/labor/workers/{worker_id}/terminate
```

#### 경로 파라미터
- `worker_id` (int, 필수): 작업자 ID

#### 요청 본문
```json
{
  "termination_date": "2024-03-20",
  "reason": "개인사유"
}
```

#### 응답
```json
{
  "id": 1,
  "name": "홍길동",
  "status": "TERMINATED",
  "termination_date": "2024-03-20",
  "reason": "개인사유"
}
```

### 안전 교육 기록
```http
POST /api/v1/labor/safety-trainings
```

#### 요청 본문
```json
{
  "worker_id": 1,
  "type": "BASIC",
  "completed_at": "2024-03-20T10:00:00",
  "expires_at": "2025-03-20T10:00:00",
  "instructor": "김교육",
  "location": "본사 교육장"
}
```

#### 응답
```json
{
  "id": 1,
  "worker_id": 1,
  "type": "BASIC",
  "completed_at": "2024-03-20T10:00:00",
  "expires_at": "2025-03-20T10:00:00",
  "instructor": "김교육",
  "location": "본사 교육장",
  "created_at": "2024-03-20T10:00:00"
}
```

### 안전 교육 이력 조회
```http
GET /api/v1/labor/workers/{worker_id}/safety-trainings
```

#### 경로 파라미터
- `worker_id` (int, 필수): 작업자 ID

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "type": "BASIC",
      "completed_at": "2024-03-20T10:00:00",
      "expires_at": "2025-03-20T10:00:00",
      "instructor": "김교육",
      "location": "본사 교육장"
    }
  ],
  "total": 1
}
```

### 자격증 등록
```http
POST /api/v1/labor/certifications
```

#### 요청 본문
```json
{
  "worker_id": 1,
  "type": "건설기계조종사",
  "number": "12345",
  "issue_date": "2024-03-20",
  "expiry_date": "2029-03-20",
  "issuing_authority": "국토교통부"
}
```

#### 응답
```json
{
  "id": 1,
  "worker_id": 1,
  "type": "건설기계조종사",
  "number": "12345",
  "issue_date": "2024-03-20",
  "expiry_date": "2029-03-20",
  "issuing_authority": "국토교통부",
  "created_at": "2024-03-20T10:00:00"
}
```

### 자격증 목록 조회
```http
GET /api/v1/labor/workers/{worker_id}/certifications
```

#### 경로 파라미터
- `worker_id` (int, 필수): 작업자 ID

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "type": "건설기계조종사",
      "number": "12345",
      "issue_date": "2024-03-20",
      "expiry_date": "2029-03-20",
      "issuing_authority": "국토교통부"
    }
  ],
  "total": 1
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
- 작업자 조회: 모든 인증된 사용자
- 작업자 등록: 인사 관리자
- 작업자 정보 수정: 인사 관리자
- 작업자 퇴사 처리: 인사 관리자
- 안전 교육 기록: 안전 관리자
- 자격증 관리: 인사 관리자 