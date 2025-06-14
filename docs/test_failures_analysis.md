# 테스트 실패 분석 문서

## 1. 모델 관계 설정 문제

### 1.1 User-UserProfile 관계 문제
- **파일**: `backend/app/models/user.py`
- **오류**: `sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers.`
- **원인**: User와 UserProfile 모델 간의 양방향 관계 설정이 잘못됨
- **해결 방법**: 
  ```python
  # User 모델
  profile = relationship("UserProfile", back_populates="user", uselist=False)
  
  # UserProfile 모델
  user = relationship("User", back_populates="profile")
  ```

### 1.2 Department-User 관계 문제
- **파일**: `backend/app/models/department.py`
- **오류**: `sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize`
- **원인**: Department와 User 모델 간의 양방향 관계 설정이 잘못됨
- **해결 방법**:
  ```python
  # Department 모델
  users = relationship("User", back_populates="department")
  
  # User 모델
  department = relationship("Department", back_populates="users")
  ```

## 2. Import 경로 문제

### 2.1 모델 Import 문제
- **파일**: `backend/app/models/*.py`
- **오류**: `ModuleNotFoundError: No module named 'app'`
- **원인**: 상대 경로 import가 잘못됨
- **해결 방법**: 모든 import 문을 `backend.app`으로 수정
  ```python
  from backend.app.models.user import User
  from backend.app.models.department import Department
  ```

### 2.2 테스트 Import 문제
- **파일**: `backend/tests/*.py`
- **오류**: `ModuleNotFoundError: No module named 'app'`
- **원인**: 테스트에서도 동일한 import 경로 문제 발생
- **해결 방법**: 테스트 파일의 import 문도 `backend.app`으로 수정

## 3. 데이터베이스 제약조건 문제

### 3.1 Project 모델 NOT NULL 제약조건
- **파일**: `backend/app/models/project.py`
- **오류**: `sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: projects.owner_id`
- **원인**: Project 생성 시 필수 필드인 owner_id가 누락됨
- **해결 방법**: Project 생성 시 owner_id 필수 포함
  ```python
  project = Project(
      name="Test Project",
      description="Test Description",
      owner_id=1  # 필수 필드
  )
  ```

### 3.2 Task 모델 NOT NULL 제약조건
- **파일**: `backend/app/models/task.py`
- **오류**: `sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: tasks.project_id`
- **원인**: Task 생성 시 필수 필드인 project_id가 누락됨
- **해결 방법**: Task 생성 시 project_id 필수 포함
  ```python
  task = Task(
      title="Test Task",
      description="Test Description",
      project_id=1  # 필수 필드
  )
  ```

## 4. 테스트 데이터 설정 문제

### 4.1 테스트 데이터 초기화
- **파일**: `backend/tests/conftest.py`
- **오류**: 테스트 데이터가 올바르게 초기화되지 않음
- **해결 방법**: 
  1. 테스트 데이터베이스 초기화
  2. 필수 모델(User, Department 등) 먼저 생성
  3. 의존성이 있는 모델(Project, Task 등) 생성 시 필수 필드 포함

### 4.2 테스트 격리
- **파일**: `backend/tests/*.py`
- **오류**: 테스트 간 데이터 격리가 되지 않음
- **해결 방법**:
  1. 각 테스트 전에 데이터베이스 초기화
  2. 트랜잭션 사용으로 테스트 격리
  3. 테스트 후 롤백 처리

## 5. 권한 검사 문제

### 5.1 권한 검사 로직
- **파일**: `backend/app/core/security.py`
- **오류**: 권한 검사가 올바르게 동작하지 않음
- **해결 방법**:
  1. 권한 검사 로직 수정
  2. 테스트에서 권한 검사 시나리오 추가
  3. 권한 검사 실패 케이스 테스트 추가

## 6. API 엔드포인트 테스트 문제

### 6.1 API 응답 검증
- **파일**: `backend/tests/api/*.py`
- **오류**: API 응답 검증이 불완전함
- **해결 방법**:
  1. 응답 상태 코드 검증
  2. 응답 데이터 구조 검증
  3. 에러 케이스 검증

### 6.2 API 인증 테스트
- **파일**: `backend/tests/api/*.py`
- **오류**: 인증 관련 테스트가 불완전함
- **해결 방법**:
  1. 인증 토큰 검증
  2. 인증 실패 케이스 테스트
  3. 권한별 접근 제어 테스트 