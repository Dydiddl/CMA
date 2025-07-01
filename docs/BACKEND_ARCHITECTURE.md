# 🏗️ CMA 백엔드 시스템 아키텍처

## 📋 시스템 개요

CMA 백엔드는 **FastAPI 기반의 비동기 웹 API 서버**로, 건설 공사 내역서 자동화를 위한 핵심 비즈니스 로직을 제공합니다.

### 🎯 주요 특징
- **비동기 처리**: asyncio 기반 고성능 API
- **모듈화 설계**: 기능별 명확한 분리
- **확장 가능**: 마이크로서비스 아키텍처 준비
- **성능 최적화**: 캐싱, 멀티프로세싱 지원
- **보안**: JWT 인증, 권한 관리

## 🏗️ 시스템 아키텍처

### 전체 구조
```
┌─────────────────────────────────────────────────────────────┐
│                    CMA Backend System                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Frontend  │  │   Mobile    │  │   Desktop   │         │
│  │   (React)   │  │   (Tauri)   │  │   (Tauri)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    API Gateway Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   CORS      │  │   Auth      │  │   Logging   │         │
│  │ Middleware  │  │ Middleware  │  │ Middleware  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    API Layer (v1)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Contracts  │  │  Financial  │  │    Labor    │         │
│  │     API     │  │     API     │  │     API     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    ASCR     │  │   Vendors   │  │   Workers   │         │
│  │     API     │  │     API     │  │     API     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                   Service Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Contract   │  │  Financial  │  │   Labor     │         │
│  │  Service    │  │  Service    │  │  Service    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    ASCR     │  │   Excel     │  │ Performance │         │
│  │  Service    │  │  Service    │  │ Optimizer   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                   Data Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  SQLAlchemy │  │   Redis     │  │   File      │         │
│  │     ORM     │  │   Cache     │  │  Storage    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                   Infrastructure                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ PostgreSQL  │  │    Redis    │  │   Docker    │         │
│  │  Database   │  │   Cache     │  │  Container  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 시스템 동작 원리

### 1. 요청 처리 흐름

```mermaid
sequenceDiagram
    participant Client as 클라이언트
    participant Gateway as API Gateway
    participant Middleware as 미들웨어
    participant API as API Layer
    participant Service as Service Layer
    participant DB as Database
    participant Cache as Cache

    Client->>Gateway: HTTP 요청
    Gateway->>Middleware: CORS, Auth, Logging
    Middleware->>API: 인증된 요청
    API->>Service: 비즈니스 로직 호출
    Service->>Cache: 캐시 확인
    alt 캐시 히트
        Cache-->>Service: 캐시된 데이터
    else 캐시 미스
        Service->>DB: 데이터베이스 조회
        DB-->>Service: 데이터
        Service->>Cache: 캐시 저장
    end
    Service-->>API: 처리 결과
    API-->>Middleware: 응답
    Middleware-->>Gateway: 로깅
    Gateway-->>Client: HTTP 응답
```

### 2. 비동기 처리 원리

```python
# 비동기 요청 처리 예시
async def process_contract_request(contract_data: ContractCreate):
    """계약 생성 비동기 처리"""
    
    # 1. 캐시 확인 (비동기)
    cached = await cache_manager.get_cache(f"contract:{contract_data.id}")
    if cached:
        return cached
    
    # 2. 데이터베이스 처리 (비동기)
    contract = await contract_service.create_contract(contract_data)
    
    # 3. 캐시 저장 (비동기)
    await cache_manager.set_cache(f"contract:{contract.id}", contract)
    
    # 4. 병렬 처리 (여러 작업 동시 실행)
    tasks = [
        send_notification(contract),
        update_statistics(contract),
        log_activity(contract)
    ]
    await asyncio.gather(*tasks)
    
    return contract
```

## 📁 디렉토리 구조 및 역할

### 핵심 디렉토리
```
backend/
├── app/                          # 메인 애플리케이션
│   ├── main.py                   # FastAPI 앱 진입점
│   ├── api/                      # API 라우터
│   │   └── v1/                   # API 버전 1
│   │       ├── api.py            # 메인 API 라우터
│   │       └── endpoints/        # 엔드포인트별 라우터
│   ├── models/                   # SQLAlchemy ORM 모델
│   ├── schemas/                  # Pydantic 스키마
│   ├── services/                 # 비즈니스 로직
│   ├── core/                     # 설정 및 핵심 기능
│   ├── middleware/               # 미들웨어
│   ├── db/                       # 데이터베이스 설정
│   └── utils/                    # 유틸리티 함수
├── tests/                        # 테스트 코드
├── migrations/                   # 데이터베이스 마이그레이션
└── requirements.txt              # Python 의존성
```

### 각 레이어별 역할

#### 1. API Layer (api/v1/endpoints/)
- **역할**: HTTP 요청/응답 처리
- **책임**: 입력 검증, 응답 포맷팅, 에러 처리
- **예시**: `contracts.py`, `financial.py`, `labor.py`

#### 2. Service Layer (services/)
- **역할**: 비즈니스 로직 처리
- **책임**: 데이터 처리, 비즈니스 규칙, 외부 서비스 연동
- **예시**: `ContractService`, `FinancialService`, `ASCRService`

#### 3. Data Layer (models/, db/)
- **역할**: 데이터 접근 및 저장
- **책임**: 데이터베이스 CRUD, 캐싱, 파일 처리
- **예시**: `Contract`, `Financial`, `Labor` 모델

## ⚙️ 시스템 설정 및 환경

### 환경 변수
```env
# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost/cma_db

# Redis 캐시
REDIS_URL=redis://localhost:6379

# 보안
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 성능 설정
MAX_WORKERS=4
CACHE_TTL=3600
API_TIMEOUT=30

# CORS 설정
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:1420"]
```

### 성능 최적화 설정
```python
# 성능 최적화 설정
PERFORMANCE_CONFIG = {
    "max_workers": cpu_count(),
    "cache_ttl": 3600,
    "api_timeout": 30,
    "batch_size": 100,
    "connection_pool_size": 20
}
```

## 🔒 보안 아키텍처

### 인증 및 권한 관리
```python
# JWT 토큰 기반 인증
class AuthMiddleware:
    """인증 미들웨어"""
    
    async def __call__(self, request: Request, call_next):
        # 1. 토큰 추출
        token = extract_token(request)
        
        # 2. 토큰 검증
        if token:
            user = verify_token(token)
            request.state.user = user
        
        # 3. 권한 확인
        if requires_auth(request.url.path):
            if not user:
                raise AuthenticationError("인증 필요")
        
        return await call_next(request)
```

### 데이터 보안
- **암호화**: 민감한 데이터 암호화 저장
- **입력 검증**: Pydantic 스키마로 모든 입력 검증
- **SQL 인젝션 방지**: SQLAlchemy ORM 사용
- **XSS 방지**: 입력 데이터 이스케이프 처리

## 📊 성능 모니터링

### 성능 지표
```python
PERFORMANCE_METRICS = {
    "api_response_time": "500ms 이내",
    "database_query_time": "100ms 이내",
    "cache_hit_rate": "80% 이상",
    "memory_usage": "512MB 이내",
    "concurrent_users": "100명 이상"
}
```

### 모니터링 도구
- **성능 측정**: 커스텀 데코레이터
- **메모리 모니터링**: psutil 기반
- **캐시 통계**: Redis 통계 수집
- **에러 추적**: 구조화된 로깅

## 🚀 배포 및 운영

### 개발 환경
```bash
# 개발 서버 실행
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프로덕션 환경
```bash
# Docker 컨테이너 실행
docker-compose up -d

# 또는 직접 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 헬스 체크
```python
@app.get("/health")
async def health_check():
    """시스템 상태 확인"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "database": "connected",
        "cache": "connected"
    }
```

## 🔄 데이터베이스 마이그레이션

### 마이그레이션 관리
```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Add new table"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

### 스키마 버전 관리
- **Alembic**: 데이터베이스 스키마 버전 관리
- **자동 마이그레이션**: 모델 변경 시 자동 감지
- **롤백 지원**: 이전 버전으로 되돌리기 가능

## 📈 확장성 고려사항

### 수평 확장
- **로드 밸런싱**: 여러 인스턴스 배포
- **세션 공유**: Redis를 통한 세션 공유
- **데이터베이스 샤딩**: 대용량 데이터 처리

### 수직 확장
- **리소스 증가**: CPU, 메모리 증설
- **성능 최적화**: 쿼리 최적화, 인덱스 추가
- **캐싱 강화**: 다층 캐싱 전략

이 아키텍처를 통해 **확장 가능하고 유지보수하기 쉬운** 백엔드 시스템을 구축할 수 있습니다. 