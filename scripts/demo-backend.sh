#!/bin/bash

# CMA 백엔드 시스템 데모 스크립트
# 실제 사용자에게 시스템을 보여주기 위한 스크립트

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

# 헤더 출력
print_header() {
    echo "=================================================="
    echo "           CMA 백엔드 시스템 데모"
    echo "=================================================="
    echo ""
}

# 환경 확인
check_environment() {
    log_info "환경 확인 중..."
    
    # Python 버전 확인
    if command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1)
        log_success "Python: $PYTHON_VERSION"
    else
        log_error "Python이 설치되지 않았습니다."
        exit 1
    fi
    
    # pip 확인
    if command -v pip &> /dev/null; then
        log_success "pip: $(pip --version)"
    else
        log_error "pip이 설치되지 않았습니다."
        exit 1
    fi
    
    # 현재 디렉토리 확인
    log_info "현재 디렉토리: $(pwd)"
    
    # 가상환경 확인
    if [ -d "venv" ]; then
        log_success "가상환경 디렉토리 발견"
    else
        log_warning "가상환경이 없습니다. 생성합니다..."
        python -m venv venv
    fi
}

# 가상환경 활성화
activate_venv() {
    log_info "가상환경 활성화 중..."
    source venv/bin/activate
    log_success "가상환경 활성화 완료: $(which python)"
}

# 의존성 확인
check_dependencies() {
    log_info "의존성 확인 중..."
    
    # 주요 패키지 버전 확인
    log_info "주요 패키지 버전:"
    pip show fastapi uvicorn sqlalchemy pydantic 2>/dev/null || {
        log_warning "일부 패키지가 설치되지 않았습니다."
        log_info "requirements.txt에서 설치 중..."
        pip install -r requirements.txt
    }
}

# 데이터베이스 초기화
init_database() {
    log_info "데이터베이스 초기화 중..."
    
    # 기존 DB 파일 삭제 (깨끗한 상태로 시작)
    if [ -f "cma_backend.db" ]; then
        rm cma_backend.db
        log_info "기존 데이터베이스 파일 삭제"
    fi
    
    # 데이터베이스 초기화
    python -c "from app.db.database import init_db; init_db()" && {
        log_success "데이터베이스 초기화 완료"
    } || {
        log_error "데이터베이스 초기화 실패"
        exit 1
    }
}

# 서버 구동
start_server() {
    log_info "백엔드 서버 구동 중..."
    
    # 서버 백그라운드 실행
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > server.log 2>&1 &
    SERVER_PID=$!
    
    # 서버 시작 대기
    log_info "서버 시작 대기 중..."
    sleep 5
    
    # 서버 상태 확인
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        log_success "서버가 성공적으로 시작되었습니다. (PID: $SERVER_PID)"
    else
        log_error "서버 시작 실패"
        cat server.log
        exit 1
    fi
}

# API 테스트
test_apis() {
    log_info "API 테스트 시작..."
    
    # 헬스 체크
    log_info "1. 헬스 체크"
    curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health
    
    # 루트 엔드포인트
    log_info "2. 루트 엔드포인트"
    curl -s http://localhost:8000/ | jq . 2>/dev/null || curl -s http://localhost:8000/
    
    # 성능 정보
    log_info "3. 성능 정보"
    curl -s http://localhost:8000/performance | jq . 2>/dev/null || curl -s http://localhost:8000/performance
    
    # 캐시 상태
    log_info "4. 캐시 상태"
    curl -s http://localhost:8000/cache/status | jq . 2>/dev/null || curl -s http://localhost:8000/cache/status
    
    # 테스트용 계약 데이터
    log_info "5. 테스트용 계약 데이터"
    curl -s http://localhost:8000/test/contracts | jq . 2>/dev/null || curl -s http://localhost:8000/test/contracts
    
    # 테스트용 노무 데이터
    log_info "6. 테스트용 노무 데이터"
    curl -s http://localhost:8000/test/labor | jq . 2>/dev/null || curl -s http://localhost:8000/test/labor
    
    # 테스트용 재무 데이터
    log_info "7. 테스트용 재무 데이터"
    curl -s http://localhost:8000/test/financial | jq . 2>/dev/null || curl -s http://localhost:8000/test/financial
    
    # 실제 API 엔드포인트
    log_info "8. 실제 API 엔드포인트 테스트"
    log_info "   - 계약 목록: http://localhost:8000/api/v1/contracts/"
    curl -s http://localhost:8000/api/v1/contracts/ | jq . 2>/dev/null || curl -s http://localhost:8000/api/v1/contracts/
    
    log_info "   - 노무 목록: http://localhost:8000/api/v1/labor/"
    curl -s http://localhost:8000/api/v1/labor/ | jq . 2>/dev/null || curl -s http://localhost:8000/api/v1/labor/
}

# API 문서 안내
show_api_docs() {
    log_info "API 문서 접속 안내:"
    echo "   Swagger UI: http://localhost:8000/docs"
    echo "   ReDoc: http://localhost:8000/redoc"
    echo "   OpenAPI JSON: http://localhost:8000/openapi.json"
    echo ""
}

# 성능 테스트
performance_test() {
    log_info "성능 테스트 시작..."
    
    # 응답 시간 측정
    log_info "API 응답 시간 측정:"
    
    # 헬스 체크 응답 시간
    START_TIME=$(date +%s%N)
    curl -s http://localhost:8000/health > /dev/null
    END_TIME=$(date +%s%N)
    RESPONSE_TIME=$(( (END_TIME - START_TIME) / 1000000 ))
    log_info "   헬스 체크: ${RESPONSE_TIME}ms"
    
    # 계약 목록 응답 시간
    START_TIME=$(date +%s%N)
    curl -s http://localhost:8000/api/v1/contracts/ > /dev/null
    END_TIME=$(date +%s%N)
    RESPONSE_TIME=$(( (END_TIME - START_TIME) / 1000000 ))
    log_info "   계약 목록: ${RESPONSE_TIME}ms"
    
    # 시스템 리소스 확인
    log_info "시스템 리소스 사용량:"
    ps aux | grep uvicorn | grep -v grep || log_warning "서버 프로세스를 찾을 수 없습니다."
}

# 오류 처리 테스트
error_handling_test() {
    log_info "오류 처리 테스트..."
    
    # 존재하지 않는 리소스 조회
    log_info "1. 존재하지 않는 계약 조회"
    curl -s http://localhost:8000/api/v1/contracts/non-existent-id | jq . 2>/dev/null || curl -s http://localhost:8000/api/v1/contracts/non-existent-id
    
    # 잘못된 요청
    log_info "2. 잘못된 JSON 데이터로 요청"
    curl -s -X POST http://localhost:8000/api/v1/contracts/ \
        -H "Content-Type: application/json" \
        -d '{"invalid": "data"}' | jq . 2>/dev/null || curl -s -X POST http://localhost:8000/api/v1/contracts/ \
        -H "Content-Type: application/json" \
        -d '{"invalid": "data"}'
}

# 서버 종료
cleanup() {
    log_info "서버 종료 중..."
    
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null || log_warning "서버 프로세스를 찾을 수 없습니다."
        log_success "서버가 종료되었습니다."
    fi
    
    # 가상환경 비활성화
    deactivate 2>/dev/null || log_warning "가상환경이 이미 비활성화되었습니다."
    
    # 임시 파일 정리
    rm -f server.log
    
    log_success "정리 완료"
}

# 메인 함수
main() {
    print_header
    
    # 트랩 설정 (Ctrl+C 시 정리)
    trap cleanup EXIT INT TERM
    
    # 단계별 실행
    check_environment
    activate_venv
    check_dependencies
    init_database
    start_server
    
    echo ""
    log_success "=== 백엔드 시스템이 성공적으로 구동되었습니다! ==="
    echo ""
    
    # API 테스트
    test_apis
    
    echo ""
    show_api_docs
    
    # 성능 테스트
    performance_test
    
    echo ""
    # 오류 처리 테스트
    error_handling_test
    
    echo ""
    log_info "데모가 완료되었습니다."
    log_info "서버는 계속 실행 중입니다. 종료하려면 Ctrl+C를 누르세요."
    log_info "API 문서를 확인하려면 브라우저에서 http://localhost:8000/docs 에 접속하세요."
    
    # 서버 로그 모니터링
    log_info "서버 로그 모니터링 중... (종료하려면 Ctrl+C)"
    tail -f server.log
}

# 스크립트 실행
main "$@" 