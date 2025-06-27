# 건설 관리 시스템 (Construction Management System)

## 프로젝트 개요
건설 프로젝트의 효율적인 관리를 위한 종합적인 관리 시스템입니다. 계약 관리, 진행 상황 추적, 재무 기록, 문서 관리 등 건설 프로젝트의 전반적인 업무를 디지털화하여 관리할 수 있습니다.

## 🧩 주요 특징
- 설치형 실행 파일로 배포 (.exe) - Tauri 2.x 기반
- UI는 React + TypeScript + Vite + Mantine/MUI
- 백엔드는 Python + FastAPI + SQLAlchemy
- 데이터베이스는 PostgreSQL (로컬) + Supabase (클라우드 연동)
- 문서 작업(Excel 등)은 백엔드에서 Python으로 처리
- 샤딩 기능으로 대용량 데이터 처리 지원

## 🎯 주요 기능
1. **계약 관리**  
   - 공사명, 계약금액, 계약일, 발주처, 상태관리  
   - 계약서 및 첨부 문서 업로드
   - 계약 추정서 생성 및 관리

2. **계약 업무 처리**
   - 내부 양식으로 Excel 문서작성
   - 단계별 계약 절차 체크리스트 관리
   - PDF to Word 변환 기능

3. **노무비 관리**
   - 일용직 명부 관리, 작업일지 업로드
   - 주간/월간 집계 기능
   - 노동자별 비용 추적

4. **매출 관리**
   - 공사별 수입·지출 내역 등록
   - 월별/분기별 통계 및 시각화
   - 거래 내역 관리

5. **거래처 관리**
   - 기본정보, 담당자, 사업자등록증 및 통장사본 업로드
   - 계약 및 공사와 연동
   - 벤더 정보 관리

6. **Excel 처리**
   - Excel 파일 업로드 및 검증
   - 데이터 처리 및 변환
   - 템플릿 기반 문서 생성

## 🛠 기술 스택
- **Frontend**: 
  - React 18.2.0 + TypeScript 5.8.3
  - Vite 4.5.14 (빌드 도구)
  - Mantine 8.1.0 + Material-UI 5.17.1 (UI 라이브러리)
  - Tauri 2.5.0 (데스크톱 앱 프레임워크)
  - Zustand 4.5.7 (상태 관리)
  - React Router DOM 6.30.1 (라우팅)

- **Backend**: 
  - Python 3.12+ + FastAPI 0.115.12
  - SQLAlchemy 2.0.41 (ORM)
  - Alembic 1.16.1 (데이터베이스 마이그레이션)
  - Pydantic 2.11.7 (데이터 검증)
  - Uvicorn 0.34.3 (ASGI 서버)

- **Database**: 
  - PostgreSQL 14+ (로컬 개발)
  - Supabase (클라우드 프로덕션)

- **추가 도구**:
  - Pandas 2.3.0 (데이터 처리)
  - OpenPyXL 3.1.5 (Excel 처리)
  - XlsxWriter 3.2.3 (Excel 생성)

## 🚀 시작하기

### 필수 요구사항
- Node.js 18+
- Python 3.12+
- PostgreSQL 14+
- Rust 1.77.2+ (Tauri 빌드용)

### 설치 방법
1. 저장소 클론
```bash
git clone https://github.com/Dydiddl/CMA.git
cd CMA
```

2. 백엔드 설정
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. 데이터베이스 설정
```bash
alembic upgrade head
```

4. 프론트엔드 설정
```bash
cd frontend
npm install
```

5. 개발 서버 실행
```bash
# 백엔드 서버
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# 프론트엔드 개발 서버 (새 터미널에서)
cd frontend
npm run tauri dev
```

## 📚 문서
- [개발 가이드](docs/development/development-guide.md)
- [설계 문서](docs/design/design-overview.md)
- [API 문서](docs/design/api-design.md)
- [데이터베이스 스키마](docs/architecture/database-schema.md)

## 📝 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 현재 진행 상황
- [x] 프로젝트 기본 구조 설계
- [x] 데이터베이스 스키마 설계
- [x] API 문서화
- [x] 기본 모델 구현
  - [x] User (사용자)
  - [x] Client (고객)
  - [x] Contract (계약)
  - [x] Document (문서)
  - [x] Financial (재무)
  - [x] Labor (노무)
  - [x] Vendor (거래처)
  - [x] Worker (노동자)
  - [x] Transaction (거래내역)
  - [x] Revenue (수익)
  - [x] Expense (지출)
  - [x] LaborCost (노무비)
- [x] API 엔드포인트 구현
  - [x] 계약 관리 API
  - [x] 재무 관리 API
  - [x] 노무 관리 API
  - [x] Excel 처리 API
- [x] 프론트엔드 개발
  - [x] Tauri 데스크톱 앱 UI 구현
  - [x] 사용자 인증 시스템
  - [x] 프로젝트 관리 페이지
  - [x] 작업 관리 페이지
  - [x] Excel 업로드/처리 기능
  - [x] 대시보드
- [x] 사용자 인증 시스템
- [x] 파일 업로드 시스템
- [x] Excel 처리 시스템
- [x] 샤딩 기능 구현
- [ ] 보고서 생성 시스템
- [ ] 오프라인 지원 기능
- [ ] 로컬 데이터 동기화

## 프로젝트 구조
```
CMA/
├── backend/
│   ├── app/
│   │   ├── models/          # 데이터베이스 모델
│   │   ├── schemas/         # Pydantic 스키마
│   │   ├── api/
│   │   │   ├── v1/         # API v1 엔드포인트
│   │   │   └── endpoints/  # 기타 엔드포인트
│   │   ├── services/       # 비즈니스 로직
│   │   ├── core/           # 설정 및 보안
│   │   └── middleware/     # 미들웨어
│   ├── tests/              # 테스트 코드
│   └── migrations/         # 데이터베이스 마이그레이션
├── frontend/
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── services/       # API 서비스
│   │   ├── hooks/          # 커스텀 훅
│   │   ├── contexts/       # React Context
│   │   ├── stores/         # 상태 관리
│   │   └── types/          # TypeScript 타입 정의
│   └── public/             # 정적 파일
├── src-tauri/              # Tauri 설정 및 Rust 코드
├── docs/                   # 프로젝트 문서
└── venv/                   # Python 가상환경
```

## 기여 방법
1. 이슈 생성
2. 브랜치 생성 (`git checkout -b feature/새기능`)
3. 변경사항 커밋
4. Pull Request 생성

## 설치 방법

### Unix/Linux/macOS 환경
```bash
cd backend
chmod +x setup.sh  # 실행 권한 부여
./setup.sh
```

### Windows 환경
```powershell
cd backend
# PowerShell 실행 정책 변경 (관리자 권한 필요)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

## 서버 실행
### Unix/Linux/macOS 환경
```bash
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Windows 환경
```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

## 빌드 및 배포
### 데스크톱 앱 빌드
```bash
cd frontend
npm run tauri build
```

### 백엔드 배포
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
