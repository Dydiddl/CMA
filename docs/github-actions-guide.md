# GitHub Actions 활용 가이드

## 📋 개요

이 문서는 CMA 프로젝트에서 GitHub Actions를 활용하는 방법을 설명합니다.

## 🚀 설정된 워크플로우

### 1. CI/CD Pipeline (`ci.yml`)
메인 CI/CD 파이프라인으로 다음 작업들을 수행합니다:

#### 보안 검사
- **Trivy 취약점 스캐너**: 코드와 의존성의 보안 취약점 검사
- **GitHub Security Tab 연동**: 검사 결과를 GitHub Security 탭에 업로드

#### 프론트엔드 검증
- **Node.js 18 환경 설정**
- **의존성 설치 및 캐싱**
- **린터 실행** (`npm run lint`)
- **타입 체크** (`npm run type-check`)
- **테스트 실행 및 커버리지 측정** (`npm run test:coverage`)
- **빌드 검증** (`npm run build`)
- **아티팩트 업로드**

#### 백엔드 검증
- **Python 3.12 환경 설정**
- **PostgreSQL 14 서비스 컨테이너 실행**
- **의존성 설치 및 캐싱**
- **테스트 실행 및 커버리지 측정**
- **ASCR 모듈 테스트**
- **코드 포맷팅 검사** (black, isort)
- **보안 검사** (bandit, safety)

#### Tauri 데스크톱 앱
- **Rust 환경 설정**
- **의존성 캐싱**
- **앱 빌드**
- **테스트 실행**
- **실행 파일 아티팩트 업로드**

#### 성능 테스트
- **Locust를 사용한 부하 테스트**
- **main 브랜치에서만 실행**

#### 자동 배포
- **main 브랜치 푸시 시 자동 릴리즈 생성**
- **아티팩트를 GitHub Release에 업로드**

### 2. CodeQL 분석 (`codeql-analysis.yml`)
- **정적 코드 분석**: Python과 JavaScript 코드의 보안 취약점 검사
- **주간 스케줄링**: 매주 일요일 새벽 1시 30분에 자동 실행
- **GitHub Security Tab 연동**

### 3. 의존성 검토 (`dependency-review.yml`)
- **Pull Request 시 자동 실행**
- **의존성 보안 취약점 검사**
- **중간 이상 심각도의 취약점 발견 시 실패**

### 4. 알림 시스템 (`notify.yml`)
- **CI/CD 파이프라인 완료 시 Slack 알림**
- **성공/실패 상태에 따른 차별화된 메시지**

## 🔧 설정 방법

### 1. GitHub Secrets 설정

GitHub 저장소의 Settings > Secrets and variables > Actions에서 다음 시크릿을 설정해야 합니다:

```bash
# Slack 알림용 (선택사항)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

# 배포용 (필요시)
DEPLOY_KEY=your_deploy_private_key
DEPLOY_HOST=your_deploy_host
```

### 2. 브랜치 보호 규칙 설정

GitHub 저장소의 Settings > Branches에서 main 브랜치에 다음 규칙을 설정:

- ✅ **Require a pull request before merging**
- ✅ **Require status checks to pass before merging**
  - `frontend` (필수)
  - `backend` (필수)
  - `tauri` (필수)
  - `security-scan` (필수)
- ✅ **Require branches to be up to date before merging**
- ✅ **Require conversation resolution before merging**

### 3. GitHub Apps 설정

#### Codecov 연동
1. [Codecov](https://codecov.io)에 가입
2. GitHub 저장소 연결
3. 토큰을 GitHub Secrets에 추가

#### Slack 연동
1. Slack 워크스페이스에서 앱 생성
2. Incoming Webhook 설정
3. Webhook URL을 GitHub Secrets에 추가

## 📊 모니터링 및 분석

### 1. Actions 탭에서 확인 가능한 정보
- **워크플로우 실행 상태**
- **실행 시간 및 비용**
- **실패 원인 분석**
- **아티팩트 다운로드**

### 2. Security 탭에서 확인 가능한 정보
- **CodeQL 분석 결과**
- **Trivy 취약점 스캔 결과**
- **의존성 보안 취약점**

### 3. Insights 탭에서 확인 가능한 정보
- **커밋 활동**
- **코드 변경 통계**
- **기여자 분석**

## 🛠 로컬 개발에서 활용

### 1. 로컬에서 CI 검사 실행

```bash
# 프론트엔드 검사
cd frontend
npm run lint
npm run type-check
npm run test:coverage
npm run build

# 백엔드 검사
cd backend
python -m black --check .
python -m isort --check-only .
python -m pytest tests/ -v --cov=app
```

### 2. Pre-commit 훅 설정

```bash
# pre-commit 설치
pip install pre-commit

# 설정 파일 생성
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
EOF

# pre-commit 훅 설치
pre-commit install
```

## 🚨 문제 해결

### 1. 일반적인 실패 원인

#### 캐시 문제
```bash
# GitHub Actions에서 캐시 무효화
# 워크플로우 파일에서 캐시 키 변경
cache: 'npm-${{ hashFiles('**/package-lock.json') }}-${{ runner.os }}'
```

#### 의존성 문제
```bash
# requirements.txt 업데이트
pip freeze > requirements.txt

# package-lock.json 업데이트
npm ci
```

#### 권한 문제
```bash
# 워크플로우에 필요한 권한 추가
permissions:
  contents: read
  security-events: write
```

### 2. 디버깅 방법

#### 로그 확인
- GitHub Actions 탭에서 실패한 작업의 로그 확인
- 각 단계별 상세 로그 분석

#### 로컬 재현
```bash
# 동일한 환경에서 로컬 테스트
docker run --rm -v $(pwd):/app -w /app python:3.12 bash -c "pip install -r requirements.txt && python -m pytest"
```

## 📈 성능 최적화

### 1. 캐싱 전략
- **npm 캐시**: `node_modules` 캐싱
- **pip 캐시**: Python 패키지 캐싱
- **Rust 캐시**: Cargo 레지스트리 캐싱

### 2. 병렬 실행
- **독립적인 작업**: frontend, backend, tauri 병렬 실행
- **의존성 관리**: `needs` 키워드로 작업 순서 제어

### 3. 조건부 실행
```yaml
# 특정 브랜치에서만 실행
if: github.ref == 'refs/heads/main'

# 특정 파일 변경 시에만 실행
if: contains(github.event.head_commit.modified, 'backend/')
```

## 🔄 워크플로우 확장

### 1. 새로운 작업 추가
```yaml
new-job:
  runs-on: ubuntu-latest
  needs: [frontend, backend]
  steps:
    - uses: actions/checkout@v4
    - name: New step
      run: echo "New job"
```

### 2. 환경별 배포
```yaml
deploy-staging:
  if: github.ref == 'refs/heads/develop'
  # 스테이징 환경 배포

deploy-production:
  if: github.ref == 'refs/heads/main'
  # 프로덕션 환경 배포
```

### 3. 수동 실행
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: '배포 환경'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production
```

## 📚 추가 리소스

- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [GitHub Actions 예제](https://github.com/actions/starter-workflows)
- [CodeQL 가이드](https://docs.github.com/en/code-security/codeql-cli)
- [Trivy 문서](https://aquasecurity.github.io/trivy/)

## 🤝 기여 가이드

워크플로우를 수정하거나 새로운 워크플로우를 추가할 때:

1. **변경 사항 문서화**: 이 가이드 문서 업데이트
2. **테스트**: 로컬에서 워크플로우 테스트
3. **검토**: 팀원과 코드 리뷰 진행
4. **모니터링**: 배포 후 성능 및 안정성 모니터링 