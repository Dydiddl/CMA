#!/bin/bash

# 🚀 D 드라이브 WSL2 개발 환경 자동 설정 스크립트
# CMA 프로젝트용 WSL2 환경 구축

set -e  # 오류 발생 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 제목 출력
print_title() {
    echo -e "${BLUE}"
    echo "=========================================="
    echo "  D 드라이브 WSL2 개발 환경 설정 스크립트"
    echo "  CMA 프로젝트용"
    echo "=========================================="
    echo -e "${NC}"
}

# 시스템 정보 확인
check_system() {
    log_info "시스템 정보 확인 중..."
    
    # Ubuntu 버전 확인
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        log_info "OS: $NAME $VERSION"
    fi
    
    # 메모리 확인
    total_mem=$(free -m | awk 'NR==2{printf "%.1f", $2/1024}')
    log_info "총 메모리: ${total_mem}GB"
    
    # 디스크 공간 확인
    available_space=$(df -h / | awk 'NR==2{print $4}')
    log_info "사용 가능한 디스크 공간: $available_space"
    
    # Python 버전 확인
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version)
        log_info "Python: $python_version"
    else
        log_error "Python3가 설치되어 있지 않습니다."
        exit 1
    fi
}

# 기본 도구 설치
install_basic_tools() {
    log_info "기본 도구 설치 중..."
    
    # 패키지 목록 업데이트
    sudo apt update
    
    # 기본 도구 설치
    sudo apt install -y \
        git \
        curl \
        wget \
        build-essential \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        htop \
        tree \
        vim \
        nano \
        unzip \
        zip \
        jq \
        httpie \
        tmux
    
    log_success "기본 도구 설치 완료"
}

# Python 환경 설정
setup_python() {
    log_info "Python 환경 설정 중..."
    
    # pip 업그레이드
    python3 -m pip install --upgrade pip
    
    # Python 가상환경 도구 설치
    sudo apt install -y python3-venv
    
    # pip 캐시 정리
    pip cache purge
    
    log_success "Python 환경 설정 완료"
}

# Node.js 설치
install_nodejs() {
    log_info "Node.js 설치 중..."
    
    # Node.js 18.x 저장소 추가
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    
    # Node.js 설치
    sudo apt install -y nodejs
    
    # npm 업그레이드
    sudo npm install -g npm@latest
    
    # 버전 확인
    node_version=$(node --version)
    npm_version=$(npm --version)
    log_info "Node.js: $node_version"
    log_info "npm: $npm_version"
    
    # npm 캐시 정리
    npm cache clean --force
    
    log_success "Node.js 설치 완료"
}

# PostgreSQL 설치
install_postgresql() {
    log_info "PostgreSQL 설치 중..."
    
    # PostgreSQL 설치
    sudo apt install -y postgresql postgresql-contrib
    
    # 서비스 시작
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    # 상태 확인
    if sudo systemctl is-active --quiet postgresql; then
        log_success "PostgreSQL 서비스 시작 완료"
    else
        log_error "PostgreSQL 서비스 시작 실패"
        exit 1
    fi
    
    # 기본 데이터베이스 생성
    sudo -u postgres createdb cma_db 2>/dev/null || log_warning "cma_db 데이터베이스가 이미 존재합니다."
    
    log_success "PostgreSQL 설치 완료"
}

# Redis 설치
install_redis() {
    log_info "Redis 설치 중..."
    
    # Redis 설치
    sudo apt install -y redis-server
    
    # 서비스 시작
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
    # 상태 확인
    if sudo systemctl is-active --quiet redis-server; then
        log_success "Redis 서비스 시작 완료"
    else
        log_error "Redis 서비스 시작 실패"
        exit 1
    fi
    
    log_success "Redis 설치 완료"
}

# Git 설정
setup_git() {
    log_info "Git 설정 중..."
    
    # Git 설정 (사용자가 직접 입력하도록 안내)
    log_warning "Git 사용자 정보를 설정해주세요:"
    echo "예시:"
    echo "  git config --global user.name \"Your Name\""
    echo "  git config --global user.email \"your.email@example.com\""
    echo ""
    
    read -p "Git 사용자 이름을 입력하세요: " git_name
    read -p "Git 이메일을 입력하세요: " git_email
    
    if [ -n "$git_name" ] && [ -n "$git_email" ]; then
        git config --global user.name "$git_name"
        git config --global user.email "$git_email"
        git config --global init.defaultBranch main
        log_success "Git 설정 완료"
    else
        log_warning "Git 설정을 건너뜁니다. 나중에 수동으로 설정해주세요."
    fi
}

# 프로젝트 폴더 구조 생성
create_project_structure() {
    log_info "프로젝트 폴더 구조 생성 중..."
    
    # 홈 디렉토리로 이동
    cd ~
    
    # 폴더 생성
    mkdir -p projects
    mkdir -p venvs
    mkdir -p data
    mkdir -p logs
    mkdir -p backups
    
    # 권한 설정
    chmod 755 projects venvs data logs backups
    
    log_success "프로젝트 폴더 구조 생성 완료"
    
    # 폴더 구조 출력
    log_info "생성된 폴더 구조:"
    tree -L 2 ~/projects ~/venvs ~/data ~/logs ~/backups 2>/dev/null || ls -la ~/projects ~/venvs ~/data ~/logs ~/backups
}

# CMA 프로젝트 설정
setup_cma_project() {
    log_info "CMA 프로젝트 설정 중..."
    
    cd ~/projects
    
    # CMA 프로젝트가 이미 존재하는지 확인
    if [ -d "CMA" ]; then
        log_warning "CMA 프로젝트가 이미 존재합니다."
        read -p "기존 프로젝트를 백업하고 새로 클론하시겠습니까? (y/N): " backup_choice
        
        if [[ $backup_choice =~ ^[Yy]$ ]]; then
            mv CMA CMA_backup_$(date +%Y%m%d_%H%M%S)
            log_info "기존 프로젝트를 백업했습니다."
        else
            log_info "기존 프로젝트를 사용합니다."
            return 0
        fi
    fi
    
    # Git 저장소 URL 입력
    read -p "CMA 프로젝트 Git 저장소 URL을 입력하세요: " repo_url
    
    if [ -n "$repo_url" ]; then
        git clone "$repo_url" CMA
        log_success "CMA 프로젝트 클론 완료"
    else
        log_warning "Git 저장소 URL이 입력되지 않았습니다. 나중에 수동으로 클론해주세요."
        mkdir -p CMA
    fi
}

# 가상환경 설정
setup_virtual_environments() {
    log_info "가상환경 설정 중..."
    
    # 백엔드 가상환경
    if [ -f ~/projects/CMA/backend/requirements.txt ]; then
        log_info "백엔드 가상환경 설정 중..."
        cd ~/projects/CMA/backend
        
        python3 -m venv ~/venvs/backend_venv
        source ~/venvs/backend_venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        deactivate
        
        log_success "백엔드 가상환경 설정 완료"
    else
        log_warning "backend/requirements.txt 파일을 찾을 수 없습니다."
    fi
    
    # 데스크탑 가상환경
    if [ -f ~/projects/CMA/desktop/requirements.txt ]; then
        log_info "데스크탑 가상환경 설정 중..."
        cd ~/projects/CMA/desktop
        
        python3 -m venv ~/venvs/desktop_venv
        source ~/venvs/desktop_venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        deactivate
        
        log_success "데스크탑 가상환경 설정 완료"
    else
        log_warning "desktop/requirements.txt 파일을 찾을 수 없습니다."
    fi
}

# 프론트엔드 설정
setup_frontend() {
    log_info "프론트엔드 설정 중..."
    
    if [ -f ~/projects/CMA/frontend/package.json ]; then
        cd ~/projects/CMA/frontend
        
        # npm 의존성 설치
        npm install
        
        log_success "프론트엔드 설정 완료"
    else
        log_warning "frontend/package.json 파일을 찾을 수 없습니다."
    fi
}

# 성능 최적화
optimize_performance() {
    log_info "성능 최적화 중..."
    
    # 불필요한 서비스 비활성화
    sudo systemctl disable snapd 2>/dev/null || true
    sudo systemctl disable snapd.socket 2>/dev/null || true
    
    # 스왑 파일 생성 (4GB)
    if [ ! -f /swapfile ]; then
        sudo fallocate -l 4G /swapfile
        sudo chmod 600 /swapfile
        sudo mkswap /swapfile
        sudo swapon /swapfile
        
        # 영구 설정
        if ! grep -q "/swapfile" /etc/fstab; then
            echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
        fi
        
        log_success "스왑 파일 생성 완료"
    else
        log_info "스왑 파일이 이미 존재합니다."
    fi
    
    # 로그 로테이션 설정
    sudo sed -i 's/#compress/compress/' /etc/logrotate.conf 2>/dev/null || true
    
    log_success "성능 최적화 완료"
}

# 환경 변수 설정
setup_environment_variables() {
    log_info "환경 변수 설정 중..."
    
    # .bashrc에 환경 변수 추가
    cat >> ~/.bashrc << 'EOF'

# CMA 프로젝트 환경 변수
export CMA_PROJECT_ROOT="$HOME/projects/CMA"
export CMA_VENV_ROOT="$HOME/venvs"
export CMA_DATA_ROOT="$HOME/data"
export CMA_LOG_ROOT="$HOME/logs"

# 별칭 설정
alias cma-backend="source $HOME/venvs/backend_venv/bin/activate && cd $HOME/projects/CMA/backend"
alias cma-desktop="source $HOME/venvs/desktop_venv/bin/activate && cd $HOME/projects/CMA/desktop"
alias cma-frontend="cd $HOME/projects/CMA/frontend"
alias cma-status="echo '=== CMA 프로젝트 상태 ===' && echo '백엔드: ' && ps aux | grep -E '(uvicorn|fastapi)' | grep -v grep && echo '프론트엔드: ' && ps aux | grep -E '(vite|npm)' | grep -v grep"

# Python 경로 설정
export PYTHONPATH="$CMA_PROJECT_ROOT/backend:$PYTHONPATH"
EOF
    
    # 환경 변수 적용
    source ~/.bashrc
    
    log_success "환경 변수 설정 완료"
}

# 테스트 실행
run_tests() {
    log_info "환경 테스트 실행 중..."
    
    # Python 테스트
    if command -v python3 &> /dev/null; then
        log_success "Python3 정상 작동"
    else
        log_error "Python3 테스트 실패"
    fi
    
    # Node.js 테스트
    if command -v node &> /dev/null; then
        log_success "Node.js 정상 작동"
    else
        log_error "Node.js 테스트 실패"
    fi
    
    # PostgreSQL 테스트
    if sudo systemctl is-active --quiet postgresql; then
        log_success "PostgreSQL 정상 작동"
    else
        log_error "PostgreSQL 테스트 실패"
    fi
    
    # Redis 테스트
    if sudo systemctl is-active --quiet redis-server; then
        log_success "Redis 정상 작동"
    else
        log_error "Redis 테스트 실패"
    fi
    
    # 가상환경 테스트
    if [ -d ~/venvs/backend_venv ]; then
        source ~/venvs/backend_venv/bin/activate
        python --version > /dev/null 2>&1 && log_success "백엔드 가상환경 정상 작동"
        deactivate
    fi
    
    if [ -d ~/venvs/desktop_venv ]; then
        source ~/venvs/desktop_venv/bin/activate
        python --version > /dev/null 2>&1 && log_success "데스크탑 가상환경 정상 작동"
        deactivate
    fi
}

# 완료 메시지
print_completion_message() {
    echo -e "${GREEN}"
    echo "=========================================="
    echo "  🎉 D 드라이브 WSL2 환경 설정 완료!"
    echo "=========================================="
    echo -e "${NC}"
    
    echo "다음 단계:"
    echo "1. VS Code/Cursor에서 WSL 확장 설치"
    echo "2. CMA 프로젝트 폴더 열기: cd ~/projects/CMA && code ."
    echo "3. Python 인터프리터 설정: ~/venvs/backend_venv/bin/python"
    echo ""
    echo "유용한 명령어:"
    echo "  cma-backend    # 백엔드 개발 환경"
    echo "  cma-desktop    # 데스크탑 개발 환경"
    echo "  cma-frontend   # 프론트엔드 개발 환경"
    echo "  cma-status     # 프로젝트 상태 확인"
    echo ""
    echo "문서 참조: docs/environment-setup/D-drive-wsl2-setup.md"
}

# 메인 함수
main() {
    print_title
    
    # 시스템 정보 확인
    check_system
    
    # 사용자 확인
    echo "이 스크립트는 D 드라이브 WSL2 환경을 설정합니다."
    read -p "계속하시겠습니까? (y/N): " confirm
    
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        log_info "설정을 취소했습니다."
        exit 0
    fi
    
    # 단계별 실행
    install_basic_tools
    setup_python
    install_nodejs
    install_postgresql
    install_redis
    setup_git
    create_project_structure
    setup_cma_project
    setup_virtual_environments
    setup_frontend
    optimize_performance
    setup_environment_variables
    run_tests
    
    print_completion_message
}

# 스크립트 실행
main "$@" 