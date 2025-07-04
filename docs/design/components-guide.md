# 컴포넌트 가이드 문서

## 1. 공통 컴포넌트

### 1.1 LoadingSpinner
로딩 상태를 표시하는 컴포넌트입니다.

#### Props
```typescript
interface LoadingSpinnerProps {
  message?: string;  // 로딩 메시지 (선택)
}
```

#### 사용 예시
```tsx
<LoadingSpinner message="데이터를 불러오는 중..." />
```

### 1.2 ErrorMessage
에러 메시지를 표시하는 컴포넌트입니다.

#### Props
```typescript
interface ErrorMessageProps {
  message: string;  // 에러 메시지
  onRetry?: () => void;  // 재시도 콜백 (선택)
}
```

#### 사용 예시
```tsx
<ErrorMessage 
  message="데이터를 불러오는데 실패했습니다" 
  onRetry={() => fetchData()} 
/>
```

### 1.3 Layout
전체 레이아웃을 구성하는 컴포넌트입니다.

#### Props
```typescript
interface LayoutProps {
  children: React.ReactNode;
}
```

#### 사용 예시
```tsx
<Layout>
  <YourComponent />
</Layout>
```

## 2. 프로젝트 컴포넌트

### 2.1 ProjectCard
프로젝트 정보를 카드 형태로 표시하는 컴포넌트입니다.

#### Props
```typescript
interface ProjectCardProps {
  project: Project;
  onClick: () => void;
}
```

#### 사용 예시
```tsx
<ProjectCard 
  project={projectData} 
  onClick={() => navigate(`/projects/${projectData.id}`)} 
/>
```

### 2.2 ProjectForm
프로젝트 생성/수정 폼 컴포넌트입니다.

#### Props
```typescript
interface ProjectFormProps {
  initialData?: Project;
  onSubmit: (data: ProjectFormData) => void;
  onCancel: () => void;
}
```

#### 사용 예시
```tsx
<ProjectForm 
  initialData={projectData}
  onSubmit={handleSubmit}
  onCancel={handleCancel}
/>
```

## 3. 태스크 컴포넌트

### 3.1 TaskCard
태스크 정보를 카드 형태로 표시하는 컴포넌트입니다.

#### Props
```typescript
interface TaskCardProps {
  task: Task;
  onClick: () => void;
}
```

#### 사용 예시
```tsx
<TaskCard 
  task={taskData} 
  onClick={() => navigate(`/tasks/${taskData.id}`)} 
/>
```

### 3.2 TaskForm
태스크 생성/수정 폼 컴포넌트입니다.

#### Props
```typescript
interface TaskFormProps {
  initialData?: Task;
  projectId?: number;
  onSubmit: (data: TaskFormData) => void;
  onCancel: () => void;
}
```

#### 사용 예시
```tsx
<TaskForm 
  initialData={taskData}
  projectId={1}
  onSubmit={handleSubmit}
  onCancel={handleCancel}
/>
```

## 4. 페이지 컴포넌트

### 4.1 Dashboard
대시보드 페이지 컴포넌트입니다.

#### 주요 기능
- 프로젝트 현황 요약
- 태스크 진행 상황
- 최근 활동 내역

### 4.2 ProjectList
프로젝트 목록 페이지 컴포넌트입니다.

#### 주요 기능
- 프로젝트 목록 표시
- 검색 및 필터링
- 프로젝트 생성/수정/삭제

### 4.3 ProjectDetail
프로젝트 상세 페이지 컴포넌트입니다.

#### 주요 기능
- 프로젝트 상세 정보 표시
- 관련 태스크 목록
- 프로젝트 수정/삭제

### 4.4 TaskList
태스크 목록 페이지 컴포넌트입니다.

#### 주요 기능
- 태스크 목록 표시
- 검색 및 필터링
- 태스크 생성/수정/삭제

### 4.5 TaskDetail
태스크 상세 페이지 컴포넌트입니다.

#### 주요 기능
- 태스크 상세 정보 표시
- 댓글 기능
- 태스크 수정/삭제

## 5. Context 컴포넌트

### 5.1 ProjectContext
프로젝트 관련 상태를 관리하는 Context입니다.

#### 주요 기능
- 프로젝트 목록 관리
- 프로젝트 CRUD 작업
- 로딩/에러 상태 관리

### 5.2 TaskContext
태스크 관련 상태를 관리하는 Context입니다.

#### 주요 기능
- 태스크 목록 관리
- 태스크 CRUD 작업
- 로딩/에러 상태 관리

## 6. 컴포넌트 설계 원칙

### 6.1 단일 책임 원칙
- 각 컴포넌트는 하나의 명확한 책임을 가져야 함
- 기능이 복잡해지면 더 작은 컴포넌트로 분리

### 6.2 재사용성
- 공통 컴포넌트는 최대한 재사용 가능하도록 설계
- Props를 통해 유연한 커스터마이징 지원

### 6.3 일관성
- 동일한 기능의 컴포넌트는 일관된 인터페이스 제공
- 디자인 시스템을 따르는 스타일링

### 6.4 접근성
- 키보드 네비게이션 지원
- 스크린 리더 호환성
- 색상 대비 고려

## 7. 컴포넌트 테스트

### 7.1 단위 테스트
- Props 검증
- 이벤트 핸들러 테스트
- 렌더링 결과 검증

### 7.2 통합 테스트
- 컴포넌트 간 상호작용 테스트
- API 연동 테스트

### 7.3 시각적 테스트
- 스토리북을 활용한 컴포넌트 문서화
- 다양한 상태별 렌더링 확인

---

**마지막 업데이트**: 2025년 1월 23일
**문서 버전**: v2.0 