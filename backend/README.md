# CMA Backend

*최종 업데이트: 2025-01-23*

CMA (Construction Management System) 백엔드 서버입니다.

## 🏗️ 아키텍처

### 기술 스택
- **Python**: 3.12+
- **FastAPI**: 0.115.12 (비동기 웹 프레임워크)
- **SQLAlchemy**: 2.0.41 (ORM)
- **Alembic**: 1.16.1 (데이터베이스 마이그레이션)
- **Pydantic**: 2.11.7 (데이터 검증)
- **Uvicorn**: 0.34.3 (ASGI 서버)
- **PostgreSQL**: 14+ (데이터베이스)

### 프로젝트 구조
```
backend/
├── app/
│   ├── api/                    # API 라우터
│   │   ├── v1/                # API v1
│   │   │   ├── api.py         # 메인 API 라우터
│   │   │   └── endpoints/     # 엔드포인트
│   │   │       ├── projects.py
│   │   │       └── tasks.py
│   │   └── common/            # 공통 API 기능
│   ├── core/                  # 핵심 설정
│   │   ├── config.py          # 애플리케이션 설정
│   │   ├── auth.py            # 인증
│   │   └── database.py        # 데이터베이스 연결
│   ├── models/                # SQLAlchemy 모델
│   │   ├── base.py            # 기본 모델
│   │   └── models.py          # 모든 모델
│   ├── schemas/               # Pydantic 스키마
│   │   └── schemas.py         # 모든 스키마
│   ├── services/              # 비즈니스 로직
│   │   └── ascr/              # ASCR 모듈
│   ├── crud.py                # CRUD 작업
│   └── main.py                # 애플리케이션 진입점
├── alembic/                   # 데이터베이스 마이그레이션
├── tests/                     # 테스트
├── requirements.txt           # 의존성
└── README.md                  # 이 파일
```

## 🚀 시작하기

### 1. 환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 설정
```bash
# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 데이터베이스 설정

# 데이터베이스 마이그레이션
alembic upgrade head
```

### 3. 서버 실행
```bash
# 개발 서버 실행
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 또는
python app/main.py
```

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 개발

### 코드 스타일
- **PEP8** 준수
- **Black** 포맷터 사용
- **isort** 임포트 정렬
- **flake8** 린터 사용

### 테스트 실행
```bash
# 모든 테스트 실행
pytest

# 특정 테스트 실행
pytest tests/test_api.py

# 커버리지와 함께 실행
pytest --cov=app
```

### 데이터베이스 마이그레이션
```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "설명"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 되돌리기
alembic downgrade -1
```

## 🏗️ 주요 기능

### 1. 프로젝트 관리
- 프로젝트 생성, 조회, 수정, 삭제
- 프로젝트별 작업 관리
- 프로젝트 상태 추적

### 2. 작업 관리
- 작업 생성 및 할당
- 작업 진행 상황 추적
- 작업 완료율 계산

### 3. ASCR 모듈
- PDF 문서 처리
- 목차 자동 추출
- 문서 구조 분석

## 🔒 보안

- JWT 기반 인증
- CORS 설정
- 입력 데이터 검증
- SQL 인젝션 방지

## 📊 성능 최적화

- 비동기 처리
- 데이터베이스 연결 풀링
- 캐싱 전략
- 쿼리 최적화

## 🐛 문제 해결

### 일반적인 문제
1. **데이터베이스 연결 실패**: `.env` 파일의 데이터베이스 설정 확인
2. **포트 충돌**: 다른 프로세스가 8000번 포트를 사용 중인지 확인
3. **의존성 오류**: `pip install -r requirements.txt` 재실행

### 로그 확인
```bash
# 애플리케이션 로그
tail -f logs/cma.log

# 서버 로그
uvicorn app.main:app --log-level debug
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 