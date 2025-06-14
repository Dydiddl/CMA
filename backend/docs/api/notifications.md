# 알림 관리 API 문서

## 개요
알림 관리 API는 시스템 내의 다양한 이벤트에 대한 알림을 관리하는 엔드포인트를 제공합니다. 알림의 생성, 조회, 수정, 삭제 및 템플릿 관리 기능을 포함합니다.

## 인증
모든 API 요청에는 JWT 토큰이 필요합니다. 헤더에 다음과 같이 포함해야 합니다:
```
Authorization: Bearer <token>
```

## 엔드포인트

### 알림 목록 조회
```http
GET /api/v1/notifications/
```

#### 쿼리 파라미터
- `skip` (int, 선택): 건너뛸 항목 수 (기본값: 0)
- `limit` (int, 선택): 반환할 항목 수 (기본값: 100)
- `is_read` (boolean, 선택): 읽음 상태 필터
- `type` (string, 선택): 알림 유형 필터 (SYSTEM, PROJECT, TASK, CONTRACT)

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "title": "새로운 작업 할당",
      "message": "프로젝트 A의 작업이 할당되었습니다.",
      "type": "TASK",
      "is_read": false,
      "user_id": 1,
      "created_at": "2024-03-20T10:00:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### 알림 상세 조회
```http
GET /api/v1/notifications/{notification_id}
```

#### 경로 파라미터
- `notification_id` (int, 필수): 알림 ID

#### 응답
```json
{
  "id": 1,
  "title": "새로운 작업 할당",
  "message": "프로젝트 A의 작업이 할당되었습니다.",
  "type": "TASK",
  "is_read": false,
  "user_id": 1,
  "created_at": "2024-03-20T10:00:00",
  "metadata": {
    "project_id": 1,
    "task_id": 1
  }
}
```

### 알림 생성
```http
POST /api/v1/notifications/
```

#### 요청 본문
```json
{
  "title": "새로운 작업 할당",
  "message": "프로젝트 A의 작업이 할당되었습니다.",
  "type": "TASK",
  "user_id": 1,
  "metadata": {
    "project_id": 1,
    "task_id": 1
  }
}
```

#### 응답
```json
{
  "id": 1,
  "title": "새로운 작업 할당",
  "message": "프로젝트 A의 작업이 할당되었습니다.",
  "type": "TASK",
  "is_read": false,
  "user_id": 1,
  "created_at": "2024-03-20T10:00:00",
  "metadata": {
    "project_id": 1,
    "task_id": 1
  }
}
```

### 알림 수정
```http
PUT /api/v1/notifications/{notification_id}
```

#### 경로 파라미터
- `notification_id` (int, 필수): 알림 ID

#### 요청 본문
```json
{
  "is_read": true
}
```

#### 응답
```json
{
  "id": 1,
  "title": "새로운 작업 할당",
  "message": "프로젝트 A의 작업이 할당되었습니다.",
  "type": "TASK",
  "is_read": true,
  "user_id": 1,
  "created_at": "2024-03-20T10:00:00",
  "metadata": {
    "project_id": 1,
    "task_id": 1
  }
}
```

### 알림 삭제
```http
DELETE /api/v1/notifications/{notification_id}
```

#### 경로 파라미터
- `notification_id` (int, 필수): 알림 ID

#### 응답
```json
{
  "message": "알림이 성공적으로 삭제되었습니다."
}
```

### 알림 일괄 읽음 처리
```http
PUT /api/v1/notifications/batch/read
```

#### 요청 본문
```json
{
  "notification_ids": [1, 2, 3]
}
```

#### 응답
```json
{
  "message": "선택한 알림이 모두 읽음 처리되었습니다.",
  "updated_count": 3
}
```

### 알림 일괄 삭제
```http
DELETE /api/v1/notifications/batch
```

#### 요청 본문
```json
{
  "notification_ids": [1, 2, 3]
}
```

#### 응답
```json
{
  "message": "선택한 알림이 모두 삭제되었습니다.",
  "deleted_count": 3
}
```

### 알림 템플릿 생성
```http
POST /api/v1/notifications/templates
```

#### 요청 본문
```json
{
  "name": "작업 할당 알림",
  "content": "{user_name}님이 {project_name} 프로젝트의 {task_name} 작업이 할당되었습니다.",
  "category": "TASK",
  "variables": ["user_name", "project_name", "task_name"],
  "is_active": true
}
```

#### 응답
```json
{
  "id": 1,
  "name": "작업 할당 알림",
  "content": "{user_name}님이 {project_name} 프로젝트의 {task_name} 작업이 할당되었습니다.",
  "category": "TASK",
  "variables": ["user_name", "project_name", "task_name"],
  "is_active": true,
  "created_at": "2024-03-20T10:00:00"
}
```

### 알림 템플릿 목록 조회
```http
GET /api/v1/notifications/templates
```

#### 응답
```json
{
  "items": [
    {
      "id": 1,
      "name": "작업 할당 알림",
      "content": "{user_name}님이 {project_name} 프로젝트의 {task_name} 작업이 할당되었습니다.",
      "category": "TASK",
      "variables": ["user_name", "project_name", "task_name"],
      "is_active": true,
      "created_at": "2024-03-20T10:00:00"
    }
  ]
}
```

### 알림 통계 조회
```http
GET /api/v1/notifications/statistics
```

#### 응답
```json
{
  "total_notifications": 100,
  "unread_count": 30,
  "notifications_by_type": {
    "SYSTEM": 20,
    "PROJECT": 40,
    "TASK": 30,
    "CONTRACT": 10
  },
  "recent_notifications": [
    {
      "id": 1,
      "title": "새로운 작업 할당",
      "type": "TASK",
      "created_at": "2024-03-20T10:00:00"
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
- 알림 조회: 모든 인증된 사용자
- 알림 생성: 시스템 관리자
- 알림 수정: 알림 소유자, 시스템 관리자
- 알림 삭제: 알림 소유자, 시스템 관리자
- 템플릿 관리: 시스템 관리자
- 통계 조회: 시스템 관리자 