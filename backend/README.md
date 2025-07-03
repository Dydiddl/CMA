# CMA Backend (ASCR 모듈 포함)

*최종 업데이트: 2025-07-03*

이 저장소는 **CMA(Construction Management System)** 전체 시스템의 일부로, 건설공사 내역서 자동화(ASCR) 모듈을 포함한 백엔드 서버입니다.

## 🏗️ 시스템 개요
- **CMA**는 계약, 노무, 재무, 문서(PDF/엑셀) 등 건설관리 업무를 자동화하는 하이브리드 시스템입니다.
- 본 백엔드는 FastAPI 기반 REST API와 **ASCR(Automated Standard Construction Report)** 모듈을 제공합니다.
- ASCR는 표준품셈/노임단가/제비율 PDF → 데이터화 → 엑셀 자동화, 연도별 데이터 관리, 반자동 입력, 템플릿 유지 등 최신 명세를 반영합니다.

## 🧩 주요 모듈 및 기능
- **ASCR**: PDF(표준품셈, 노임단가, 제비율 등) → 텍스트/구조화 데이터 추출 → 엑셀 내역서 자동 생성
  - 연도별 데이터 버전 관리(예: 표준품셈_2025)
  - 엑셀 템플릿 구조 유지, 수동 입력 보완(자재단가 등)
  - 원가계산서, 수량산출 자동화, 향후 ML 기반 고도화 확장 예정
- **계약/노무/재무 관리**: CRUD, 상태 추적, 보고서 등
- **공통**: 인증(JWT), 성능 모니터링, 캐싱, 헬스체크 등

## 📁 프로젝트 구조
```
backend/
├── app/
│   ├── api/                    # API 라우터 (v1/에 ASCR 등 포함)
│   ├── core/                   # 설정, 인증, DB
│   ├── models/                 # SQLAlchemy 모델
│   ├── schemas/                # Pydantic 스키마
│   ├── services/               # 비즈니스 로직 (ascr/ 등)
│   └── main.py                 # FastAPI 진입점
├── requirements.txt            # 의존성
└── ...
```

## 🚀 시작하기
### 1. 환경 설정
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 2. 데이터베이스 설정
```bash
cp .env.example .env
# .env 편집 후
alembic upgrade head
```
### 3. 서버 실행
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API 문서
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏗️ ASCR 모듈 명세 요약
- 반복적 문서작성 자동화, 최신 공공 데이터 반영
- PDF→데이터→엑셀 자동화, 연도별 데이터 관리, 반자동(수동입력 보완) 구조
- 엑셀 템플릿 유지, 수량산출/원가계산서 자동화, 향후 ML 고도화 예정
- 자세한 명세: `docs/`, `app/services/ascr/` 참고

## 🔧 개발 및 테스트
- PEP8, Black, isort, flake8 준수
- 테스트: pytest, `pytest --cov=app`
- 마이그레이션: alembic

## �� 라이선스
MIT License 