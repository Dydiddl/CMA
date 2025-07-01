#!/bin/bash
# CMA 개발 환경 설정 스크립트
# 모든 환경(개발 PC, 노트북, 클라우드 IDE)에서 일관된 개발 환경 구축

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_step() {
    echo -e "${PURPLE}🚀 $1${NC}"
}

log_header() {
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}================================${NC}"
}

# 메인 함수
main() {
    log_header "CMA 개발 환경 설정을 시작합니다"
    
    # 운영체제 확인
    detect_os
    
    # 필수 도구 확인
    check_prerequisites
    
    # 에디터 확인
    detect_editor
    
    # 확장 프로그램 설치
    install_extensions
    
    # Python 환경 설정
    setup_python_environment
    
    # Node.js 환경 설정
    setup_node_environment
    
    # 프로젝트 설정 파일 생성
    create_project_files
    
    # 환경 검증
    verify_environment
    
    # 완료 메시지
    show_completion_message
}

# 운영체제 감지
detect_os() {
    log_step "운영체제 감지 중..."
    
    OS="$(uname -s)"
    case "${OS}" in
        Linux*)     MACHINE=Linux;;
        Darwin*)    MACHINE=Mac;;
        CYGWIN*)    MACHINE=Cygwin;;
        MINGW*)     MACHINE=MinGw;;
        *)          MACHINE="UNKNOWN:${OS}"
    esac
    
    log_success "운영체제: $MACHINE"
    echo ""
}

# 필수 도구 확인
check_prerequisites() {
    log_step "필수 도구 확인 중..."
    
    local missing_tools=()
    
    # Python 확인
    if command -v python3 &> /dev/null; then
        log_success "Python3: $(python3 --version)"
    else
        log_error "Python3가 설치되지 않았습니다"
        missing_tools+=("python3")
    fi
    
    # Node.js 확인
    if command -v node &> /dev/null; then
        log_success "Node.js: $(node --version)"
    else
        log_warning "Node.js가 설치되지 않았습니다 (선택사항)"
    fi
    
    # npm 확인
    if command -v npm &> /dev/null; then
        log_success "npm: $(npm --version)"
    else
        log_warning "npm이 설치되지 않았습니다 (선택사항)"
    fi
    
    # Git 확인
    if command -v git &> /dev/null; then
        log_success "Git: $(git --version)"
    else
        log_error "Git이 설치되지 않았습니다"
        missing_tools+=("git")
    fi
    
    # 누락된 도구가 있으면 종료
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "다음 도구들을 먼저 설치해주세요: ${missing_tools[*]}"
        exit 1
    fi
    
    echo ""
}

# 에디터 감지
detect_editor() {
    log_step "에디터 감지 중..."
    
    if command -v cursor &> /dev/null; then
        EDITOR_CMD="cursor"
        log_success "Cursor가 감지되었습니다"
    elif command -v code &> /dev/null; then
        EDITOR_CMD="code"
        log_success "VSCode가 감지되었습니다"
    else
        log_error "Cursor 또는 VSCode가 설치되지 않았습니다"
        log_info "다음 중 하나를 설치해주세요:"
        log_info "- Cursor: https://cursor.sh"
        log_info "- VSCode: https://code.visualstudio.com"
        exit 1
    fi
    
    echo ""
}

# 확장 프로그램 설치
install_extensions() {
    log_step "확장 프로그램 설치 중..."
    
    # Python 개발 확장
    log_info "Python 개발 확장 설치 중..."
    $EDITOR_CMD --install-extension ms-python.python
    $EDITOR_CMD --install-extension ms-python.black-formatter
    $EDITOR_CMD --install-extension ms-python.isort
    $EDITOR_CMD --install-extension ms-python.flake8
    
    # TypeScript/React 개발 확장
    log_info "TypeScript/React 개발 확장 설치 중..."
    $EDITOR_CMD --install-extension ms-vscode.vscode-typescript-next
    $EDITOR_CMD --install-extension esbenp.prettier-vscode
    $EDITOR_CMD --install-extension dbaeumer.vscode-eslint
    $EDITOR_CMD --install-extension formulahendry.auto-rename-tag
    $EDITOR_CMD --install-extension formulahendry.auto-close-tag
    $EDITOR_CMD --install-extension christian-kohler.path-intellisense
    
    # 개발 생산성 확장
    log_info "개발 생산성 확장 설치 중..."
    $EDITOR_CMD --install-extension eamodio.gitlens
    $EDITOR_CMD --install-extension mhutchie.git-graph
    $EDITOR_CMD --install-extension yzhang.markdown-all-in-one
    
    # 운영체제별 추가 확장
    if [ "$MACHINE" = "Mac" ]; then
        log_info "macOS 전용 확장 설치 중..."
        $EDITOR_CMD --install-extension ms-vscode.vscode-terminal
    elif [ "$MACHINE" = "Linux" ]; then
        log_info "Linux 전용 확장 설치 중..."
        $EDITOR_CMD --install-extension ms-vscode.vscode-terminal
    fi
    
    log_success "확장 프로그램 설치 완료"
    echo ""
}

# Python 환경 설정
setup_python_environment() {
    log_step "Python 환경 설정 중..."
    
    # 백엔드 가상환경 설정
    if [ ! -d "backend/venv" ]; then
        log_info "백엔드 가상환경 생성 중..."
        python3 -m venv backend/venv
        log_success "백엔드 가상환경 생성 완료"
    else
        log_info "백엔드 가상환경이 이미 존재합니다"
    fi
    
    # 데스크톱 가상환경 설정
    if [ ! -d "desktop/venv" ]; then
        log_info "데스크톱 가상환경 생성 중..."
        python3 -m venv desktop/venv
        log_success "데스크톱 가상환경 생성 완료"
    else
        log_info "데스크톱 가상환경이 이미 존재합니다"
    fi
    
    # 백엔드 의존성 설치
    if [ -f "backend/requirements.txt" ]; then
        log_info "백엔드 의존성 설치 중..."
        backend/venv/bin/pip install --upgrade pip
        backend/venv/bin/pip install -r backend/requirements.txt
        log_success "백엔드 의존성 설치 완료"
    else
        log_warning "backend/requirements.txt 파일이 없습니다"
    fi
    
    # 데스크톱 의존성 설치
    if [ -f "desktop/requirements.txt" ]; then
        log_info "데스크톱 의존성 설치 중..."
        desktop/venv/bin/pip install --upgrade pip
        desktop/venv/bin/pip install -r desktop/requirements.txt
        log_success "데스크톱 의존성 설치 완료"
    else
        log_warning "desktop/requirements.txt 파일이 없습니다"
    fi
    
    echo ""
}

# Node.js 환경 설정
setup_node_environment() {
    log_step "Node.js 환경 설정 중..."
    
    if [ -f "frontend/package.json" ]; then
        log_info "프론트엔드 의존성 설치 중..."
        cd frontend
        npm install
        cd ..
        log_success "프론트엔드 의존성 설치 완료"
    else
        log_warning "frontend/package.json 파일이 없습니다"
    fi
    
    echo ""
}

# 프로젝트 설정 파일 생성
create_project_files() {
    log_step "프로젝트 설정 파일 생성 중..."
    
    # .vscode 폴더 생성
    mkdir -p .vscode
    
    # workspace.code-workspace 파일 생성
    if [ ! -f "CMA.code-workspace" ]; then
        log_info "작업 영역 파일 생성 중..."
        cat > CMA.code-workspace << 'EOF'
{
  "folders": [
    {
      "name": "CMA Project",
      "path": "."
    },
    {
      "name": "Backend",
      "path": "./backend"
    },
    {
      "name": "Frontend", 
      "path": "./frontend"
    },
    {
      "name": "Desktop",
      "path": "./desktop"
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "./backend/venv/bin/python",
    "typescript.preferences.importModuleSpecifier": "relative",
    "editor.formatOnSave": true,
    "workbench.colorTheme": "Cursor Dark",
    "workbench.iconTheme": "material-icon-theme"
  },
  "extensions": {
    "recommendations": [
      "ms-python.python",
      "ms-vscode.vscode-typescript-next",
      "eamodio.gitlens"
    ]
  }
}
EOF
        log_success "작업 영역 파일 생성 완료"
    fi
    
    echo ""
}

# 환경 검증
verify_environment() {
    log_step "환경 검증 중..."
    
    # 가상환경 확인
    if [ -d "backend/venv" ]; then
        log_success "백엔드 가상환경 확인됨"
    else
        log_error "백엔드 가상환경이 없습니다"
    fi
    
    if [ -d "desktop/venv" ]; then
        log_success "데스크톱 가상환경 확인됨"
    else
        log_error "데스크톱 가상환경이 없습니다"
    fi
    
    # 확장 프로그램 확인
    log_info "설치된 확장 프로그램 확인 중..."
    $EDITOR_CMD --list-extensions | grep -E "(ms-python|ms-vscode|eamodio)" > /dev/null && \
        log_success "필수 확장 프로그램 확인됨" || \
        log_warning "일부 확장 프로그램이 누락되었을 수 있습니다"
    
    echo ""
}

# 완료 메시지
show_completion_message() {
    log_header "🎉 개발 환경 설정 완료!"
    
    echo -e "${GREEN}✅ 모든 설정이 완료되었습니다!${NC}"
    echo ""
    echo -e "${CYAN}📋 다음 단계:${NC}"
    echo "1. $EDITOR_CMD CMA.code-workspace 으로 프로젝트 열기"
    echo "2. 권장 확장 프로그램 설치 확인"
    echo "3. Python 인터프리터 설정 확인"
    echo "4. 개발 시작!"
    echo ""
    echo -e "${YELLOW}💡 팁:${NC}"
    echo "- 환경 검증: ./scripts/verify-environment.sh"
    echo "- 설정 동기화: Cursor/VSCode의 Settings Sync 활성화"
    echo "- 팀 협업: .vscode/ 폴더의 설정 파일들을 Git에 커밋"
    echo ""
    echo -e "${PURPLE}🚀 CMA 하이브리드 아키텍처 개발을 시작하세요!${NC}"
}

# 스크립트 실행
main "$@" 