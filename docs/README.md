# 📚 CMA 프로젝트 문서

## 🎯 프로젝트 개요

**CMA (Construction Management System)**는 건설 공사 내역서 자동화 시스템으로, 계약 관리, 재무 관리, 노무 관리, 문서 처리 등을 통합적으로 제공하는 **하이브리드 아키텍처** 기반의 데스크톱 애플리케이션입니다.

### 🆕 주요 특징 (2025년 1월 기준)
- **하이브리드 아키텍처**: Python 기반 + 선택적 네이티브 최적화
- 설치형 실행 파일로 배포 (.exe) - Tauri 2.x 기반
- UI는 React + TypeScript + Vite + Mantine/MUI
- 백엔드는 Python + FastAPI + SQLAlchemy
- 데이터베이스는 PostgreSQL (로컬) + Supabase (클라우드 연동)
- 문서 작업(Excel 등)은 백엔드에서 Python으로 처리
- **샤딩 기능으로 대용량 데이터 처리 지원**
- **ASCR 모듈 통합으로 PDF 처리 및 검증 기능 제공**
- **성능 최적화**: 비동기 처리, 멀티프로세싱, 캐싱 전략

### 📊 프로젝트 진행률 (2025년 1월 기준)
- **전체 진행률**: 약 65~70%
- **백엔드 API**: 80% 완료
- **프론트엔드**: 60% 완료
- **데이터베이스**: 90% 완료
- **테스트**: 50% 완료
- **성능 최적화**: 40% 완료

### 🎯 최우선 목표 (2025년 1-2월)
**핵심 기능 완성 및 안정화** - 기본적인 건설 관리 시스템으로 사용 가능한 상태 달성

#### 즉시 실행 (1-2주)
- [ ] **계약 관리 모듈 완성** - 계약 CRUD, 상태 추적, 자동 생성
- [ ] **재무 관리 모듈 완성** - 예산 관리, 비용 분석, 보고서 생성
- [ ] **노무 관리 모듈 완성** - 인력 관리, 시간 추적, 임금 계산
- [ ] **ASCR 모듈 통합** - PDF 처리, 목차 생성, 문서 자동화

#### 단기 목표 (2-4주)
- [ ] **기본 UI/UX 완성** - 대시보드, 네비게이션, 반응형 디자인
- [ ] **성능 최적화** - API 응답 시간 500ms 이내
- [ ] **테스트 커버리지** - 70% 이상 달성
- [ ] **보안 강화** - 인증/인가 시스템 완성

## 📁 문서 구조

```
docs/
├── README.md                           # 메인 문서 (현재 파일)
│
├── 📋 프로젝트 개요
│   ├── project-overview.md             # 프로젝트 개요 및 목표
│   ├── roadmap.md                      # 개발 로드맵
│   └── changelog.md                    # 변경 이력
│
├── 🏗️ 아키텍처
│   ├── architecture-overview.md        # 전체 아키텍처 개요
│   ├── frontend-architecture.md        # 프론트엔드 아키텍처
│   ├── backend-architecture.md         # 백엔드 아키텍처
│   ├── database-schema.md              # 데이터베이스 스키마
│   └── comprehensive-schema-relationship.md  # 상세 스키마 관계
│
├── 🔗 API 문서
│   ├── ENDPOINTS_DETAIL.md             # 상세 API 엔드포인트 문서 (통합됨)
│   └── api/
│       └── v1/                         # API 버전별 문서 (개별 문서 통합됨)
│
├── 💻 개발 가이드
│   ├── development-guide.md            # 개발 환경 설정 및 가이드
│   ├── setup-instructions.md           # 설치 및 설정 가이드
│   ├── testing-guide.md                # 테스트 가이드
│   └── deployment-guide.md             # 배포 가이드
│
├── 🎨 디자인 및 UI
│   ├── design-system.md                # 디자인 시스템
│   ├── components-guide.md             # 컴포넌트 가이드 (이동됨)
│   └── ui-guidelines.md                # UI 가이드라인
│
├── 🔧 기술 문서
│   ├── technical-specifications.md     # 기술 명세서
│   ├── performance-optimization.md     # 성능 최적화 가이드
│   └── security-guidelines.md          # 보안 가이드라인
│
├── 📖 사용자 가이드
│   ├── user-manual.md                  # 사용자 매뉴얼
│   ├── feature-guide.md                # 기능 가이드
│   └── troubleshooting.md              # 문제 해결 가이드
│
└── 📝 기타 문서
    ├── documentation-organization.md   # 문서 정리 작업 요약
    └── contributing.md                 # 기여 가이드
```

## 🚀 빠른 시작

### 1. 개발 환경 설정
```bash
# 1. 프로젝트 클론
git clone [repository-url]
cd CMA

# 2. 백엔드 설정
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는 venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. 프론트엔드 설정
cd ../frontend
npm install

# 4. 개발 서버 실행
# 백엔드 (터미널 1)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 프론트엔드 (터미널 2)
cd frontend
npm run dev
```

### 2. 주요 기능
- **계약 관리**: 계약 생성, 수정, 삭제, 상태 추적
- **재무 관리**: 수입/지출 관리, 예산 분석, 보고서 생성
- **노무 관리**: 작업자 관리, 시간 추적, 임금 계산
- **문서 관리**: PDF 처리, Excel 내역서 자동 생성
- **ASCR 모듈**: PDF 목차 추출, 문서 분할, 자동화

## 🛠 기술 스택

### Frontend
- **React**: 18.2.0
- **TypeScript**: 5.8.3
- **Vite**: 4.5.14 (빌드 도구)
- **Mantine**: 8.1.0 + **Material-UI**: 5.17.1 (UI 라이브러리)
- **Tauri**: 2.5.0 (데스크톱 앱 프레임워크)
- **Zustand**: 4.5.7 (상태 관리)
- **React Router DOM**: 6.30.1 (라우팅)

### Backend
- **Python**: 3.12+
- **FastAPI**: 0.115.12 (비동기 웹 프레임워크)
- **SQLAlchemy**: 2.0.41 (ORM)
- **Alembic**: 1.16.1 (데이터베이스 마이그레이션)
- **Pydantic**: 2.11.7 (데이터 검증)
- **Uvicorn**: 0.34.3 (ASGI 서버)
- **Pandas**: 2.3.0 (데이터 처리)
- **OpenPyXL**: 3.1.5 (Excel 처리)
- **XlsxWriter**: 3.2.3 (Excel 생성)
- **pypdf/PyMuPDF**: PDF 처리 (ASCR 모듈)
- **Redis**: 캐싱 및 세션 관리
- **Celery**: 비동기 작업 처리

### Desktop (PySide6)
- **PySide6**: 6.6.1 (Qt 기반 GUI 프레임워크)
- **SQLAlchemy**: 2.0.41 (로컬 데이터베이스 ORM)
- **Pandas**: 2.3.0 (데이터 처리)
- **OpenPyXL**: 3.1.5 (Excel 처리)
- **pypdf**: 3.17.4 (PDF 처리)
- **psycopg2-binary**: 2.9.10 (PostgreSQL 연결)
- **redis**: 5.2.1 (캐싱)
- **psutil**: 6.1.0 (시스템 모니터링)

### Database
- **PostgreSQL**: 14+ (로컬 개발)
- **Supabase**: (클라우드 프로덕션)
- **Redis**: 캐싱 및 세션 저장소

### Performance Optimization
- **asyncio**: 비동기 처리
- **multiprocessing**: CPU 집약적 작업
- **threading**: I/O 집약적 작업
- **Redis**: 분산 캐싱
- **Connection Pooling**: 데이터베이스 연결 최적화

## 📊 성능 목표

### 현재 성능 지표
- **API 응답 시간**: 평균 800ms (목표: 500ms)
- **데이터베이스 쿼리**: 평균 150ms (목표: 100ms)
- **파일 처리**: 평균 3초 (목표: 2초)
- **테스트 커버리지**: 65% (목표: 80%)

### 최적화 전략
1. **Python 최적화** (PHASE 1): 비동기 처리, 캐싱, 쿼리 최적화
2. **하이브리드 최적화** (PHASE 2): 핵심 모듈 네이티브 전환
3. **완전 최적화** (PHASE 3): 전체 시스템 성능 검증

## 🔒 보안 및 규정 준수

### 보안 기능
- JWT 기반 인증
- 역할 기반 접근 제어 (RBAC)
- API 엔드포인트 보안
- 데이터 암호화
- 크로스 플랫폼 보안

### 규정 준수
- 개인정보보호법 준수
- 건설업 관련 법규 준수
- 데이터 백업 및 복구 정책

## 🤝 기여하기

### 개발 참여 방법
1. 이슈 등록 또는 기존 이슈 확인
2. 브랜치 생성 (`feature/기능명` 또는 `fix/버그명`)
3. 코드 작성 및 테스트
4. Pull Request 생성
5. 코드 리뷰 및 머지

### 개발 규칙
- **코드 스타일**: PEP8 (Python), ESLint (TypeScript)
- **커밋 메시지**: Conventional Commits 형식
- **테스트**: 새로운 기능에 대한 테스트 코드 필수
- **문서화**: 코드 변경 시 관련 문서 업데이트

## 📞 지원 및 문의

### 문제 해결
- **기술적 문제**: [GitHub Issues](링크)
- **문서 관련**: [Documentation Issues](링크)
- **성능 이슈**: [Performance Issues](링크)

### 연락처
- **개발팀**: dev@cma-project.com
- **기술 지원**: support@cma-project.com
- **문서 관련**: docs@cma-project.com

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](링크) 파일을 참조하세요.

## 🔄 문서 업데이트

### 최근 업데이트 (2025년 1월 23일)
- ✅ **문서 구조 개선**: 중복 문서 통합 및 체계적 정리
- ✅ **API 문서 통합**: 개별 API 문서를 ENDPOINTS_DETAIL.md로 통합
- ✅ **아키텍처 문서 정리**: 폴더별 체계적 분류
- ✅ **개발 가이드 업데이트**: 하이브리드 아키텍처 전략 반영
- ✅ **성능 최적화 가이드**: 단계별 최적화 전략 추가
- ✅ **크로스 플랫폼 규칙**: Ubuntu → Windows 환경 전환 가이드

### 다음 업데이트 예정
- [ ] **사용자 매뉴얼 완성**: 실제 사용 시나리오 기반 가이드
- [ ] **성능 벤치마크**: 실제 성능 측정 결과 반영
- [ ] **보안 가이드 강화**: 구체적인 보안 체크리스트
- [ ] **배포 가이드 상세화**: 단계별 배포 프로세스

---

**마지막 업데이트**: 2025년 1월 23일  
**문서 버전**: v3.0  
**프로젝트 버전**: v1.2.0

## 🤝 기여하기

### 개발 참여 방법
1. 이슈 등록 또는 기존 이슈 확인
2. 브랜치 생성 (`feature/기능명` 또는 `fix/버그명`)
3. 코드 작성 및 테스트
4. Pull Request 생성
5. 코드 리뷰 및 머지

### 개발 규칙
- **코드 스타일**: PEP8 (Python), ESLint (TypeScript)
- **커밋 메시지**: Conventional Commits 형식
- **테스트**: 새로운 기능에 대한 테스트 코드 필수
- **문서화**: 코드 변경 시 관련 문서 업데이트

## 📞 지원 및 문의

### 문제 해결
- **기술적 문제**: [GitHub Issues](링크)
- **문서 관련**: [Documentation Issues](링크)
- **성능 이슈**: [Performance Issues](링크)

### 연락처
- **개발팀**: dev@cma-project.com
- **기술 지원**: support@cma-project.com
- **문서 관련**: docs@cma-project.com

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](링크) 파일을 참조하세요.

## 🔄 문서 업데이트

### 최근 업데이트 (2025년 1월 23일)
- ✅ **문서 구조 개선**: 중복 문서 통합 및 체계적 정리
- ✅ **API 문서 통합**: 개별 API 문서를 ENDPOINTS_DETAIL.md로 통합
- ✅ **아키텍처 문서 정리**: 폴더별 체계적 분류
- ✅ **개발 가이드 업데이트**: 하이브리드 아키텍처 전략 반영
- ✅ **성능 최적화 가이드**: 단계별 최적화 전략 추가
- ✅ **크로스 플랫폼 규칙**: Ubuntu → Windows 환경 전환 가이드

### 다음 업데이트 예정
- [ ] **사용자 매뉴얼 완성**: 실제 사용 시나리오 기반 가이드
- [ ] **성능 벤치마크**: 실제 성능 측정 결과 반영
- [ ] **보안 가이드 강화**: 구체적인 보안 체크리스트
- [ ] **배포 가이드 상세화**: 단계별 배포 프로세스

---

**마지막 업데이트**: 2025년 1월 23일  
**문서 버전**: v3.0  
**프로젝트 버전**: v1.2.0