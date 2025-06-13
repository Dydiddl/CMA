# 프론트엔드 아키텍처 문서

## 1. 기술 스택

### 1.1 핵심 기술
- React 18
- TypeScript
- Vite (빌드 도구)
- React Router (라우팅)
- Redux Toolkit (상태 관리)
- Axios (HTTP 클라이언트)
- Material-UI (UI 컴포넌트)

### 1.2 개발 도구
- ESLint (코드 품질)
- Prettier (코드 포맷팅)
- Jest (테스트)
- React Testing Library (컴포넌트 테스트)

## 2. 프로젝트 구조

```
frontend/
├── src/
│   ├── api/              # API 통신 관련
│   ├── assets/           # 정적 파일
│   ├── components/       # 재사용 가능한 컴포넌트
│   ├── features/         # 기능별 모듈
│   ├── hooks/            # 커스텀 훅
│   ├── layouts/          # 레이아웃 컴포넌트
│   ├── pages/            # 페이지 컴포넌트
│   ├── store/            # Redux 스토어
│   ├── types/            # TypeScript 타입 정의
│   └── utils/            # 유틸리티 함수
├── public/               # 정적 파일
└── tests/                # 테스트 파일
```

## 3. 주요 기능 구현

### 3.1 인증/인가
- 로그인/로그아웃
- JWT 토큰 관리
- 권한 기반 접근 제어

### 3.2 계약 관리
- 계약 목록 조회
- 계약 상세 정보
- 계약 생성/수정/삭제
- 계약서 문서 관리

### 3.3 인건비 관리
- 작업자 목록
- 작업 시간 기록
- 인건비 계산
- 지급 관리

### 3.4 비용 관리
- 비용 목록
- 비용 등록/수정
- 카테고리별 관리
- 지출 분석

### 3.5 수입 관리
- 수입 목록
- 수입 등록/수정
- 지불 방식 관리
- 수입 분석

### 3.6 문서 관리
- 문서 목록
- 문서 업로드/다운로드
- 문서 검색
- 문서 미리보기

## 4. 컴포넌트 구조

### 4.1 공통 컴포넌트
- Button
- Input
- Select
- Table
- Modal
- Form
- Card
- Alert
- Loading
- Pagination

### 4.2 레이아웃 컴포넌트
- MainLayout
- Sidebar
- Header
- Footer
- Content

### 4.3 페이지 컴포넌트
- Login
- Dashboard
- ContractList
- ContractDetail
- WorkerList
- WorkerDetail
- ExpenseList
- RevenueList
- DocumentList

## 5. 상태 관리

### 5.1 Redux 스토어 구조
```typescript
{
  auth: {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
  };
  contracts: {
    items: Contract[];
    selected: Contract | null;
    loading: boolean;
    error: string | null;
  };
  workers: {
    items: Worker[];
    selected: Worker | null;
    loading: boolean;
    error: string | null;
  };
  expenses: {
    items: Expense[];
    selected: Expense | null;
    loading: boolean;
    error: string | null;
  };
  revenues: {
    items: Revenue[];
    selected: Revenue | null;
    loading: boolean;
    error: string | null;
  };
}
```

### 5.2 API 통신
- Axios 인스턴스 설정
- 인터셉터 설정
- 에러 처리
- 토큰 관리

## 6. 라우팅

### 6.1 라우트 구조
```typescript
const routes = [
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'contracts', element: <ContractList /> },
      { path: 'contracts/:id', element: <ContractDetail /> },
      { path: 'workers', element: <WorkerList /> },
      { path: 'workers/:id', element: <WorkerDetail /> },
      { path: 'expenses', element: <ExpenseList /> },
      { path: 'revenues', element: <RevenueList /> },
      { path: 'documents', element: <DocumentList /> },
    ],
  },
  {
    path: '/login',
    element: <Login />,
  },
];
```

### 6.2 보호된 라우트
- 인증 필요 라우트
- 권한 기반 접근 제어
- 리다이렉션 처리

## 7. 스타일링

### 7.1 테마 설정
- 색상 팔레트
- 타이포그래피
- 간격
- 그림자
- 애니메이션

### 7.2 반응형 디자인
- 모바일 퍼스트 접근
- 브레이크포인트
- 그리드 시스템

## 8. 성능 최적화

### 8.1 코드 스플리팅
- 라우트 기반 코드 스플리팅
- 컴포넌트 지연 로딩
- 동적 임포트

### 8.2 캐싱
- API 응답 캐싱
- 컴포넌트 메모이제이션
- 이미지 최적화

## 9. 테스트

### 9.1 단위 테스트
- 컴포넌트 테스트
- 유틸리티 함수 테스트
- Redux 리듀서 테스트

### 9.2 통합 테스트
- API 통신 테스트
- 사용자 흐름 테스트
- 상태 관리 테스트

## 10. 배포

### 10.1 빌드 설정
- 환경 변수
- 최적화 설정
- 소스맵 생성

### 10.2 CI/CD
- 자동화된 테스트
- 빌드 자동화
- 배포 자동화 