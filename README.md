# 건설 관리 시스템 (Construction Management System)

## 프로젝트 개요
건설 프로젝트의 효율적인 관리를 위한 종합적인 관리 시스템입니다. 계약 관리, 진행 상황 추적, 재무 기록, 문서 관리 등 건설 프로젝트의 전반적인 업무를 디지털화하여 관리할 수 있습니다.

## 🧩 주요 특징
- 설치형 실행 파일로 배포 (.exe)
- UI는 React + TypeScript + Tauri
- 백엔드는 Python + FastAPI
- 데이터베이스는 Supabase(PostgreSQL 기반)로, 클라우드 연동
- 문서 작업(HWP, Excel 등)은 백엔드에서 Python으로 처리

## 🎯 주요 기능
1. **계약 관리**  
   - 공사명, 계약금액, 계약일, 발주처, 상태관리  
   - 계약서 및 첨부 문서 업로드

2. **계약 업무 처리**
   - 내부 양식으로 한글/워드/엑셀 문서작성
   - 단계별 계약 절차 체크리스트 관리

3. **노무비 관리**
   - 일용직 명부 관리, 작업일지 업로드
   - 주간/월간 집계 기능

4. **매출 관리**
   - 공사별 수입·지출 내역 등록
   - 월별/분기별 통계 및 시각화

5. **거래처 관리**
   - 기본정보, 담당자, 사업자등록증 및 통장사본 업로드
   - 계약 및 공사와 연동

## 🛠 기술 스택
- **Frontend**: React + TypeScript + Tauri
- **Backend**: Python + FastAPI
- **Database**: 
  - 개발: PostgreSQL (로컬)
  - 프로덕션: Supabase (PostgreSQL 기반)

## 🚀 시작하기

### 필수 요구사항
- Node.js 18+
- Python 3.12+
- PostgreSQL 14+

### 설치 방법
1. 저장소 클론
```bash
git clone https://github.com/yourusername/construction-management.git
cd construction-management
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
uvicorn main:app --reload

# 프론트엔드 개발 서버 (새 터미널에서)
cd frontend
npm run tauri dev
```

## 📚 문서
- [개발 가이드](docs/development/development-guide.md)
- [설계 문서](docs/design/design-overview.md)
- [API 문서](docs/design/api-design.md)

## 📝 라이선스
이 프로젝트는 [라이선스 이름] 라이선스 하에 배포됩니다.

## 현재 진행 상황
- [x] 프로젝트 기본 구조 설계
- [x] 데이터베이스 스키마 설계
- [x] API 문서화
- [x] 기본 모델 구현
  - [x] Project
  - [x] Contract
  - [x] Progress
  - [x] FinancialRecord
  - [x] Document
- [x] 테스트 환경 구성
- [ ] API 엔드포인트 구현
- [ ] 프론트엔드 개발
  - [ ] Tauri 데스크톱 앱 UI 구현
  - [ ] 오프라인 지원 기능
  - [ ] 로컬 데이터 동기화
- [ ] 사용자 인증 시스템
- [ ] 파일 업로드 시스템
- [ ] 보고서 생성 시스템

## 프로젝트 구조
```
construction-management/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── api/
│   │   └── core/
│   ├── tests/
│   └── migrations/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── tauri/
│   ├── public/
│   └── package.json
└── docs/
    ├── api/
    ├── architecture/
    └── guides/
```

## 기여 방법
1. 이슈 생성
2. 브랜치 생성
3. 변경사항 커밋
4. Pull Request 생성

## 연락처
- 이메일: your.email@example.com
- 프로젝트 관리자: [이름]
