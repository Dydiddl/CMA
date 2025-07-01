# 🛠️ CMA 프로젝트 VSCode/Cursor 확장 프로그램 가이드

## 📋 개요

CMA 프로젝트의 **하이브리드 아키텍처** (Python + React + TypeScript) 개발을 위한 최적화된 VSCode/Cursor 확장 프로그램 가이드입니다.

### 🎯 대상 개발 환경
- **VSCode**: 모든 확장 프로그램 지원
- **Cursor**: VSCode 기반이므로 대부분 호환 (일부 AI 관련 확장 제외)

## 🐍 Python 개발 확장 (필수)

### 1. Python 코어 확장
```json
{
  "extensions": [
    "ms-python.python",                    // Python 언어 지원
    "ms-python.black-formatter",           // Black 코드 포맷터
    "ms-python.isort",                     // import 정렬
    "ms-python.flake8",                    // 코드 품질 검사
    "ms-python.pylint",                    // 추가 린팅
    "ms-python.pytest-adapter"             // pytest 통합
  ]
}
```

**설치 명령어:**
```bash
# Cursor에서 설치
cursor --install-extension ms-python.python
cursor --install-extension ms-python.black-formatter
cursor --install-extension ms-python.isort
cursor --install-extension ms-python.flake8
cursor --install-extension ms-python.pylint
cursor --install-extension ms-python.pytest-adapter
```

### 2. FastAPI 개발 확장
```json
{
  "extensions": [
    "ms-python.fastapi",                   // FastAPI 지원
    "ms-python.pydantic",                  // Pydantic 스키마 지원
    "ms-python.sqlalchemy"                 // SQLAlchemy 지원
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension ms-python.fastapi
cursor --install-extension ms-python.pydantic
cursor --install-extension ms-python.sqlalchemy
```

### 3. 데이터 과학 확장 (Pandas, Excel 처리)
```json
{
  "extensions": [
    "ms-python.jupyter",                   // Jupyter 노트북
    "ms-toolsai.jupyter-keymap",           // Jupyter 단축키
    "ms-toolsai.jupyter-renderers",        // 데이터 시각화
    "ms-python.pandas-profiler"            // Pandas 프로파일링
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension ms-python.jupyter
cursor --install-extension ms-toolsai.jupyter-keymap
cursor --install-extension ms-toolsai.jupyter-renderers
cursor --install-extension ms-python.pandas-profiler
```

## ⚛️ React/TypeScript 개발 확장 (필수)

### 1. TypeScript/React 코어
```json
{
  "extensions": [
    "ms-vscode.vscode-typescript-next",    // TypeScript 지원
    "bradlc.vscode-tailwindcss",           // Tailwind CSS (선택)
    "esbenp.prettier-vscode",              // Prettier 포맷터
    "dbaeumer.vscode-eslint",              // ESLint 린팅
    "ms-vscode.vscode-json"                // JSON 지원
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension ms-vscode.vscode-typescript-next
cursor --install-extension bradlc.vscode-tailwindcss
cursor --install-extension esbenp.prettier-vscode
cursor --install-extension dbaeumer.vscode-eslint
cursor --install-extension ms-vscode.vscode-json
```

### 2. React 개발 도구
```json
{
  "extensions": [
    "ms-vscode.vscode-react-native",       // React Native (선택)
    "formulahendry.auto-rename-tag",       // 태그 자동 리네임
    "christian-kohler.path-intellisense",  // 경로 자동완성
    "ms-vscode.vscode-css-peek"            // CSS 정의 찾기
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension ms-vscode.vscode-react-native
cursor --install-extension formulahendry.auto-rename-tag
cursor --install-extension christian-kohler.path-intellisense
cursor --install-extension ms-vscode.vscode-css-peek
```

### 3. Mantine/MUI 지원
```json
{
  "extensions": [
    "bradlc.vscode-tailwindcss",           // Mantine CSS 유틸리티
    "ms-vscode.vscode-css-peek",           // CSS 컴포넌트 탐색
    "formulahendry.auto-close-tag"         // 태그 자동 닫기
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension bradlc.vscode-tailwindcss
cursor --install-extension ms-vscode.vscode-css-peek
cursor --install-extension formulahendry.auto-close-tag
```

## 🗄️ 데이터베이스 개발 확장

### 1. PostgreSQL 지원
```json
{
  "extensions": [
    "ckolkman.vscode-postgres",            // PostgreSQL 클라이언트
    "ms-mssql.mssql",                      // SQL Server (선택)
    "mtxr.sqltools",                       // SQL 도구
    "mtxr.sqltools-driver-pg"              // PostgreSQL 드라이버
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension ckolkman.vscode-postgres
cursor --install-extension ms-mssql.mssql
cursor --install-extension mtxr.sqltools
cursor --install-extension mtxr.sqltools-driver-pg
```

### 2. Redis 지원
```json
{
  "extensions": [
    "cweijan.vscode-redis-client",         // Redis 클라이언트
    "ms-vscode.vscode-redis"               // Redis 지원
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension cweijan.vscode-redis-client
cursor --install-extension ms-vscode.vscode-redis
```

## 📊 PDF/Excel 처리 확장 (ASCR 모듈)

### 1. 파일 처리 지원
```json
{
  "extensions": [
    "ms-vscode.vscode-pdf",                // PDF 뷰어
    "janisdd.vscode-edit-csv",             // CSV 편집기
    "mechatroner.rainbow-csv",             // CSV 하이라이팅
    "ms-vscode.vscode-excel"               // Excel 지원
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension ms-vscode.vscode-pdf
cursor --install-extension janisdd.vscode-edit-csv
cursor --install-extension mechatroner.rainbow-csv
cursor --install-extension ms-vscode.vscode-excel
```

### 2. 문서 처리 도구
```json
{
  "extensions": [
    "yzhang.markdown-all-in-one",          // Markdown 지원
    "shd101wyy.markdown-preview-enhanced", // 고급 Markdown 미리보기
    "ms-vscode.vscode-yaml"                // YAML 지원
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension yzhang.markdown-all-in-one
cursor --install-extension shd101wyy.markdown-preview-enhanced
cursor --install-extension ms-vscode.vscode-yaml
```

## 🚀 성능 최적화 확장

### 1. 성능 모니터링
```json
{
  "extensions": [
    "ms-vscode.vscode-json",               // JSON 성능 분석
    "ms-vscode.vscode-typescript-next",    // TypeScript 성능
    "ms-python.python"                     // Python 성능 분석
  ]
}
```

### 2. 메모리 최적화
```json
{
  "extensions": [
    "ms-vscode.vscode-json",               // JSON 메모리 사용량
    "ms-python.python"                     // Python 메모리 프로파일링
  ]
}
```

## 🔧 개발 생산성 확장

### 1. 코드 생성 및 자동완성
```json
{
  "extensions": [
    "ms-python.python",                    // Python 자동완성
    "ms-vscode.vscode-typescript-next",    // TypeScript 자동완성
    "ms-python.black-formatter",           // 자동 포맷팅
    "esbenp.prettier-vscode",              // Prettier 자동 포맷팅
    "ms-vscode.vscode-json"                // JSON 스키마 검증
  ]
}
```

### 2. Git 및 버전 관리
```json
{
  "extensions": [
    "eamodio.gitlens",                     // Git 히스토리 및 블라임
    "mhutchie.git-graph",                  // Git 그래프
    "donjayamanne.githistory",             // Git 히스토리
    "ms-vscode.vscode-git"                 // Git 기본 지원
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension eamodio.gitlens
cursor --install-extension mhutchie.git-graph
cursor --install-extension donjayamanne.githistory
cursor --install-extension ms-vscode.vscode-git
```

### 3. 터미널 및 개발 환경
```json
{
  "extensions": [
    "ms-vscode.vscode-terminal",           // 통합 터미널
    "ms-vscode.vscode-docker",             // Docker 지원
    "ms-azuretools.vscode-docker"          // Docker 컨테이너
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension ms-vscode.vscode-terminal
cursor --install-extension ms-vscode.vscode-docker
cursor --install-extension ms-azuretools.vscode-docker
```

## 🧪 테스트 및 디버깅 확장

### 1. 테스트 도구
```json
{
  "extensions": [
    "ms-python.pytest-adapter",            // pytest 통합
    "ms-vscode.vscode-jest",               // Jest 테스트
    "ms-vscode.vscode-js-debug",           // JavaScript 디버깅
    "ms-python.python"                     // Python 디버깅
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension ms-python.pytest-adapter
cursor --install-extension ms-vscode.vscode-jest
cursor --install-extension ms-vscode.vscode-js-debug
```

### 2. 디버깅 도구
```json
{
  "extensions": [
    "ms-vscode.vscode-js-debug",           // JavaScript 디버거
    "ms-python.python",                    // Python 디버거
    "ms-vscode.vscode-json"                // JSON 디버깅
  ]
}
```

## 🎨 UI/UX 개발 확장

### 1. 색상 및 아이콘
```json
{
  "extensions": [
    "pkief.material-icon-theme",           // Material 아이콘
    "zhuangtongfa.material-theme",         // Material 테마
    "ms-vscode.theme-tomorrowkit"          // Tomorrow 테마
  ]
}
```

**설치 명령어:**
```bash
cursor --install-extension pkief.material-icon-theme
cursor --install-extension zhuangtongfa.material-theme
cursor --install-extension ms-vscode.theme-tomorrowkit
```

### 2. 레이아웃 및 네비게이션
```json
{
  "extensions": [
    "ms-vscode.vscode-explorer",           // 파일 탐색기
    "ms-vscode.vscode-search",             // 검색 기능
    "ms-vscode.vscode-settings"            // 설정 관리
  ]
}
```

## 🚀 일괄 설치 스크립트

### 전체 확장 프로그램 설치 스크립트

```bash
#!/bin/bash
# CMA 프로젝트 확장 프로그램 일괄 설치 스크립트

echo "🚀 CMA 프로젝트 확장 프로그램 설치를 시작합니다..."

# Python 개발 확장
echo "📦 Python 개발 확장 설치 중..."
cursor --install-extension ms-python.python
cursor --install-extension ms-python.black-formatter
cursor --install-extension ms-python.isort
cursor --install-extension ms-python.flake8
cursor --install-extension ms-python.pylint
cursor --install-extension ms-python.pytest-adapter
cursor --install-extension ms-python.fastapi
cursor --install-extension ms-python.pydantic
cursor --install-extension ms-python.sqlalchemy
cursor --install-extension ms-python.jupyter

# React/TypeScript 개발 확장
echo "⚛️ React/TypeScript 개발 확장 설치 중..."
cursor --install-extension ms-vscode.vscode-typescript-next
cursor --install-extension esbenp.prettier-vscode
cursor --install-extension dbaeumer.vscode-eslint
cursor --install-extension formulahendry.auto-rename-tag
cursor --install-extension christian-kohler.path-intellisense
cursor --install-extension ms-vscode.vscode-css-peek
cursor --install-extension formulahendry.auto-close-tag

# 데이터베이스 확장
echo "🗄️ 데이터베이스 확장 설치 중..."
cursor --install-extension ckolkman.vscode-postgres
cursor --install-extension cweijan.vscode-redis-client
cursor --install-extension mtxr.sqltools
cursor --install-extension mtxr.sqltools-driver-pg

# 파일 처리 확장
echo "📊 파일 처리 확장 설치 중..."
cursor --install-extension ms-vscode.vscode-pdf
cursor --install-extension janisdd.vscode-edit-csv
cursor --install-extension mechatroner.rainbow-csv
cursor --install-extension yzhang.markdown-all-in-one
cursor --install-extension ms-vscode.vscode-yaml

# 개발 생산성 확장
echo "🔧 개발 생산성 확장 설치 중..."
cursor --install-extension eamodio.gitlens
cursor --install-extension mhutchie.git-graph
cursor --install-extension ms-vscode.vscode-docker
cursor --install-extension ms-vscode.vscode-terminal

# 테스트 및 디버깅 확장
echo "🧪 테스트 및 디버깅 확장 설치 중..."
cursor --install-extension ms-vscode.vscode-jest
cursor --install-extension ms-vscode.vscode-js-debug

# UI/UX 확장
echo "🎨 UI/UX 확장 설치 중..."
cursor --install-extension pkief.material-icon-theme
cursor --install-extension zhuangtongfa.material-theme

echo "✅ 모든 확장 프로그램 설치가 완료되었습니다!"
echo "🔄 Cursor를 재시작하여 확장 프로그램을 활성화하세요."
```

### 스크립트 실행 방법

```bash
# 스크립트 파일 생성
cat > install-extensions.sh << 'EOF'
#!/bin/bash
# 위의 스크립트 내용
EOF

# 실행 권한 부여
chmod +x install-extensions.sh

# 스크립트 실행
./install-extensions.sh
```

## ⚙️ VSCode/Cursor 설정

### 프로젝트별 설정 파일

`.vscode/settings.json` 파일을 생성하고 다음 설정을 추가하세요:

```json
{
  // Python 설정
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.flake8Enabled": true,
  "python.sortImports.args": ["--profile", "black"],
  
  // TypeScript 설정
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.suggest.autoImports": true,
  "typescript.updateImportsOnFileMove.enabled": "always",
  
  // 포맷팅 설정
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true,
    "source.fixAll.eslint": true
  },
  
  // 파일 연결 설정
  "files.associations": {
    "*.py": "python",
    "*.tsx": "typescriptreact",
    "*.ts": "typescript",
    "*.json": "json",
    "*.yaml": "yaml",
    "*.yml": "yaml"
  },
  
  // 탐색기 설정
  "explorer.fileNesting.enabled": true,
  "explorer.fileNesting.patterns": {
    "*.py": "${capture}.py, ${capture}_test.py, test_${capture}.py",
    "*.tsx": "${capture}.tsx, ${capture}.test.tsx, ${capture}.spec.tsx",
    "*.ts": "${capture}.ts, ${capture}.test.ts, ${capture}.spec.ts"
  },
  
  // CMA 프로젝트 특화 설정
  "python.analysis.extraPaths": [
    "./backend",
    "./backend/app",
    "./backend/app/services/ascr"
  ],
  
  // 테스트 설정
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "./backend/tests"
  ],
  
  // 디버깅 설정
  "python.terminal.activateEnvironment": true,
  "python.terminal.activateEnvInCurrentTerminal": true
}
```

### 작업 영역 설정

`.vscode/launch.json` 파일을 생성하여 디버깅 설정을 추가하세요:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

## 🔍 확장 프로그램 호환성 확인

### Cursor에서 확인 가능한 확장 프로그램

Cursor는 VSCode 기반이므로 대부분의 확장 프로그램이 호환됩니다. 다음 명령어로 설치된 확장 프로그램을 확인할 수 있습니다:

```bash
# 설치된 확장 프로그램 목록 확인
cursor --list-extensions

# 특정 확장 프로그램 설치 상태 확인
cursor --list-extensions | grep ms-python.python
```

### 호환성 문제 해결

일부 확장 프로그램이 Cursor에서 작동하지 않는 경우:

1. **VSCode에서 직접 설치**: VSCode를 열고 확장 프로그램을 설치한 후 Cursor에서 사용
2. **대체 확장 프로그램 사용**: 비슷한 기능을 제공하는 다른 확장 프로그램 사용
3. **Cursor 내장 기능 활용**: Cursor의 AI 기능을 활용하여 확장 프로그램 기능 대체

## 📝 사용 팁

### 1. 확장 프로그램 관리
- 정기적으로 사용하지 않는 확장 프로그램 비활성화
- 프로젝트별로 필요한 확장 프로그램만 활성화
- 확장 프로그램 업데이트 정기 확인

### 2. 성능 최적화
- 너무 많은 확장 프로그램 동시 사용 방지
- 메모리 사용량이 높은 확장 프로그램 주의
- 필요시 확장 프로그램 비활성화

### 3. 팀 협업
- `.vscode/extensions.json` 파일로 팀원들과 확장 프로그램 공유
- 프로젝트별 권장 확장 프로그램 목록 유지
- 확장 프로그램 설정 동기화

## 🎯 결론

이 가이드를 따라 CMA 프로젝트에 최적화된 개발 환경을 구축하면 **하이브리드 아키텍처** 개발의 생산성을 크게 향상시킬 수 있습니다. Cursor의 AI 기능과 함께 사용하면 더욱 효율적인 개발이 가능합니다. 