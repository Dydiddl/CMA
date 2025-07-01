# 🐳 CMA Docker 가이드

## 📋 목차
1. [개요](#개요)
2. [설치 및 설정](#설치-및-설정)
3. [개발 환경](#개발-환경)
4. [프로덕션 환경](#프로덕션-환경)
5. [모니터링](#모니터링)
6. [배포](#배포)
7. [문제 해결](#문제-해결)

---

## 🎯 개요

CMA 프로젝트는 Docker를 사용하여 **일관된 개발 및 배포 환경**을 제공합니다.

### 🏗️ 아키텍처
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Redis Cache   │
                       │   Port: 6379    │
                       └─────────────────┘
```

---

## 🚀 설치 및 설정

### 1. Docker 설치
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# macOS
brew install docker docker-compose

# Windows
# Docker Desktop 설치: https://docs.docker.com/desktop/install/windows/
```

### 2. 자동 설정 스크립트 실행
```bash
# 개발 환경 설정 (권장)
./scripts/docker-setup.sh dev

# 프로덕션 환경 설정
./scripts/docker-setup.sh prod

# 모니터링 환경 설정
./scripts/docker-setup.sh monitoring
```

### 3. 수동 설정
```bash
# 환경 변수 파일 생성
cp backend/.env.example backend/.env

# Docker 이미지 빌드
docker build -f backend/Dockerfile -t cma-backend:latest ./backend

# 개발용 이미지 빌드
docker build -f backend/Dockerfile.dev -t cma-backend:dev ./backend
```

---

## 🔧 개발 환경

### 시작하기
```bash
# 개발 환경 시작
docker-compose -f docker-compose.dev.yml up -d

# 로그 확인
docker-compose -f docker-compose.dev.yml logs -f

# 특정 서비스 로그 확인
docker-compose -f docker-compose.dev.yml logs -f backend_dev
```

### 접속 정보
- **Backend API**: http://localhost:8001
- **Frontend**: http://localhost:3001
- **PgAdmin**: http://localhost:5050 (admin@cma.com / admin)
- **Redis Commander**: http://localhost:8081

### 개발 워크플로우
```bash
# 1. 코드 변경
# 2. 자동 리로드 (개발 모드에서)
# 3. 테스트 실행
docker-compose -f docker-compose.dev.yml exec backend_dev pytest

# 4. 데이터베이스 마이그레이션
docker-compose -f docker-compose.dev.yml exec backend_dev alembic upgrade head
```

---

## 🏭 프로덕션 환경

### 시작하기
```bash
# 프로덕션 환경 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 상태 확인
docker-compose ps
```

### 접속 정보
- **Backend API**: http://localhost:8000
- **Nginx**: http://localhost:80

### 환경 변수 설정
```bash
# 프로덕션용 환경 변수
export SECRET_KEY="your-production-secret-key"
export POSTGRES_PASSWORD="your-production-password"
export REDIS_URL="redis://your-redis-server:6379"
```

---

## 📊 모니터링

### 모니터링 환경 시작
```bash
# 모니터링 서비스 시작
docker-compose --profile monitoring up -d

# 접속 정보
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin / admin)
```

### Grafana 대시보드 설정
1. Grafana에 로그인
2. Prometheus 데이터 소스 추가
3. CMA 대시보드 임포트

### 메트릭 수집
- **시스템 메트릭**: CPU, 메모리, 디스크 사용량
- **애플리케이션 메트릭**: API 응답 시간, 오류율
- **데이터베이스 메트릭**: 쿼리 성능, 연결 수

---

## 🚀 배포

### 클라우드 배포 (AWS 예시)
```bash
# 1. ECR에 이미지 푸시
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
docker tag cma-backend:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/cma-backend:latest
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/cma-backend:latest

# 2. ECS 서비스 업데이트
aws ecs update-service --cluster cma-cluster --service cma-service --force-new-deployment
```

### 로컬 배포
```bash
# 프로덕션 빌드
docker-compose -f docker-compose.yml build

# 프로덕션 실행
docker-compose -f docker-compose.yml up -d

# 헬스 체크
curl http://localhost:8000/health
```

---

## 🔍 문제 해결

### 일반적인 문제들

#### 1. 포트 충돌
```bash
# 사용 중인 포트 확인
netstat -tulpn | grep :8000

# 다른 포트 사용
docker-compose -f docker-compose.dev.yml up -d -p 8002:8000
```

#### 2. 데이터베이스 연결 실패
```bash
# 데이터베이스 상태 확인
docker-compose -f docker-compose.dev.yml exec postgres_dev pg_isready -U postgres

# 로그 확인
docker-compose -f docker-compose.dev.yml logs postgres_dev
```

#### 3. 메모리 부족
```bash
# Docker 리소스 정리
docker system prune -a

# 컨테이너 재시작
docker-compose -f docker-compose.dev.yml restart
```

#### 4. 권한 문제
```bash
# Docker 그룹에 사용자 추가
sudo usermod -aG docker $USER

# 권한 재설정
sudo chown -R $USER:$USER .
```

### 디버깅 명령어
```bash
# 컨테이너 내부 접속
docker-compose -f docker-compose.dev.yml exec backend_dev bash

# 환경 변수 확인
docker-compose -f docker-compose.dev.yml exec backend_dev env

# 네트워크 확인
docker network ls
docker network inspect cma_dev_network
```

---

## 📚 추가 리소스

### 유용한 명령어
```bash
# 모든 컨테이너 정리
./scripts/docker-setup.sh clean

# 이미지만 빌드
./scripts/docker-setup.sh build

# 특정 서비스 재시작
docker-compose -f docker-compose.dev.yml restart backend_dev

# 볼륨 백업
docker run --rm -v cma_postgres_dev_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

### 성능 최적화
```bash
# 멀티 스테이지 빌드 사용
docker build --target production -t cma-backend:prod .

# 이미지 크기 최적화
docker build --no-cache -t cma-backend:optimized .

# 레이어 캐싱 활용
# Dockerfile에서 자주 변경되지 않는 레이어를 먼저 배치
```

### 보안 고려사항
1. **환경 변수**: 민감한 정보는 환경 변수로 관리
2. **네트워크**: 필요한 포트만 노출
3. **권한**: 최소 권한 원칙 적용
4. **업데이트**: 정기적인 보안 업데이트

---

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. [Docker 공식 문서](https://docs.docker.com/)
2. [Docker Compose 문서](https://docs.docker.com/compose/)
3. 프로젝트 이슈 트래커
4. 개발팀 문의 