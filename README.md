# Construction Management Desktop App

## 🚀 프로젝트 개요
건설회사 내부에서 사용할 설치형 관리 프로그램입니다.

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
git clone [repository-url]
cd construction_management_app
```

2. 백엔드 설정
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. 프론트엔드 설정
```bash
cd frontend
npm install
```

### 실행 방법
1. 백엔드 서버 실행
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

2. 프론트엔드 개발 서버 실행
```bash
cd frontend
npm run tauri dev
```

## 📚 문서
- [개발 가이드](docs/development/development-guide.md)
- [설계 문서](docs/design/design-overview.md)
- [API 문서](docs/design/api-design.md)

## 📝 라이선스
이 프로젝트는 [라이선스 이름] 라이선스 하에 배포됩니다.
