# ASCR (Automated Standard Construction Reference) - 개발자 가이드

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [아키텍처](#아키텍처)
3. [설치 및 설정](#설치-및-설정)
4. [개발 환경](#개발-환경)
5. [API 문서](#api-문서)
6. [테스트](#테스트)
7. [배포](#배포)
8. [기여 가이드](#기여-가이드)

## 🎯 프로젝트 개요

ASCR은 건설업계 표준 문서를 자동화하여 처리하는 Python 기반 시스템입니다.

### 주요 기능
- **PDF 파일 자동 분류**: 부문별, 장별 자동 분류
- **PDF 디버그 분석**: PDF 내용 추출 및 분석
- **룩업테이블 생성**: PDF 목차를 구조화된 테이블로 변환
- **매핑 설정 자동화**: 룩업테이블을 기반으로 매핑 설정 생성
- **PDF 페이지 분리**: 지정된 페이지 범위로 PDF 분리
- **PDF 파일 병합**: 분리된 PDF 파일들을 병합

## 🏗️ 아키텍처

### 디렉토리 구조
```
ASCR/
├── src/                    # 소스 코드
│   ├── classifier/         # PDF 분류 및 처리 로직
│   ├── converter/          # PDF 변환 도구
│   ├── utils/              # 유틸리티 함수들
│   │   ├── logger.py       # 로깅 시스템
│   │   ├── exceptions.py   # 예외 처리
│   │   ├── config_manager.py # 설정 관리
│   │   └── ect/            # 기타 유틸리티
│   └── common/             # 공통 모듈
├── config/                 # 설정 파일들
│   ├── config.yaml         # YAML 기반 설정
│   ├── mapping_config.json # 매핑 규칙
│   └── settings.py         # 기존 설정
├── scripts/                # 실행 스크립트들
├── tests/                  # 테스트 코드
│   ├── unit/               # 단위 테스트
│   ├── integration/        # 통합 테스트
│   └── fixtures/           # 테스트 데이터
├── docs/                   # 문서
├── input/                  # 입력 파일
├── output/                 # 출력 파일
├── logs/                   # 로그 파일
└── temp/                   # 임시 파일
```

### 핵심 모듈

#### 1. 로깅 시스템 (`src/utils/logger.py`)
- 체계적인 로그 관리
- 파일 및 콘솔 출력
- 로그 레벨별 분리
- 성능 측정 데코레이터

#### 2. 예외 처리 (`src/utils/exceptions.py`)
- ASCR 전용 예외 클래스
- 상세한 오류 정보
- 안전한 함수 실행

#### 3. 설정 관리 (`src/utils/config_manager.py`)
- YAML/JSON 설정 파일 지원
- 설정 검증 및 병합
- 백업 및 복원 기능

## 🚀 설치 및 설정

### 요구사항
- Python 3.8+
- Windows/Linux/macOS

### 설치 방법

1. **저장소 클론**
   ```bash
   git clone [repository-url]
   cd ASCR
   ```

2. **가상환경 생성 및 활성화**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # 또는
   venv\Scripts\activate     # Windows
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

### 설정

1. **기본 설정 파일 생성**
   ```bash
   # config/config.yaml이 자동으로 생성됩니다
   ```

2. **설정 커스터마이징**
   ```yaml
   # config/config.yaml
   pdf_processing:
     max_pages_per_file: 1000
     batch_size: 50
   
   logging:
     level: "INFO"
   ```

## 💻 개발 환경

### 개발 도구 설치
```bash
pip install -r requirements.txt
```

### 코드 포맷팅
```bash
# Black을 사용한 코드 포맷팅
black src/ tests/

# Flake8을 사용한 린팅
flake8 src/ tests/
```

### 타입 검사
```bash
# MyPy를 사용한 타입 검사
mypy src/
```

## 📚 API 문서

### 로깅 시스템

#### ASCRLogger 클래스
```python
from src.utils.logger import ASCRLogger

logger = ASCRLogger("module_name", log_dir=Path("logs"))
logger.info("정보 메시지")
logger.error("오류 메시지")
```

#### 데코레이터
```python
from src.utils.logger import log_function_call, log_performance

@log_function_call
@log_performance
def my_function():
    pass
```

### 예외 처리

#### 기본 예외
```python
from src.utils.exceptions import ASCRException, PDFProcessingError

# 기본 예외
raise ASCRException("오류 메시지", "ERROR_CODE")

# PDF 처리 오류
raise PDFProcessingError("PDF 처리 실패", pdf_path="file.pdf", page_number=5)
```

#### 안전한 실행
```python
from src.utils.exceptions import safe_execute

result, error = safe_execute(my_function, arg1, arg2)
if error:
    print(f"오류 발생: {error}")
```

### 설정 관리

#### ConfigManager 클래스
```python
from src.utils.config_manager import get_config_manager

config_manager = get_config_manager()
config = config_manager.load_yaml_config("config.yaml")

# 설정 값 가져오기
max_pages = config_manager.get_config_value(config, "pdf_processing.max_pages_per_file")

# 설정 값 설정
config_manager.set_config_value(config, "pdf_processing.batch_size", 100)
```

## 🧪 테스트

### 테스트 실행
```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/unit/test_logger.py

# 커버리지와 함께 실행
pytest --cov=src --cov-report=html
```

### 테스트 구조
- **단위 테스트**: 개별 함수/클래스 테스트
- **통합 테스트**: 모듈 간 상호작용 테스트
- **픽스처**: 테스트 데이터 및 설정

### 테스트 작성 가이드
```python
import pytest
from src.utils.logger import ASCRLogger

class TestASCRLogger:
    def test_logger_creation(self, temp_dir):
        logger = ASCRLogger("test", temp_dir)
        assert logger.name == "test"
```

## 📦 배포

### 패키징
```bash
# setup.py를 통한 패키징
python setup.py sdist bdist_wheel
```

### 배포 전 체크리스트
- [ ] 모든 테스트 통과
- [ ] 코드 포맷팅 완료
- [ ] 타입 검사 통과
- [ ] 문서 업데이트
- [ ] 버전 번호 업데이트

## 🤝 기여 가이드

### 개발 워크플로우
1. 이슈 생성
2. 브랜치 생성 (`feature/issue-number`)
3. 개발 및 테스트
4. PR 생성
5. 코드 리뷰
6. 머지

### 코드 스타일
- PEP 8 준수
- Black 포맷터 사용
- 타입 힌트 사용
- 문서화 주석 작성

### 커밋 메시지 규칙
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 업데이트
test: 테스트 추가/수정
refactor: 코드 리팩토링
```

## 📞 지원

### 문제 해결
1. 이슈 트래커 확인
2. 로그 파일 확인 (`logs/`)
3. 설정 파일 검증
4. 개발팀 문의

### 로그 분석
```bash
# 최근 로그 확인
tail -f logs/ascr.log

# 오류 로그 확인
grep "ERROR" logs/ascr_error.log
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 