# CMA 백엔드 시스템 구동 가이드

## 🚀 시스템 구동 방법

### 1. 환경 요구사항

#### 필수 소프트웨어
```bash
# Python 3.12+ 설치 확인
python --version  # Python 3.12.11 이상

# pip 설치 확인
pip --version

# Git 설치 확인
git --version
```

#### 권장 사양
- **CPU**: 4코어 이상
- **RAM**: 8GB 이상
- **Storage**: 10GB 이상 (데이터베이스 + 로그)
- **OS**: Ubuntu 20.04+, Windows 10+, macOS 10.15+

### 2. 프로젝트 설정

#### 2.1 프로젝트 클론
```bash
# 프로젝트 저장소 클론
git clone https://github.com/your-org/cma-backend.git
cd cma-backend

# 또는 기존 프로젝트 업데이트
git pull origin main
```

#### 2.2 가상환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Linux/macOS)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 확인
which python  # Linux/macOS
where python  # Windows
```

#### 2.3 의존성 설치
```bash
# 기본 의존성 설치
pip install -r requirements.txt

# 개발 의존성 설치 (선택사항)
pip install -r requirements-dev.txt

# 설치 확인
pip list | grep -E "(fastapi|uvicorn|sqlalchemy)"
```

### 3. 환경 설정

#### 3.1 환경 변수 설정
```bash
# 환경 변수 파일 복사
cp env.example .env

# 환경 변수 편집
nano .env
```

#### 3.2 주요 환경 변수
```env
# 애플리케이션 설정
APP_NAME=CMA-Backend
DEBUG=True
HOST=0.0.0.0
PORT=8000

# 데이터베이스 설정
DATABASE_URL=sqlite:///./cma_backend.db

# 보안 설정
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis 설정 (선택사항)
REDIS_URL=redis://localhost:6379

# 파일 업로드 설정
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB
```

### 4. 데이터베이스 초기화

#### 4.1 데이터베이스 테이블 생성
```bash
# 데이터베이스 초기화
python -c "from app.db.database import init_db; init_db()"

# 성공 메시지 확인
# ✅ 데이터베이스 테이블과 인덱스가 생성되었습니다.
```

#### 4.2 초기 데이터 설정 (선택사항)
```bash
# 샘플 데이터 생성
python scripts/create_sample_data.py

# 또는 수동으로 데이터베이스 확인
python -c "from app.db.database import engine; print('DB 연결 성공')"
```

### 5. 서버 구동

#### 5.1 개발 서버 구동
```bash
# 방법 1: uvicorn 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 방법 2: Python 모듈로 실행
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 방법 3: main.py 직접 실행
python app/main.py
```

#### 5.2 서버 상태 확인
```bash
# 헬스 체크
curl http://localhost:8000/health

# 루트 엔드포인트
curl http://localhost:8000/

# API 문서
# 브라우저에서 http://localhost:8000/docs 접속
```

### 6. 프로덕션 구동

#### 6.1 Gunicorn + Uvicorn (권장)
```bash
# Gunicorn 설치
pip install gunicorn

# 프로덕션 서버 구동
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 6.2 Docker 구동
```bash
# Docker 이미지 빌드
docker build -t cma-backend .

# Docker 컨테이너 실행
docker run -p 8000:8000 cma-backend

# Docker Compose 사용
docker-compose up -d
```

### 7. 모니터링 및 로깅

#### 7.1 로그 확인
```bash
# 애플리케이션 로그
tail -f logs/cma.log

# 서버 로그 (uvicorn)
# 터미널에서 직접 확인

# 시스템 로그
journalctl -u cma-backend -f
```

#### 7.2 성능 모니터링
```bash
# 성능 정보 확인
curl http://localhost:8000/performance

# 캐시 상태 확인
curl http://localhost:8000/cache/status

# 메모리 사용량 확인
ps aux | grep python
```

### 8. 문제 해결

#### 8.1 일반적인 문제들

**포트 충돌**
```bash
# 포트 사용 확인
netstat -tulpn | grep :8000
lsof -i :8000

# 다른 포트로 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**데이터베이스 연결 오류**
```bash
# 데이터베이스 파일 확인
ls -la *.db

# 데이터베이스 재초기화
rm cma_backend.db
python -c "from app.db.database import init_db; init_db()"
```

**의존성 오류**
```bash
# 가상환경 재생성
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 8.2 디버깅 모드
```bash
# 디버그 모드로 실행
DEBUG=True uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 로그 레벨 설정
LOG_LEVEL=DEBUG uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 9. API 테스트

#### 9.1 기본 API 테스트
```bash
# 헬스 체크
curl -X GET http://localhost:8000/health

# 계약 목록 조회
curl -X GET http://localhost:8000/api/v1/contracts/

# 노무 목록 조회
curl -X GET http://localhost:8000/api/v1/labor/

# 재무 정보 조회
curl -X GET http://localhost:8000/api/v1/financial/
```

#### 9.2 API 문서 확인
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### 10. 성능 최적화

#### 10.1 서버 설정 최적화
```bash
# 워커 수 조정
gunicorn app.main:app -w 8 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 타임아웃 설정
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 120
```

#### 10.2 데이터베이스 최적화
```bash
# 데이터베이스 인덱스 확인
python -c "from app.db.database import engine; print('인덱스 생성 완료')"

# 쿼리 성능 분석
python scripts/analyze_queries.py
```

### 11. 보안 설정

#### 11.1 HTTPS 설정
```bash
# SSL 인증서 설정
uvicorn app.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem --host 0.0.0.0 --port 443
```

#### 11.2 방화벽 설정
```bash
# UFW 방화벽 설정 (Ubuntu)
sudo ufw allow 8000
sudo ufw enable
```

### 12. 백업 및 복구

#### 12.1 데이터베이스 백업
```bash
# SQLite 백업
cp cma_backend.db backup/cma_backend_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL 백업
pg_dump cma_db > backup/cma_db_$(date +%Y%m%d_%H%M%S).sql
```

#### 12.2 로그 백업
```bash
# 로그 파일 백업
tar -czf backup/logs_$(date +%Y%m%d_%H%M%S).tar.gz logs/
```

이 가이드를 따라하면 CMA 백엔드 시스템을 안정적으로 구동할 수 있습니다. 