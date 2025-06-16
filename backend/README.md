# Construction Management API

## 프로젝트 구조
```
CMA/                      # 프로젝트 루트
├── backend/             # 백엔드 프로젝트 루트
│   ├── app/            # 애플리케이션 코드
│   │   ├── api/        # API 엔드포인트
│   │   ├── core/       # 핵심 설정
│   │   ├── db/         # 데이터베이스
│   │   ├── middleware/ # 미들웨어
│   │   ├── models/     # 데이터베이스 모델
│   │   ├── schemas/    # Pydantic 모델
│   │   ├── services/   # 비즈니스 로직
│   │   ├── tests/      # 테스트
│   │   └── utils/      # 유틸리티
│   ├── .env           # 환경 변수 파일 (여기에 생성)
│   ├── requirements.txt
│   └── README.md
├── frontend/           # 프론트엔드 프로젝트
└── docs/              # 프로젝트 문서
```

## 환경 설정

### 필수 환경 변수

`backend` 디렉토리에 `.env` 파일을 생성하고 다음 환경 변수들을 설정하세요:

```env
# 프로젝트 설정
PROJECT_NAME="Construction Management API"
API_V1_STR="/api/v1"

# CORS 설정
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","tauri://localhost"]

# 데이터베이스 설정(실제 설정한 내용과 일치해야 한다.)
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=construction_management

# JWT 설정
SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 days

# 로깅 설정
LOG_LEVEL=INFO
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## 설치 및 실행

1. 백엔드 디렉토리로 이동
```bash
cd backend
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 데이터베이스 마이그레이션
```bash
alembic upgrade head
```

5. 서버 실행
```bash
uvicorn app.main:app --reload
```

## API 문서

서버가 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 테스트

테스트를 실행하려면:
```bash
pytest
``` 