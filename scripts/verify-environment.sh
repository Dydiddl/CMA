#!/bin/bash
# CMA 개발 환경 검증 스크립트
# 현재 환경이 CMA 프로젝트 개발에 적합한지 확인

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
    echo -e "${PURPLE}🔍 $1${NC}"
}

log_header() {
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}================================${NC}"
}

# 메인 함수
main() {
    log_header "CMA 개발 환경 검증을 시작합니다"
    
    # 기본 도구 검증
    verify_basic_tools
    
    # Python 환경 검증
    verify_python_environment
    
    # Node.js 환경 검증
    verify_node_environment
    
    # 에디터 및 확장 프로그램 검증
    verify_editor_extensions
    
    # 프로젝트 구조 검증
    verify_project_structure
    
    # 설정 파일 검증
    verify_config_files
    
    # 성능 검증
    verify_performance
    
    # 완료 메시지
    show_verification_summary
}

# 기본 도구 검증
verify_basic_tools() {
    log_step "기본 도구 검증 중..."
    
    local all_passed=true
    
    # Git 확인
    if command -v git &> /dev/null; then
        local git_version=$(git --version | cut -d' ' -f3)
        log_success "Git: $git_version"
    else
        log_error "Git이 설치되지 않았습니다"
        all_passed=false
    fi
    
    # 운영체제 확인
    local os=$(uname -s)
    local arch=$(uname -m)
    log_info "운영체제: $os ($arch)"
    
    # 메모리 확인
    if [ "$os" = "Darwin" ]; then
        local total_mem=$(sysctl -n hw.memsize | awk '{print $0/1024/1024/1024 " GB"}')
        log_info "총 메모리: $total_mem"
    elif [ "$os" = "Linux" ]; then
        local total_mem=$(free -g | awk 'NR==2{print $2 " GB"}')
        log_info "총 메모리: $total_mem"
    fi
    
    # 디스크 공간 확인
    local available_space=$(df -h . | awk 'NR==2{print $4}')
    log_info "사용 가능한 디스크 공간: $available_space"
    
    echo ""
}

# Python 환경 검증
verify_python_environment() {
    log_step "Python 환경 검증 중..."
    
    local all_passed=true
    
    # Python 버전 확인
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version | cut -d' ' -f2)
        log_success "Python3: $python_version"
        
        # Python 버전 호환성 확인
        local major_version=$(echo $python_version | cut -d'.' -f1)
        local minor_version=$(echo $python_version | cut -d'.' -f2)
        
        if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 8 ]; then
            log_success "Python 버전 호환성 확인됨 (3.8+)"
        else
            log_warning "Python 3.8 이상을 권장합니다 (현재: $python_version)"
        fi
    else
        log_error "Python3가 설치되지 않았습니다"
        all_passed=false
    fi
    
    # pip 확인
    if command -v pip3 &> /dev/null; then
        local pip_version=$(pip3 --version | cut -d' ' -f2)
        log_success "pip3: $pip_version"
    else
        log_error "pip3가 설치되지 않았습니다"
        all_passed=false
    fi
    
    # 가상환경 확인
    if [ -d "backend/venv" ]; then
        log_success "백엔드 가상환경 확인됨"
        
        # 가상환경 내 Python 버전 확인
        if [ -f "backend/venv/bin/python" ]; then
            local venv_python_version=$(backend/venv/bin/python --version | cut -d' ' -f2)
            log_info "백엔드 가상환경 Python: $venv_python_version"
        fi
    else
        log_warning "백엔드 가상환경이 없습니다"
    fi
    
    if [ -d "desktop/venv" ]; then
        log_success "데스크톱 가상환경 확인됨"
        
        # 가상환경 내 Python 버전 확인
        if [ -f "desktop/venv/bin/python" ]; then
            local venv_python_version=$(desktop/venv/bin/python --version | cut -d' ' -f2)
            log_info "데스크톱 가상환경 Python: $venv_python_version"
        fi
    else
        log_warning "데스크톱 가상환경이 없습니다"
    fi
    
    # 핵심 Python 패키지 확인
    if [ -d "backend/venv" ]; then
        log_info "백엔드 핵심 패키지 확인 중..."
        
        local required_packages=("fastapi" "uvicorn" "sqlalchemy" "pandas")
        for package in "${required_packages[@]}"; do
            if backend/venv/bin/pip show $package &> /dev/null; then
                local version=$(backend/venv/bin/pip show $package | grep Version | cut -d' ' -f2)
                log_success "$package: $version"
            else
                log_warning "$package이 설치되지 않았습니다"
            fi
        done
    fi
    
    echo ""
}

# Node.js 환경 검증
verify_node_environment() {
    log_step "Node.js 환경 검증 중..."
    
    # Node.js 확인
    if command -v node &> /dev/null; then
        local node_version=$(node --version)
        log_success "Node.js: $node_version"
        
        # Node.js 버전 호환성 확인
        local major_version=$(echo $node_version | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$major_version" -ge 16 ]; then
            log_success "Node.js 버전 호환성 확인됨 (16+)"
        else
            log_warning "Node.js 16 이상을 권장합니다 (현재: $node_version)"
        fi
    else
        log_warning "Node.js가 설치되지 않았습니다 (선택사항)"
    fi
    
    # npm 확인
    if command -v npm &> /dev/null; then
        local npm_version=$(npm --version)
        log_success "npm: $npm_version"
    else
        log_warning "npm이 설치되지 않았습니다 (선택사항)"
    fi
    
    # 프론트엔드 의존성 확인
    if [ -f "frontend/package.json" ]; then
        if [ -d "frontend/node_modules" ]; then
            log_success "프론트엔드 의존성 확인됨"
            
            # 핵심 패키지 확인
            local required_packages=("react" "typescript" "vite")
            for package in "${required_packages[@]}"; do
                if [ -d "frontend/node_modules/$package" ]; then
                    local version=$(cd frontend && npm list $package --depth=0 | grep $package | cut -d' ' -f2)
                    log_success "$package: $version"
                else
                    log_warning "$package이 설치되지 않았습니다"
                fi
            done
        else
            log_warning "프론트엔드 의존성이 설치되지 않았습니다"
        fi
    else
        log_info "프론트엔드 프로젝트가 없습니다"
    fi
    
    echo ""
}

# 에디터 및 확장 프로그램 검증
verify_editor_extensions() {
    log_step "에디터 및 확장 프로그램 검증 중..."
    
    # 에디터 확인
    if command -v cursor &> /dev/null; then
        log_success "Cursor가 설치되어 있습니다"
        EDITOR_CMD="cursor"
    elif command -v code &> /dev/null; then
        log_success "VSCode가 설치되어 있습니다"
        EDITOR_CMD="code"
    else
        log_warning "Cursor 또는 VSCode가 설치되지 않았습니다"
        return
    fi
    
    # 확장 프로그램 확인
    log_info "설치된 확장 프로그램 확인 중..."
    
    local required_extensions=(
        "ms-python.python"
        "ms-python.black-formatter"
        "ms-python.isort"
        "ms-python.flake8"
        "ms-vscode.vscode-typescript-next"
        "esbenp.prettier-vscode"
        "dbaeumer.vscode-eslint"
        "eamodio.gitlens"
        "yzhang.markdown-all-in-one"
    )
    
    local installed_extensions=$($EDITOR_CMD --list-extensions)
    local missing_extensions=()
    
    for extension in "${required_extensions[@]}"; do
        if echo "$installed_extensions" | grep -q "^$extension$"; then
            log_success "$extension"
        else
            log_warning "$extension (누락)"
            missing_extensions+=("$extension")
        fi
    done
    
    if [ ${#missing_extensions[@]} -gt 0 ]; then
        echo ""
        log_info "누락된 확장 프로그램 설치:"
        for extension in "${missing_extensions[@]}"; do
            echo "  $EDITOR_CMD --install-extension $extension"
        done
    fi
    
    echo ""
}

# 프로젝트 구조 검증
verify_project_structure() {
    log_step "프로젝트 구조 검증 중..."
    
    local required_dirs=(
        "backend"
        "frontend"
        "desktop"
        "docs"
        "scripts"
        ".vscode"
    )
    
    local required_files=(
        "README.md"
        "backend/requirements.txt"
        "frontend/package.json"
        ".vscode/settings.json"
        ".vscode/launch.json"
        ".vscode/extensions.json"
    )
    
    # 디렉토리 확인
    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            log_success "디렉토리: $dir"
        else
            log_warning "디렉토리 누락: $dir"
        fi
    done
    
    # 파일 확인
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            log_success "파일: $file"
        else
            log_warning "파일 누락: $file"
        fi
    done
    
    echo ""
}

# 설정 파일 검증
verify_config_files() {
    log_step "설정 파일 검증 중..."
    
    # .vscode/settings.json 확인
    if [ -f ".vscode/settings.json" ]; then
        if python3 -c "import json; json.load(open('.vscode/settings.json'))" 2>/dev/null; then
            log_success ".vscode/settings.json JSON 형식 확인됨"
        else
            log_error ".vscode/settings.json JSON 형식 오류"
        fi
    fi
    
    # .vscode/launch.json 확인
    if [ -f ".vscode/launch.json" ]; then
        if python3 -c "import json; json.load(open('.vscode/launch.json'))" 2>/dev/null; then
            log_success ".vscode/launch.json JSON 형식 확인됨"
        else
            log_error ".vscode/launch.json JSON 형식 오류"
        fi
    fi
    
    # .vscode/extensions.json 확인
    if [ -f ".vscode/extensions.json" ]; then
        if python3 -c "import json; json.load(open('.vscode/extensions.json'))" 2>/dev/null; then
            log_success ".vscode/extensions.json JSON 형식 확인됨"
        else
            log_error ".vscode/extensions.json JSON 형식 오류"
        fi
    fi
    
    echo ""
}

# 성능 검증
verify_performance() {
    log_step "성능 검증 중..."
    
    # Python 가상환경 활성화 시간 측정
    if [ -d "backend/venv" ]; then
        local start_time=$(date +%s%N)
        backend/venv/bin/python -c "print('Python 가상환경 테스트')" &> /dev/null
        local end_time=$(date +%s%N)
        local duration=$(( (end_time - start_time) / 1000000 ))
        log_info "Python 가상환경 활성화 시간: ${duration}ms"
        
        if [ $duration -lt 1000 ]; then
            log_success "Python 가상환경 성능 양호"
        else
            log_warning "Python 가상환경 활성화가 느립니다"
        fi
    fi
    
    # 디스크 I/O 성능 확인
    if command -v dd &> /dev/null; then
        local write_speed=$(dd if=/dev/zero of=/tmp/test_file bs=1M count=100 2>&1 | grep "MB/s" | awk '{print $8}')
        log_info "디스크 쓰기 속도: $write_speed"
        rm -f /tmp/test_file
    fi
    
    echo ""
}

# 검증 결과 요약
show_verification_summary() {
    log_header "🎯 환경 검증 완료!"
    
    echo -e "${GREEN}✅ 기본 검증이 완료되었습니다!${NC}"
    echo ""
    echo -e "${CYAN}📋 권장사항:${NC}"
    echo "1. 누락된 확장 프로그램이 있다면 설치하세요"
    echo "2. Python 가상환경이 없다면 생성하세요"
    echo "3. 의존성 패키지가 누락되었다면 설치하세요"
    echo "4. 성능 이슈가 있다면 시스템을 최적화하세요"
    echo ""
    echo -e "${YELLOW}💡 다음 단계:${NC}"
    echo "- 개발 시작: cursor CMA.code-workspace"
    echo "- 환경 설정: ./scripts/setup-development-environment.sh"
    echo "- 설정 동기화: Cursor/VSCode Settings Sync 활성화"
    echo ""
    echo -e "${PURPLE}🚀 CMA 하이브리드 아키텍처 개발을 시작하세요!${NC}"
}

# 스크립트 실행
main "$@" 