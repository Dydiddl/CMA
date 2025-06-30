# 배포 가이드

*최종 업데이트: 2025-01-23*

이 폴더는 CMA 시스템의 배포 관련 문서를 포함합니다.

## 🚀 배포 환경

### 지원 환경
- **운영체제**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.12+
- **Node.js**: 18+
- **PostgreSQL**: 14+
- **Redis**: 6.0+

### 하이브리드 아키텍처 배포
- **Python 백엔드**: FastAPI + SQLAlchemy
- **React 프론트엔드**: Tauri 2.x 데스크톱 앱
- **데이터베이스**: PostgreSQL (로컬) + Supabase (클라우드)

## 📋 배포 단계

### 1. 개발 환경 배포
- [개발 환경 설정](development-setup.md)
- [로컬 데이터베이스 설정](local-database.md)
- [개발 서버 실행](dev-server.md)

### 2. 테스트 환경 배포
- [테스트 환경 구성](test-environment.md)
- [테스트 데이터 설정](test-data.md)
- [자동화 테스트 실행](automated-tests.md)

### 3. 프로덕션 환경 배포
- [프로덕션 서버 설정](production-server.md)
- [데이터베이스 마이그레이션](database-migration.md)
- [SSL 인증서 설정](ssl-certificate.md)
- [로드 밸런서 구성](load-balancer.md)

### 4. 데스크톱 앱 배포
- [Tauri 빌드 설정](tauri-build.md)
- [코드 서명](code-signing.md)
- [인스톨러 생성](installer-creation.md)
- [업데이트 시스템](update-system.md)

## 🔧 배포 도구

### 자동화 스크립트
- [배포 스크립트](deploy.sh)
- [성능 최적화 스크립트](optimize-performance.py)
- [백업 스크립트](backup.sh)

### 모니터링 도구
- [성능 모니터링](performance-monitoring.md)
- [로그 관리](log-management.md)
- [알림 시스템](notification-system.md)

## 🛡️ 보안 고려사항

### 인증 및 권한
- [JWT 토큰 설정](jwt-configuration.md)
- [역할 기반 접근 제어](rbac.md)
- [API 보안](api-security.md)

### 데이터 보호
- [데이터 암호화](data-encryption.md)
- [백업 전략](backup-strategy.md)
- [재해 복구](disaster-recovery.md)

## 📊 성능 최적화

### 시스템 최적화
- [데이터베이스 튜닝](database-tuning.md)
- [캐싱 전략](caching-strategy.md)
- [비동기 처리](async-processing.md)

### 모니터링
- [성능 지표](performance-metrics.md)
- [리소스 사용량](resource-usage.md)
- [사용자 경험 모니터링](ux-monitoring.md)

## 🔄 업데이트 관리

### 버전 관리
- [시맨틱 버저닝](semantic-versioning.md)
- [릴리즈 노트](release-notes.md)
- [롤백 전략](rollback-strategy.md)

### 무중단 배포
- [Blue-Green 배포](blue-green-deployment.md)
- [Canary 배포](canary-deployment.md)
- [A/B 테스트](ab-testing.md)

## 📞 지원 및 문제 해결

### 배포 문제 해결
- [일반적인 배포 오류](common-deployment-errors.md)
- [로그 분석](log-analysis.md)
- [성능 문제 진단](performance-troubleshooting.md)

### 지원 채널
- [기술 지원](technical-support.md)
- [문서화](documentation.md)
- [커뮤니티](community.md) 