# 건설 관리 시스템 문서

*최종 업데이트: 2025-01-23*

이 디렉토리는 CMA (Construction Management System)의 전체 문서를 포함하고 있습니다.

## 📚 문서 구조

### 1. 시스템 개요
- [프로젝트 목표](project_goals.md)
- [프로젝트 진행 현황](project_progress.md)
- [컴포넌트 구성](components.md)

### 2. 아키텍처
- [시스템 아키텍처 개요](architecture.md)
- [프론트엔드 아키텍처](frontend_architecture.md)
- [데이터베이스 설계](architecture/database-schema.md)
- [현재 데이터베이스 스키마](architecture/current-database-schema.md)

### 3. API 문서
- [API 개요](api/api-overview.md)
- [API 엔드포인트](api_endpoints.md)
- [API 버전 관리](api/versioning.md)

#### 3.1 API v1
- [API v1 명세](api/v1/api.md)
- [계약 관리](api/v1/endpoints/contracts.md)
- [재무 관리](api/v1/endpoints/financial.md)
- [노무 관리](api/v1/endpoints/labor.md)

#### 3.2 공통 사항
- [인증](api/common/authentication.md)
- [에러 처리](api/common/error-handling.md)
- [보안](api/common/security.md)

### 4. 개발 가이드
- [개발 환경 설정](development/setup-guide.md)
- [개발 가이드라인](development/development-guide.md)
- [코딩 표준](development/coding-standards.md)
- [Cursor 규칙 유지보수](development/cursor-rules-maintenance.md)

### 5. 설계 문서
- [설계 개요](design/design-overview.md)
- [API 설계](design/api-design.md)
- [데이터베이스 설계](design/database-schema.md)
- [ASCR 명세](design/ascr-spec.md)

### 6. 사용자 가이드
- [시작하기](user-guide/README.md)
- [기능별 가이드](user-guide/README.md#기능별-가이드)
- [고급 기능](user-guide/README.md#고급-기능)
- [문제 해결](user-guide/README.md#문제-해결)

### 7. 배포 가이드
- [배포 환경](deployment/README.md)
- [개발 환경 배포](deployment/README.md#1-개발-환경-배포)
- [테스트 환경 배포](deployment/README.md#2-테스트-환경-배포)
- [프로덕션 환경 배포](deployment/README.md#3-프로덕션-환경-배포)

### 8. 문제 해결
- [문제 해결 프로세스](troubleshooting/README.md)
- [일반적인 문제](troubleshooting/README.md#일반적인-문제)
- [성능 문제](troubleshooting/README.md#성능-문제)
- [보안 문제](troubleshooting/README.md#보안-문제)

### 9. 변경 로그
- [버전 관리](changelog/README.md)
- [버전별 변경 로그](changelog/README.md#버전별-변경-로그)
- [주요 마일스톤](changelog/README.md#주요-마일스톤)

## 🔍 문서 작성 가이드라인

1. **문서 형식**
   - 모든 문서는 Markdown 형식으로 작성
   - 각 문서 상단에 최종 업데이트 일자 포함
   - 목차는 필수 (문서가 긴 경우)

2. **문서 업데이트**
   - 코드 변경 시 관련 문서도 함께 업데이트
   - 주요 변경사항은 [changelog](changelog/README.md)에 기록
   - 문서 리뷰는 코드 리뷰의 일부로 포함

3. **상호 참조**
   - 관련 문서는 상대 경로로 링크
   - 코드 참조는 라인 번호 포함
   - API 엔드포인트는 실제 URL 포함

## 🔄 문서 관리 프로세스

1. **정기 검토**
   - 월 1회 전체 문서 검토
   - 분기별 문서 구조 개선
   - 연 2회 전체 문서 감사

2. **버전 관리**
   - 주요 버전 변경 시 문서 태그 생성
   - 문서 변경 이력 관리
   - 오래된 버전 문서 보관

3. **피드백 및 개선**
   - 문서 개선 제안은 이슈로 등록
   - 문서 오류는 즉시 수정
   - 사용자 피드백 반영

## 📌 주요 링크

- [프로젝트 저장소](https://github.com/Dydiddl/CMA)
- [이슈 트래커](https://github.com/Dydiddl/CMA/issues)
- [위키](https://github.com/Dydiddl/CMA/wiki)

## 🤝 기여 방법

1. 문서 개선 제안
2. 오타 또는 잘못된 정보 수정
3. 새로운 문서 작성
4. 번역 지원

## 📞 지원 및 문의

- 이메일: support@example.com
- 이슈 등록: [새 이슈 만들기](https://github.com/Dydiddl/CMA/issues/new)
- 기술 지원: [문제 해결 가이드](troubleshooting/README.md) 