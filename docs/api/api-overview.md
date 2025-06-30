# API 문서

## 1. 프로젝트 API

### 1.1 프로젝트 목록 조회
```http
GET /api/projects
```
프로젝트 목록을 조회합니다.

#### 응답
```json
{
  "projects": [
    {
      "id": 1,
      "name": "프로젝트명",
      "description": "프로젝트 설명",
      "status": "IN_PROGRESS",
      "startDate": "2024-03-20",
      "endDate": "2024-06-20",
      "progress": 45,
      "managerId": 1,
      "createdAt": "2024-03-20T00:00:00Z",
      "updatedAt": "2024-03-20T00:00:00Z"
    }
  ]
}
```

### 1.2 프로젝트 상세 조회
```http
GET /api/projects/:id
```
특정 프로젝트의 상세 정보를 조회합니다.

#### 응답
```json
{
  "id": 1,
  "name": "프로젝트명",
  "description": "프로젝트 설명",
  "status": "IN_PROGRESS",
  "startDate": "2024-03-20",
  "endDate": "2024-06-20",
  "progress": 45,
  "managerId": 1,
  "tasks": [
    {
      "id": 1,
      "name": "태스크명",
      "status": "IN_PROGRESS",
      "progress": 60
    }
  ],
  "createdAt": "2024-03-20T00:00:00Z",
  "updatedAt": "2024-03-20T00:00:00Z"
}
```

### 1.3 프로젝트 생성
```http
POST /api/projects
```
새로운 프로젝트를 생성합니다.

#### 요청
```json
{
  "name": "프로젝트명",
  "description": "프로젝트 설명",
  "status": "IN_PROGRESS",
  "startDate": "2024-03-20",
  "endDate": "2024-06-20",
  "managerId": 1
}
```

### 1.4 프로젝트 수정
```http
PUT /api/projects/:id
```
기존 프로젝트를 수정합니다.

#### 요청
```json
{
  "name": "수정된 프로젝트명",
  "description": "수정된 프로젝트 설명",
  "status": "IN_PROGRESS",
  "startDate": "2024-03-20",
  "endDate": "2024-06-20",
  "managerId": 1
}
```

### 1.5 프로젝트 삭제
```http
DELETE /api/projects/:id
```
프로젝트를 삭제합니다.

## 2. 태스크 API

### 2.1 태스크 목록 조회
```http
GET /api/tasks?projectId=1
```
작업 목록을 조회합니다.

#### 응답
```json
{
  "tasks": [
    {
      "id": 1,
      "name": "태스크명",
      "description": "태스크 설명",
      "status": "IN_PROGRESS",
      "startDate": "2024-03-20",
      "endDate": "2024-03-25",
      "progress": 60,
      "projectId": 1,
      "assigneeId": 1,
      "createdAt": "2024-03-20T00:00:00Z",
      "updatedAt": "2024-03-20T00:00:00Z"
    }
  ]
}
```

### 2.2 태스크 상세 조회
```http
GET /api/tasks/:id
```
특정 작업의 상세 정보를 조회합니다.

#### 응답
```json
{
  "id": 1,
  "name": "태스크명",
  "description": "태스크 설명",
  "status": "IN_PROGRESS",
  "startDate": "2024-03-20",
  "endDate": "2024-03-25",
  "progress": 60,
  "projectId": 1,
  "assigneeId": 1,
  "comments": [
    {
      "id": 1,
      "content": "댓글 내용",
      "userId": 1,
      "createdAt": "2024-03-20T00:00:00Z"
    }
  ],
  "createdAt": "2024-03-20T00:00:00Z",
  "updatedAt": "2024-03-20T00:00:00Z"
}
```

### 2.3 태스크 생성
```http
POST /api/tasks
```
새로운 작업을 생성합니다.

#### 요청
```json
{
  "name": "태스크명",
  "description": "태스크 설명",
  "status": "TODO",
  "startDate": "2024-03-20",
  "endDate": "2024-03-25",
  "projectId": 1,
  "assigneeId": 1
}
```

### 2.4 태스크 수정
```http
PUT /api/tasks/:id
```
기존 작업을 수정합니다.

#### 요청
```json
{
  "name": "수정된 태스크명",
  "description": "수정된 태스크 설명",
  "status": "IN_PROGRESS",
  "startDate": "2024-03-20",
  "endDate": "2024-03-25",
  "projectId": 1,
  "assigneeId": 1
}
```

### 2.5 태스크 삭제
```http
DELETE /api/tasks/:id
```
작업을 삭제합니다.

## 3. 사용자 API

### 3.1 로그인
```http
POST /api/auth/login
```
사용자 로그인을 수행합니다.

#### 요청
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### 응답
```json
{
  "token": "jwt_token",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "사용자명",
    "role": "USER"
  }
}
```

### 3.2 회원가입
```http
POST /api/auth/register
```
새로운 사용자를 등록합니다.

#### 요청
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "사용자명"
}
```

### 3.3 현재 사용자 정보 조회
```http
GET /api/auth/me
```
현재 로그인한 사용자의 정보를 조회합니다.

#### 응답
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "사용자명",
  "role": "USER"
}
```

### 3.4 사용자 정보 수정
```http
PUT /api/users/:id
```
사용자 정보를 수정합니다.

#### 요청
```json
{
  "name": "수정된 사용자명",
  "email": "updated@example.com"
}
```

### 3.5 로그아웃
```http
POST /api/auth/logout
```
사용자 로그아웃을 수행합니다.

## 4. 에러 응답

모든 API는 에러 발생 시 다음과 같은 형식으로 응답합니다:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "에러 메시지"
  }
}
```

### 4.1 주요 에러 코드
- `INVALID_REQUEST`: 잘못된 요청
- `UNAUTHORIZED`: 인증 실패
- `FORBIDDEN`: 권한 없음
- `NOT_FOUND`: 리소스를 찾을 수 없음
- `INTERNAL_ERROR`: 서버 내부 오류 