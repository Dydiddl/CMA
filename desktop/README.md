# CMA PySide6 데스크톱 애플리케이션

## 📁 프로젝트 구조

```
desktop/
├── api/                    # API 클라이언트
│   └── client.py          # 백엔드 API 통신 클라이언트
├── ui/                     # PySide6 UI 컴포넌트
│   ├── __init__.py
│   ├── main_window.py     # 메인 윈도우
│   ├── login_dialog.py    # 로그인 다이얼로그
│   ├── dashboard_tab.py   # 대시보드 탭
│   ├── contract_tab.py    # 계약 관리 탭
│   ├── financial_tab.py   # 재무 관리 탭
│   └── labor_tab.py       # 노무 관리 탭
├── main.py                # 애플리케이션 진입점
├── requirements.txt       # Python 의존성
└── README.md             # 이 파일
```

## 🚀 실행 방법

### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. 백엔드 서버 실행
```bash
# backend 폴더에서
cd ../backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 데스크톱 앱 실행
```bash
# desktop 폴더에서
cd desktop
python main.py
```

## 🏗️ 아키텍처

### 하이브리드 아키텍처
- **PySide6**: 데스크톱 UI 프레임워크
- **FastAPI**: 백엔드 API 서버
- **PostgreSQL**: 로컬 데이터베이스
- **Redis**: 캐싱 및 세션 관리

### API 통신
- **HTTP REST API**: 백엔드와 통신
- **JWT 토큰**: 인증 관리
- **비동기 처리**: UI 응답성 보장

## 📋 주요 기능

### 1. 인증 시스템
- 로그인/회원가입 다이얼로그
- JWT 토큰 기반 인증
- 자동 로그인 지원

### 2. 대시보드
- 실시간 통계 정보
- 프로젝트 진행률 차트
- 최근 활동 목록
- 시스템 상태 모니터링

### 3. 계약 관리
- 계약 목록 조회/검색
- 계약 생성/수정/삭제
- 계약 상태 추적
- 파일 첨부 지원

### 4. 재무 관리
- 수입/지출 기록
- 예산 관리
- 재무 보고서 생성
- 차트 및 그래프

### 5. 노무 관리
- 근로자 정보 관리
- 근무 시간 기록
- 임금 계산
- 인력 현황 분석

## 🔧 개발 가이드

### 새로운 탭 추가
1. `ui/` 폴더에 새 탭 파일 생성
2. `main_window.py`에 탭 추가
3. API 클라이언트에 관련 메서드 추가

### API 연동
```python
from api.client import get_api_client

# API 클라이언트 사용
api_client = get_api_client()
result = api_client.get_contracts()
```

### 스타일링
- CSS 스타일시트 사용
- 일관된 색상 팔레트 적용
- 반응형 디자인 고려

## 🐛 문제 해결

### 일반적인 문제
1. **PySide6 설치 실패**: Qt 의존성 확인
2. **API 연결 실패**: 백엔드 서버 실행 상태 확인
3. **데이터베이스 오류**: PostgreSQL 서비스 상태 확인

### 로그 확인
```bash
# 로그 레벨 설정
export PYTHONPATH=.
python main.py --log-level DEBUG
```

## 📦 배포

### 실행 파일 생성
```bash
# PyInstaller 사용
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Docker 컨테이너
```bash
# Docker 이미지 빌드
docker build -t cma-desktop .

# 컨테이너 실행
docker run -p 8000:8000 cma-desktop
```

## 🤝 기여 가이드

### 코드 스타일
- PEP 8 준수
- 타입 힌트 사용
- 한국어 주석 작성
- 에러 처리 포함

### 테스트
```bash
# 단위 테스트 실행
python -m pytest tests/

# UI 테스트
python -m pytest tests/ui/
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 등록해 주세요. 