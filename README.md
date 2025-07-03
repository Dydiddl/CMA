# 🏗️ CMA (Construction Management System)

**건설 공사 내역서 자동화 시스템** - 계약 관리, 재무 관리, 노무 관리, 문서 처리를 통합적으로 제공하는 **하이브리드 아키텍처** 기반의 데스크톱 애플리케이션입니다.

## 🎯 프로젝트 개요

CMA는 건설업계의 복잡한 공사 내역서 작성과 관리를 자동화하여 업무 효율성을 극대화하는 시스템입니다. **Python 기반의 빠른 개발**과 **선택적 네이티브 최적화**를 통해 최고의 성능과 개발 생산성을 동시에 달성합니다.

### 🆕 주요 특징 (2025년 1월 기준)

- **🚀 하이브리드 아키텍처**: Python 기반 + 선택적 네이티브 최적화
- **📦 설치형 실행 파일**: Tauri 2.x 기반 (.exe, .app, .AppImage)
- **⚡ 성능 최적화**: 비동기 처리, 멀티프로세싱, 캐싱 전략
- **📊 샤딩 기능**: 대용량 데이터 처리 지원
- **🔍 ASCR 모듈**: PDF 처리 및 검증 기능 통합
- **🌐 크로스 플랫폼**: Windows, macOS, Linux 지원
- **🔄 실시간 동기화**: 로컬 + 클라우드 데이터 연동

### 📈 프로젝트 진행률 (2025년 1월 기준)

| 영역 | 진행률 | 상태 |
|------|--------|------|
| **백엔드 API** | 80% | 🟢 거의 완료 |
| **프론트엔드** | 60% | 🟡 진행 중 |
| **데이터베이스** | 90% | 🟢 거의 완료 |
| **테스트** | 50% | 🟡 진행 중 |
| **성능 최적화** | 40% | 🟡 진행 중 |
| **전체** | 65-70% | 🟡 안정적 개발 |

### 🎯 최우선 목표 (2025년 1-2월)

**핵심 기능 완성 및 안정화** - 기본적인 건설 관리 시스템으로 사용 가능한 상태 달성

#### 즉시 실행 (1-2주)
- [ ] **계약 관리 모듈 완성** - 계약 CRUD, 상태 추적, 자동 생성
- [ ] **재무 관리 모듈 완성** - 예산 관리, 비용 분석, 보고서 생성
- [ ] **노무 관리 모듈 완성** - 인력 관리, 시간 추적, 임금 계산
- [ ] **ASCR 모듈 통합** - PDF 처리, 목차 생성, 문서 자동화

#### 단기 목표 (2-4주)
- [ ] **기본 UI/UX 완성** - 대시보드, 네비게이션, 반응형 디자인
- [ ] **성능 최적화** - API 응답 시간 500ms 이내
- [ ] **테스트 커버리지** - 70% 이상 달성
- [ ] **보안 강화** - 인증/인가 시스템 완성

## 🏗️ ASCR 모듈 (건설공사 내역서 자동화)

### 개발 배경 및 필요성
- 건설공사 설계 시 반복적으로 유사한 구조의 문서를 수작업으로 작성
- 매년 변경되는 **표준품셈**, **노임단가**, **조달청 제비율표** 등을 반영해야 하는 반복적이고 비효율적인 과정
- **문서 자동화 시스템**을 구축하여 업무 강도를 줄이고, 실수를 방지하며, 최신 정보를 반영하는 체계 구축

### 주요 기능
| 기능 항목 | 설명 |
|-----------|------|
| 📥 PDF 데이터 수집 | 표준품셈 / 노임단가 / 제비율표 PDF 다운로드 및 저장 |
| 🧠 데이터 구조화 | PDF 내용 → JSON/CSV/DB 형태로 가공 및 분류 |
| 🧾 엑셀 내역서 자동 작성 | 가공된 데이터를 기존 엑셀 내역서 양식에 맞춰 자동 작성 |
| 🔁 노임단가 최신화 | 전기/당기 노임 비교 및 자동 대체 |
| ⚙ 제비율 자동 적용 | 조달청 제비율 데이터 기반 원가 계산서 최신화 |
| 🧮 수량산출 자동화 | 사용자가 UI로 수량 입력 → 수량산출서 및 내역서 자동 연결 |
| 🧍 사용자 입력 관리 | 자재단가, 공정내용, 공사 정보 등의 수동 입력 인터페이스 |
| 📄 서식 템플릿 유지 | 기존 엑셀 서식 틀 유지 및 작성 위치 자동 반영 |

### 개발 전략
- **우선 완성 가능한 기능부터 구축**하여 전체 흐름이 가능한 수준의 MVP(최소 기능 제품) 개발
- 이후 여유가 생길 때마다 머신러닝 등 고급 기능 또는 반복 입력 최소화 기능 추가
- 자동화가 불가능한 부분은 사용자 수동 입력으로 보완하는 **반자동 시스템**으로 초기 출발

## 🛠 기술 스택

### Frontend
- **React 18.2.0** + **TypeScript 5.8.3**
- **Vite 4.5.14** (빌드 도구)
- **Mantine 8.1.0** + **Material-UI 5.17.1** (UI 라이브러리)
- **Tauri 2.5.0** (데스크톱 앱 프레임워크)
- **Zustand 4.5.7** (상태 관리)
- **React Router DOM 6.30.1** (라우팅)

### Backend
- **Python 3.12+** (메인 개발 언어)
- **FastAPI 0.115.12** (비동기 웹 프레임워크)
- **SQLAlchemy 2.0.41** (ORM)
- **Alembic 1.16.1** (데이터베이스 마이그레이션)
- **Pydantic 2.11.7** (데이터 검증)
- **Uvicorn 0.34.3** (ASGI 서버)

### 데이터 처리
- **Pandas 2.3.0** (데이터 처리)
- **OpenPyXL 3.1.5** (Excel 처리)
- **XlsxWriter 3.2.3** (Excel 생성)
- **pypdf/PyMuPDF** (PDF 처리 - ASCR 모듈)

### 성능 최적화
- **Redis** (캐싱 및 세션 관리)
- **Celery** (비동기 작업 처리)
- **asyncio** (비동기 처리)
- **multiprocessing** (CPU 집약적 작업)
- **threading** (I/O 집약적 작업)
- **Connection Pooling** (데이터베이스 연결 최적화)

### Database
- **PostgreSQL 14+** (로컬 개발)
- **Supabase** (클라우드 프로덕션)
- **Redis** (캐싱 및 세션 저장소)

## 🏗️ 아키텍처 전략

### 하이브리드 아키텍처 접근법

CMA는 **하이브리드 아키텍처**를 채택하여 개발 속도와 성능을 모두 최적화합니다:

#### 1단계: Python 기반 개발 (현재)
```python
# 빠른 개발과 풍부한 생태계 활용
class ContractService:
    async def create_contract(self, contract_data: ContractCreate) -> Contract:
        # 비동기 처리로 성능 최적화
        contract = Contract(**contract_data.dict())
        self.db.add(contract)
        await self.db.commit()
        return contract
```

#### 2단계: 성능 최적화 (진행 중)
```python
# 멀티프로세싱과 캐싱으로 성능 향상
class PerformanceOptimizedService:
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.cache = Redis()
    
    async def process_large_data(self, data_chunks: List[str]) -> List[float]:
        # CPU 집약적 작업을 스레드 풀에서 실행
        tasks = [
            loop.run_in_executor(self.thread_pool, self.expensive_calculation, chunk)
            for chunk in data_chunks
        ]
        return await asyncio.gather(*tasks)
```

#### 3단계: 선택적 네이티브 전환 (계획)
```python
# 핵심 성능 모듈만 네이티브로 전환
class NativeOptimizedProcessor:
    def __init__(self):
        self.native_lib = ctypes.CDLL("./native_optimizations.dll")
    
    def process_pdf_native(self, pdf_path: str) -> Dict[str, Any]:
        # 네이티브 라이브러리로 PDF 처리 최적화
        result = self.native_lib.process_pdf(pdf_path.encode())
        return self._parse_native_result(result)
```

### 성능 최적화 전략

#### 성능 지표 (KPI)
- **API 응답 시간**: 500ms 이내
- **데이터베이스 쿼리**: 100ms 이내
- **파일 처리**: 2초 이내 (1MB 기준)
- **동시 사용자**: 100명 이상
- **시스템 가용성**: 99.9%

#### 최적화 우선순위
1. **HIGH**: PDF 처리, 대용량 Excel 처리, 복잡한 수식 계산
2. **MEDIUM**: API 응답 시간, 파일 업로드/다운로드, 캐싱
3. **LOW**: UI 렌더링, 로그 처리, 설정 관리

## 📁 프로젝트 구조

```
CMA/
├── backend/                 # Python FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 엔드포인트
│   │   ├── models/         # 데이터베이스 모델
│   │   ├── schemas/        # Pydantic 스키마
│   │   ├── services/       # 비즈니스 로직
│   │   │   ├── ascr/       # ASCR 모듈 (PDF 처리)
│   │   │   ├── excel/      # Excel 처리
│   │   │   └── estimator/  # 추정서 생성
│   │   └── core/           # 설정 및 보안
│   └── main.py             # 백엔드 서버 진입점
├── frontend/               # React + TypeScript 프론트엔드
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   └── services/       # API 서비스
├── desktop/                # PySide6 데스크톱 앱 (실험적)
│   ├── ui/                 # PySide6 UI 컴포넌트
│   ├── core/               # 공통 비즈니스 로직
│   └── main.py             # 데스크톱 앱 진입점
├── docs/                   # 프로젝트 문서
│   ├── ASCR_PROJECT_SPECIFICATION.md  # ASCR 프로젝트 명세서
│   ├── ASCR_MODULE_TEMPLATE.md        # ASCR 모듈 템플릿
│   ├── PROJECT_RULES.md               # 프로젝트 규칙
│   └── ...                 # 기타 문서들
├── scripts/                # 유틸리티 스크립트
│   ├── fix_logging_imports.py         # 로깅 import 수정
│   ├── fix_pyside6_signals.py         # PySide6 시그널 수정
│   └── ...                 # 기타 스크립트들
├── test/                   # 테스트 파일들
│   ├── api_connection_test.py         # API 연결 테스트
│   ├── realtime_api_test.py           # 실시간 API 테스트
│   ├── simple_test_server.py          # 간단한 테스트 서버
│   └── ...                 # 기타 테스트들
└── src-tauri/             # Tauri 데스크톱 앱 설정
```

### ASCR 모듈 구조
```
backend/app/services/ascr/
├── src/                    # 핵심 소스 코드
│   ├── common/            # 공통 모듈
│   ├── utils/             # 유틸리티 모듈
│   ├── classifier/        # 분류기
│   ├── converter/         # 변환기
│   └── validate/          # 검증
├── scripts/               # 실행 스크립트
├── input/                 # 입력 파일
├── output/                # 출력 파일
└── logs/                  # 로그 파일
```

## 🚀 시작하기

### 필수 요구사항

- **Python**: 3.12+
- **Node.js**: 18+
- **PostgreSQL**: 14+
- **Redis**: 6+
- **Rust**: 1.77+ (Tauri 빌드용)

### 설치 및 실행

1. **저장소 클론**
```bash
git clone https://github.com/your-username/cma.git
cd cma
```

2. **환경 설정**
```bash
# 백엔드 환경 설정
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는 venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 프론트엔드 환경 설정
cd ../frontend
npm install
```

3. **데이터베이스 설정**
```bash
# PostgreSQL 및 Redis 실행 (Docker 사용)
docker-compose up -d postgres redis
```

4. **개발 서버 실행**
```bash
# 백엔드 서버 (새 터미널)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프론트엔드 서버 (새 터미널)
cd frontend
npm run dev
```

### Docker를 사용한 전체 스택 실행
```bash
# 개발 환경
docker-compose -f docker-compose.dev.yml up

# 프로덕션 환경
docker-compose up
```

## 📚 문서

- [ASCR 프로젝트 명세서](docs/ASCR_PROJECT_SPECIFICATION.md) - 건설공사 내역서 자동화 시스템 상세 명세
- [ASCR 모듈 템플릿](docs/ASSCR_MODULE_TEMPLATE.md) - ASCR 모듈 개발 템플릿
- [프로젝트 규칙](docs/PROJECT_RULES.md) - 개발 규칙 및 가이드라인
- [API 문서](docs/API_DOCUMENTATION.md) - 백엔드 API 문서
- [데이터베이스 스키마](docs/DATABASE_SCHEMAS.md) - 데이터베이스 구조 문서

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 연락처

프로젝트 링크: [https://github.com/your-username/cma](https://github.com/your-username/cma)

---

**CMA** - 건설 관리의 미래를 만들어갑니다 🏗️
