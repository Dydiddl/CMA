# 🧪 CMA 테스트 구조

## 📁 테스트 디렉토리 구조

```
tests/
├── unit/              # 단위 테스트
│   ├── test_labor_service.py
│   ├── test_estimator_parser.py
│   └── test_estimator_generator.py
├── integration/       # 통합 테스트
│   ├── integration_test_suite.py
│   └── test_ascr_advanced.py
├── api/              # API 테스트
│   └── test_contracts.py
├── performance/      # 성능 테스트
│   ├── test_performance.py
│   ├── load_test.py
│   └── performance_test_labor.py
├── fixtures/         # 테스트 데이터
│   └── __init__.py
├── conftest.py       # 공통 설정
└── __init__.py
```

## 🚀 테스트 실행 방법

### 1. 전체 테스트 실행
```bash
pytest
```

### 2. 특정 타입의 테스트만 실행
```bash
# 단위 테스트만
pytest tests/unit/ -m unit

# 통합 테스트만
pytest tests/integration/ -m integration

# API 테스트만
pytest tests/api/ -m api

# 성능 테스트만
pytest tests/performance/ -m performance
```

### 3. 특정 모듈 테스트
```bash
# ASCR 모듈 테스트
pytest -m ascr

# Excel 처리 테스트
pytest -m excel

# PDF 처리 테스트
pytest -m pdf
```

### 4. 커버리지 리포트 생성
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### 5. 테스트 실행 스크립트 사용
```bash
python run_tests.py
```

## 📊 테스트 마커 (Markers)

| 마커 | 설명 | 예시 |
|------|------|------|
| `unit` | 단위 테스트 | `pytest -m unit` |
| `integration` | 통합 테스트 | `pytest -m integration` |
| `api` | API 테스트 | `pytest -m api` |
| `performance` | 성능 테스트 | `pytest -m performance` |
| `slow` | 느린 테스트 | `pytest -m "not slow"` |
| `ascr` | ASCR 모듈 테스트 | `pytest -m ascr` |
| `excel` | Excel 처리 테스트 | `pytest -m excel` |
| `pdf` | PDF 처리 테스트 | `pytest -m pdf` |

## 🔧 테스트 설정

### pytest.ini 설정
- 테스트 경로: `tests/`
- 파일 패턴: `test_*.py`
- 클래스 패턴: `Test*`
- 함수 패턴: `test_*`
- 커버리지 리포트 자동 생성

### conftest.py 픽스처
- `client`: FastAPI 테스트 클라이언트
- `db_session`: 데이터베이스 세션
- `sample_contract_data`: 샘플 계약 데이터
- `sample_labor_data`: 샘플 노무 데이터
- `sample_financial_data`: 샘플 재무 데이터
- `large_dataset`: 대용량 테스트 데이터

## 📈 성능 테스트 기준

### API 성능 목표
- 계약 목록 조회: 2초 이내
- 계약 검색: 1초 이내
- 동시 요청 처리: 5초 이내 (10개 요청)
- 메모리 사용량: 100MB 이내 증가

### 데이터베이스 성능 목표
- 대량 삽입: 10초 이내 (1000개 레코드)
- 복잡한 집계 쿼리: 1초 이내
- 캐시 히트: 0.1초 이내

### ASCR 모듈 성능 목표
- PDF 처리: 5초 이내
- Excel 처리: 2초 이내

## 🧪 테스트 작성 가이드

### 단위 테스트 작성
```python
import pytest
from unittest.mock import Mock, patch

class TestContractService:
    def test_create_contract_success(self, db_session):
        """계약 생성 성공 테스트"""
        # Given
        contract_data = {"name": "테스트 계약"}
        
        # When
        result = contract_service.create_contract(contract_data)
        
        # Then
        assert result.name == "테스트 계약"
```

### API 테스트 작성
```python
def test_create_contract_api(self, client, sample_contract_data):
    """계약 생성 API 테스트"""
    response = client.post("/api/v1/contracts/", json=sample_contract_data)
    
    assert response.status_code == 201
    assert response.json()["status"] == "success"
```

### 성능 테스트 작성
```python
def test_api_performance(self, client, large_dataset):
    """API 성능 테스트"""
    start_time = time.time()
    response = client.get("/api/v1/contracts/")
    execution_time = time.time() - start_time
    
    assert response.status_code == 200
    assert execution_time < 2.0  # 2초 이내
```

## 🔍 테스트 커버리지 목표

- **전체 커버리지**: 80% 이상
- **단위 테스트**: 85% 이상
- **통합 테스트**: 75% 이상
- **API 테스트**: 90% 이상

## 🚨 주의사항

1. **테스트 격리**: 각 테스트는 독립적으로 실행되어야 함
2. **데이터 정리**: 테스트 후 데이터베이스 상태를 원래대로 복원
3. **성능 테스트**: 실제 환경과 유사한 조건에서 실행
4. **모킹 사용**: 외부 의존성은 적절히 모킹하여 테스트 속도 향상

## 📝 테스트 추가 시 체크리스트

- [ ] 테스트 파일명이 `test_*.py` 패턴을 따르는가?
- [ ] 테스트 클래스명이 `Test*` 패턴을 따르는가?
- [ ] 테스트 함수명이 `test_*` 패턴을 따르는가?
- [ ] 적절한 마커가 설정되어 있는가?
- [ ] 테스트가 독립적으로 실행되는가?
- [ ] 에러 케이스도 테스트하는가?
- [ ] 성능 테스트가 필요한가?
- [ ] 커버리지가 증가하는가? 