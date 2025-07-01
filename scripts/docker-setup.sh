#!/bin/bash

# CMA Docker Setup Script
# 이 스크립트는 CMA 프로젝트의 Docker 환경을 설정합니다.

set -e

echo "🚀 CMA Docker 환경 설정을 시작합니다..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Docker 설치 확인
check_docker() {
    print_info "Docker 설치 상태를 확인합니다..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker가 설치되지 않았습니다."
        echo "Docker 설치 방법: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose가 설치되지 않았습니다."
        echo "Docker Compose 설치 방법: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker 및 Docker Compose가 설치되어 있습니다."
}

# 환경 변수 파일 생성
create_env_file() {
    print_info "환경 변수 파일을 생성합니다..."
    
    if [ ! -f "backend/.env" ]; then
        cat > backend/.env << EOF
# CMA Backend Environment Variables
PROJECT_NAME="Construction Management API"
API_V1_STR="/api/v1"

# Database Configuration
POSTGRES_SERVER=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=construction_management
USE_LOCAL_DB=false

# Redis Configuration
REDIS_URL=redis://redis:6379

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Performance Configuration
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
SLOW_QUERY_THRESHOLD=0.5

# Sharding Configuration
ENABLE_SHARDING=true
SHARD_1_DB=construction_management_shard1
SHARD_2_DB=construction_management_shard2

# File Upload Configuration
MAX_EXCEL_FILE_SIZE=10485760
ALLOWED_EXCEL_EXTENSIONS=.xlsx,.xls
EXCEL_TEMP_DIR=temp/excel

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","tauri://localhost"]
EOF
        print_success "backend/.env 파일이 생성되었습니다."
    else
        print_warning "backend/.env 파일이 이미 존재합니다."
    fi
}

# Docker 이미지 빌드
build_images() {
    print_info "Docker 이미지를 빌드합니다..."
    
    # 백엔드 이미지 빌드
    print_info "백엔드 이미지를 빌드합니다..."
    docker build -f backend/Dockerfile -t cma-backend:latest ./backend
    
    # 개발용 백엔드 이미지 빌드
    print_info "개발용 백엔드 이미지를 빌드합니다..."
    docker build -f backend/Dockerfile.dev -t cma-backend:dev ./backend
    
    print_success "모든 Docker 이미지가 빌드되었습니다."
}

# 개발 환경 실행
start_dev_environment() {
    print_info "개발 환경을 시작합니다..."
    
    # 기존 컨테이너 정리
    docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
    
    # 개발 환경 시작
    docker-compose -f docker-compose.dev.yml up -d
    
    print_success "개발 환경이 시작되었습니다."
    echo ""
    echo "📋 접속 정보:"
    echo "  - Backend API: http://localhost:8001"
    echo "  - Frontend: http://localhost:3001"
    echo "  - PgAdmin: http://localhost:5050 (admin@cma.com / admin)"
    echo "  - Redis Commander: http://localhost:8081"
    echo ""
    echo "🔍 로그 확인:"
    echo "  - docker-compose -f docker-compose.dev.yml logs -f"
}

# 프로덕션 환경 실행
start_prod_environment() {
    print_info "프로덕션 환경을 시작합니다..."
    
    # 기존 컨테이너 정리
    docker-compose down --volumes --remove-orphans
    
    # 프로덕션 환경 시작
    docker-compose up -d
    
    print_success "프로덕션 환경이 시작되었습니다."
    echo ""
    echo "📋 접속 정보:"
    echo "  - Backend API: http://localhost:8000"
    echo "  - Nginx: http://localhost:80"
    echo ""
    echo "🔍 로그 확인:"
    echo "  - docker-compose logs -f"
}

# 모니터링 환경 실행
start_monitoring() {
    print_info "모니터링 환경을 시작합니다..."
    
    docker-compose --profile monitoring up -d
    
    print_success "모니터링 환경이 시작되었습니다."
    echo ""
    echo "📋 접속 정보:"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3001 (admin / admin)"
}

# 메인 함수
main() {
    case "${1:-dev}" in
        "dev")
            check_docker
            create_env_file
            build_images
            start_dev_environment
            ;;
        "prod")
            check_docker
            create_env_file
            build_images
            start_prod_environment
            ;;
        "monitoring")
            check_docker
            start_monitoring
            ;;
        "build")
            check_docker
            build_images
            ;;
        "clean")
            print_info "모든 Docker 리소스를 정리합니다..."
            docker-compose -f docker-compose.yml down --volumes --remove-orphans
            docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
            docker system prune -f
            print_success "정리가 완료되었습니다."
            ;;
        *)
            echo "사용법: $0 [dev|prod|monitoring|build|clean]"
            echo ""
            echo "옵션:"
            echo "  dev        - 개발 환경 시작 (기본값)"
            echo "  prod       - 프로덕션 환경 시작"
            echo "  monitoring - 모니터링 환경 시작"
            echo "  build      - 이미지만 빌드"
            echo "  clean      - 모든 Docker 리소스 정리"
            exit 1
            ;;
    esac
}

# 스크립트 실행
main "$@" 