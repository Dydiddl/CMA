# API 문서화 API 문서

## 개요
API 문서화 API는 시스템의 API 엔드포인트에 대한 문서를 관리하는 기능을 제공합니다. API 문서의 생성, 버전 관리, 태그 관리, 댓글 기능 등을 포함합니다.

## 인증
모든 API 요청에는 JWT 토큰이 필요합니다. 헤더에 다음과 같이 포함해야 합니다:
```
Authorization: Bearer <token>
```

## 엔드포인트

### API 문서 목록 조회
```http
GET /api/v1/api-docs
```

#### 쿼리 파라미터
- `skip` (int, 선택): 건너뛸 항목 수 (기본값: 0)
- `limit` (int, 선택): 반환할 항목 수 (기본값: 100)
- `category` (string, 선택): 카테고리로 필터링
- `status` (string, 선택): 상태로 필터링 (DRAFT, REVIEW, PUBLISHED)

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "title": "사용자 관리 API",
      "description": "사용자 관리 관련 API 문서",
      "category": "USER",
      "status": "PUBLISHED",
      "version": "1.0.0",
      "created_at": "2024-03-20T10:00:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### API 문서 상세 조회
```http
GET /api/v1/api-docs/{doc_id}
```

#### 경로 파라미터
- `doc_id` (int, 필수): API 문서 ID

#### 응답
```json
{
  "id": 1,
  "title": "사용자 관리 API",
  "description": "사용자 관리 관련 API 문서",
  "content": "# 사용자 관리 API\n\n## 개요\n사용자 관리 API는...",
  "category": "USER",
  "status": "PUBLISHED",
  "version": "1.0.0",
  "created_at": "2024-03-20T10:00:00",
  "updated_at": "2024-03-20T10:00:00",
  "tags": ["user", "auth"],
  "comments": [
    {
      "id": 1,
      "content": "API 응답 형식에 대한 설명이 필요합니다.",
      "user_id": 1,
      "created_at": "2024-03-20T10:00:00"
    }
  ]
}
```

### API 문서 생성
```http
POST /api/v1/api-docs
```

#### 요청 본문
```json
{
  "title": "사용자 관리 API",
  "description": "사용자 관리 관련 API 문서",
  "content": "# 사용자 관리 API\n\n## 개요\n사용자 관리 API는...",
  "category": "USER",
  "tags": ["user", "auth"]
}
```

#### 응답
```json
{
  "id": 1,
  "title": "사용자 관리 API",
  "description": "사용자 관리 관련 API 문서",
  "content": "# 사용자 관리 API\n\n## 개요\n사용자 관리 API는...",
  "category": "USER",
  "status": "DRAFT",
  "version": "1.0.0",
  "created_at": "2024-03-20T10:00:00",
  "tags": ["user", "auth"]
}
```

### API 문서 수정
```http
PUT /api/v1/api-docs/{doc_id}
```

#### 경로 파라미터
- `doc_id` (int, 필수): API 문서 ID

#### 요청 본문
```json
{
  "title": "사용자 관리 API v2",
  "description": "사용자 관리 관련 API 문서 (업데이트)",
  "content": "# 사용자 관리 API v2\n\n## 개요\n사용자 관리 API는...",
  "category": "USER",
  "tags": ["user", "auth", "v2"]
}
```

#### 응답
```json
{
  "id": 1,
  "title": "사용자 관리 API v2",
  "description": "사용자 관리 관련 API 문서 (업데이트)",
  "content": "# 사용자 관리 API v2\n\n## 개요\n사용자 관리 API는...",
  "category": "USER",
  "status": "DRAFT",
  "version": "1.0.0",
  "updated_at": "2024-03-20T10:00:00",
  "tags": ["user", "auth", "v2"]
}
```

### API 문서 삭제
```http
DELETE /api/v1/api-docs/{doc_id}
```

#### 경로 파라미터
- `doc_id` (int, 필수): API 문서 ID

#### 응답
```json
{
  "message": "API 문서가 성공적으로 삭제되었습니다."
}
```

### API 문서 버전 생성
```http
POST /api/v1/api-docs/{doc_id}/versions
```

#### 경로 파라미터
- `doc_id` (int, 필수): API 문서 ID

#### 요청 본문
```json
{
  "version": "1.1.0",
  "content": "# 사용자 관리 API v1.1.0\n\n## 개요\n사용자 관리 API는...",
  "changes": "새로운 엔드포인트 추가 및 응답 형식 변경"
}
```

#### 응답
```json
{
  "id": 2,
  "doc_id": 1,
  "version": "1.1.0",
  "content": "# 사용자 관리 API v1.1.0\n\n## 개요\n사용자 관리 API는...",
  "changes": "새로운 엔드포인트 추가 및 응답 형식 변경",
  "created_at": "2024-03-20T10:00:00"
}
```

### API 문서 버전 목록 조회
```http
GET /api/v1/api-docs/{doc_id}/versions
```

#### 경로 파라미터
- `doc_id` (int, 필수): API 문서 ID

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "version": "1.0.0",
      "created_at": "2024-03-20T10:00:00",
      "status": "PUBLISHED"
    },
    {
      "id": 2,
      "version": "1.1.0",
      "created_at": "2024-03-20T10:00:00",
      "status": "DRAFT"
    }
  ],
  "total": 2
}
```

### API 문서 태그 추가
```http
POST /api/v1/api-docs/{doc_id}/tags
```

#### 경로 파라미터
- `doc_id` (int, 필수): API 문서 ID

#### 요청 본문
```json
{
  "tags": ["new-feature", "deprecated"]
}
```

#### 응답
```json
{
  "id": 1,
  "tags": ["user", "auth", "new-feature", "deprecated"]
}
```

### API 문서 댓글 추가
```http
POST /api/v1/api-docs/{doc_id}/comments
```

#### 경로 파라미터
- `doc_id` (int, 필수): API 문서 ID

#### 요청 본문
```json
{
  "content": "API 응답 형식에 대한 설명이 필요합니다.",
  "parent_id": null
}
```

#### 응답
```json
{
  "id": 1,
  "content": "API 응답 형식에 대한 설명이 필요합니다.",
  "user_id": 1,
  "created_at": "2024-03-20T10:00:00",
  "parent_id": null
}
```

### API 문서 댓글 목록 조회
```http
GET /api/v1/api-docs/{doc_id}/comments
```

#### 경로 파라미터
- `doc_id` (int, 필수): API 문서 ID

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "content": "API 응답 형식에 대한 설명이 필요합니다.",
      "user_id": 1,
      "created_at": "2024-03-20T10:00:00",
      "parent_id": null,
      "replies": [
        {
          "id": 2,
          "content": "응답 형식은 다음과 같습니다...",
          "user_id": 2,
          "created_at": "2024-03-20T10:00:00",
          "parent_id": 1
        }
      ]
    }
  ],
  "total": 1
}
```

### API 문서 통계 조회
```http
GET /api/v1/api-docs/statistics
```

#### 응답
```json
{
  "total_docs": 100,
  "docs_by_category": {
    "USER": 30,
    "PROJECT": 40,
    "CONTRACT": 20,
    "OTHER": 10
  },
  "docs_by_status": {
    "DRAFT": 20,
    "REVIEW": 30,
    "PUBLISHED": 50
  },
  "recent_updates": [
    {
      "id": 1,
      "title": "사용자 관리 API",
      "version": "1.1.0",
      "updated_at": "2024-03-20T10:00:00"
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
- API 문서 조회: 모든 인증된 사용자
- API 문서 생성: 개발자, 기술 문서 작성자
- API 문서 수정: 개발자, 기술 문서 작성자
- API 문서 삭제: 개발자, 기술 문서 작성자
- 버전 관리: 개발자, 기술 문서 작성자
- 태그 관리: 개발자, 기술 문서 작성자
- 댓글 작성: 모든 인증된 사용자
- 통계 조회: 개발자, 기술 문서 작성자 