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
- **PyPDF2/PyMuPDF** (PDF 처리 - ASCR 모듈)

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
├── frontend/               # React + TypeScript 프론트엔드
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   └── services/       # API 서비스
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

2. **백엔드 설정**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **프론트엔드 설정**
```bash
cd frontend
npm install
```

4. **데이터베이스 설정**
```bash
# PostgreSQL 데이터베이스 생성
createdb cma_db

# 마이그레이션 실행
cd backend
alembic upgrade head
```

5. **개발 서버 실행**
```bash
# 백엔드 (터미널 1)
cd backend
uvicorn app.main:app --reload

# 프론트엔드 (터미널 2)
cd frontend
npm run dev

# Tauri 개발 (터미널 3)
cd src-tauri
cargo tauri dev
```

### 환경 변수 설정

`.env` 파일을 생성하고 다음 설정을 추가하세요:

```env
# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost/cma_db

# Redis
REDIS_URL=redis://localhost:6379

# 보안
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 성능 설정
MAX_WORKERS=4
CACHE_TTL=3600
API_TIMEOUT=30
```

## 📊 주요 기능

### 1. 계약 관리
- 계약 생성, 수정, 삭제
- 계약 상태 추적
- 계약서 자동 생성
- 계약 이력 관리

### 2. 재무 관리
- 예산 계획 및 추적
- 비용 분석 및 보고
- 수익성 분석
- 재무 보고서 자동 생성

### 3. 노무 관리
- 인력 배치 및 관리
- 작업 시간 추적
- 임금 계산
- 노무비 분석

### 4. 문서 처리 (ASCR 모듈)
- PDF 텍스트 추출
- 목차 자동 생성
- 문서 분할 및 병합
- 표준품셈 자동 적용

### 5. Excel 처리
- 대용량 Excel 파일 처리
- 데이터 자동 변환
- 보고서 자동 생성
- 데이터 검증 및 정리

## 🔧 개발 가이드

### 코드 스타일

#### Python (PEP8 준수)
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모듈 설명
"""

from typing import List, Dict, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ExampleService:
    """서비스 클래스 설명"""
    
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
    
    async def process_data(self, data: List[str]) -> List[Dict]:
        """데이터 처리 - 비동기"""
        # 비동기 처리 로직
        return []
```

#### TypeScript (ESLint 준수)
```typescript
// 파일명: example-service.ts
// 컴포넌트명: ExampleService
// 변수명: camelCase

interface ExampleData {
  id: string;
  name: string;
  status: string;
}

export const ExampleService: React.FC<{
  data: ExampleData[];
  onUpdate: (data: ExampleData) => void;
}> = ({ data, onUpdate }) => {
  const handleUpdate = async (item: ExampleData) => {
    try {
      await onUpdate(item);
    } catch (error) {
      console.error('업데이트 실패:', error);
    }
  };

  return (
    <div className="example-service">
      {/* 컴포넌트 내용 */}
    </div>
  );
};
```

### 성능 최적화 패턴

#### 비동기 처리
```python
# 비동기 API 엔드포인트
@app.post("/contracts")
async def create_contract(contract_data: ContractCreate):
    # 비동기 서비스 호출
    contract = await contract_service.create_contract(contract_data)
    return contract
```

#### 멀티프로세싱
```python
# CPU 집약적 작업
from multiprocessing import Pool

def process_large_data(data_chunks):
    with Pool() as pool:
        results = pool.map(process_chunk, data_chunks)
    return results
```

#### 캐싱 전략
```python
# Redis 캐싱
@cache_manager.get_or_set("contracts:list", ttl=3600)
async def get_contracts_list():
    return await contract_service.get_all_contracts()
```

## 🧪 테스트

### 테스트 실행

```bash
# 백엔드 테스트
cd backend
pytest

# 프론트엔드 테스트
cd frontend
npm test

# 전체 테스트 커버리지
pytest --cov=app --cov-report=html
```

### 테스트 커버리지 목표

- **전체 커버리지**: 80%
- **단위 테스트**: 85%
- **통합 테스트**: 75%
- **E2E 테스트**: 60%

## 📦 배포

### 개발 빌드

```bash
# Tauri 개발 빌드
cd src-tauri
cargo tauri build

# 생성된 파일
# Windows: target/release/bundle/msi/app_0.1.0_x64_en-US.msi
# macOS: target/release/bundle/dmg/app_0.1.0_x64.dmg
# Linux: target/release/bundle/appimage/app_0.1.0_amd64.AppImage
```

### 프로덕션 배포

```bash
# 백엔드 배포
cd backend
docker build -t cma-backend .
docker run -p 8000:8000 cma-backend

# 프론트엔드 배포
cd frontend
npm run build
```

## 🔄 버전 관리

### Semantic Versioning

- **MAJOR**: 기존 API와 호환되지 않는 변경
- **MINOR**: 기존 API와 호환되는 새로운 기능
- **PATCH**: 버그 수정

### 브랜치 전략

- **main**: 프로덕션 배포용
- **develop**: 개발 통합용
- **feature/**: 기능 개발
- **hotfix/**: 긴급 버그 수정
- **release/**: 릴리즈 준비

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 커밋 메시지 규칙

```
<type>(<scope>): <description>

# 타입
feat: 새로운 기능 추가
fix: 버그 수정
perf: 성능 개선
refactor: 코드 리팩토링
test: 테스트 코드 추가/수정
docs: 문서 수정
style: 코드 포맷팅
chore: 빌드 프로세스 변경

# 예시
feat(contract): 계약 생성 API 엔드포인트 추가
perf(database): 데이터베이스 쿼리 최적화
fix(performance): 메모리 누수 수정
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 연락처

- **프로젝트 관리자**: [이름] - [이메일]
- **기술 문의**: [이메일]
- **버그 리포트**: [GitHub Issues](https://github.com/your-username/cma/issues)

## 🙏 감사의 말

- [FastAPI](https://fastapi.tiangolo.com/) - 현대적이고 빠른 웹 프레임워크
- [Tauri](https://tauri.app/) - 안전하고 빠른 데스크톱 앱 프레임워크
- [React](https://reactjs.org/) - 사용자 인터페이스 구축 라이브러리
- [PostgreSQL](https://www.postgresql.org/) - 강력한 오픈소스 데이터베이스

---

**CMA** - 건설업계의 디지털 혁신을 이끄는 솔루션 🏗️
