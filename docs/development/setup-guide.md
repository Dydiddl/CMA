# 환경 설정 가이드

## 1. 개발 환경 요구사항

### 1.1 필수 소프트웨어
- Node.js 18+
- Python 3.12+
- PostgreSQL 14+
- Git

### 1.2 권장 개발 도구
- VS Code
- Postman (API 테스트)
- pgAdmin (데이터베이스 관리)

## 2. 로컬 개발 환경 설정

### 2.1 저장소 클론
```bash
git clone [repository-url]
cd construction_management_app
```

### 2.2 백엔드 설정

#### Python 가상환경 생성
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
```

#### 의존성 설치
```bash
pip install -r requirements.txt
```

#### 환경 변수 설정
1. `.env` 파일 생성
```bash
cp .env.example .env
```

2. 환경 변수 설정
```env
# 데이터베이스 설정
DATABASE_URL=postgresql://username:password@localhost:5432/construction_management

# 보안 설정
SECRET_KEY=your_secret_key_here
```

#### 데이터베이스 설정
1. PostgreSQL 데이터베이스 생성
```bash
createdb construction_management
```

2. 스키마 적용
```bash
psql -d construction_management -f schema.sql
```

### 2.3 프론트엔드 설정

#### 의존성 설치
```bash
cd frontend
npm install
```

#### 환경 변수 설정
1. `.env` 파일 생성
```bash
cp .env.example .env
```

2. 환경 변수 설정
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 3. 개발 서버 실행

### 3.1 백엔드 서버
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### 3.2 프론트엔드 서버
```bash
cd frontend
npm run tauri dev
```

## 4. 테스트 환경 설정

### 4.1 백엔드 테스트
```bash
cd backend
pytest
```

### 4.2 프론트엔드 테스트
```bash
cd frontend
npm test
```

## 5. 빌드 및 배포

### 5.1 백엔드 빌드
```bash
cd backend
pip install -r requirements.txt
```

### 5.2 프론트엔드 빌드
```bash
cd frontend
npm run tauri build
```

## 6. 문제 해결

### 6.1 일반적인 문제
1. **포트 충돌**
   - 백엔드: 8000번 포트 사용 중인 경우
   ```bash
   lsof -i :8000
   kill -9 [PID]
   ```

2. **데이터베이스 연결 오류**
   - PostgreSQL 서비스 실행 확인
   ```bash
   brew services list
   brew services start postgresql@14
   ```

3. **의존성 문제**
   - 가상환경 재생성
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 6.2 로그 확인
- 백엔드 로그: `backend/logs/`
- 프론트엔드 로그: 브라우저 개발자 도구

## 7. 개발 워크플로우

### 7.1 코드 작성
1. 새로운 브랜치 생성
```bash
git checkout -b feature/[feature-name]
```

2. 코드 작성 및 테스트

3. 커밋
```bash
git add .
git commit -m "feat: [feature description]"
```

4. 푸시
```bash
git push origin feature/[feature-name]
```

### 7.2 코드 리뷰
1. Pull Request 생성
2. 코드 리뷰 진행
3. 수정사항 반영
4. 머지 승인

## 8. 유용한 명령어

### 8.1 데이터베이스
```bash
# 데이터베이스 백업
pg_dump construction_management > backup.sql

# 데이터베이스 복원
psql construction_management < backup.sql
```

### 8.2 개발 도구
```bash
# 포맷팅
cd backend
black .
cd ../frontend
npm run format

# 린트
cd backend
flake8
cd ../frontend
npm run lint
``` 