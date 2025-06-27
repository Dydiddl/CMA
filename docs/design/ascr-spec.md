# ASCR 모듈 통합 명세서

## 📋 개요
ASCR(Automated Standard Construction Report) 모듈은 건설업계 표준 문서의 자동화 처리를 위한 Python 기반 시스템으로, CMA 프로젝트에 통합되어 PDF 처리 및 검증 기능을 제공합니다.

## 🏗️ 아키텍처

### 통합 구조
```
CMA/
├── backend/
│   └── app/
│       └── services/
│           └── ascr/           # ASCR 모듈
│               ├── src/        # 핵심 소스 코드
│               ├── scripts/    # 실행 스크립트
│               ├── config/     # 설정 파일
│               ├── docs/       # 문서
│               └── main.py     # 메인 인터페이스
```

### 핵심 컴포넌트
- **TOCExtractor**: PDF에서 목차 구조 추출
- **PDFSplitter**: 목차 기반 PDF 분할
- **PDFTextExtractor**: PDF 텍스트 추출
- **ConfigManager**: 설정 관리
- **StandardPriceDownloader**: 표준 가격 목록 자동 다운로드

## 🔌 API 설계

### 1. PDF 처리 API
```python
# PDF 목차 추출
POST /api/v1/ascr/extract-toc
{
    "pdf_file": "file",
    "year": "2025"
}

# PDF 텍스트 추출
POST /api/v1/ascr/extract-text
{
    "pdf_file": "file",
    "pages": [1, 2, 3]
}

# PDF 분할
POST /api/v1/ascr/split-pdf
{
    "pdf_file": "file",
    "toc_structure": "json_data"
}
```

### 2. 표준 가격 목록 API
```python
# 표준 가격 목록 다운로드
POST /api/v1/ascr/download-standard-price
{
    "year": "2025",
    "force_update": false
}

# 가격 목록 검증
POST /api/v1/ascr/validate-price-list
{
    "year": "2025"
}
```

### 3. 분석 API
```python
# 지반 진실 데이터 분석
POST /api/v1/ascr/analyze-ground-truth
{
    "data_file": "file",
    "analysis_type": "comprehensive"
}

# 계층 구조 수정
POST /api/v1/ascr/fix-hierarchy
{
    "structure_file": "file",
    "fix_type": "dots_to_commas"
}
```

## 📁 파일 구조

### 입력 디렉토리
```
backend/app/services/ascr/input/
├── By_year_Construction_work_standard_price_list/
│   ├── 2025_construction_work_standard_price_list.pdf
│   └── index.pdf
└── ground_truth/
    └── comprehensive_generation_report.md
```

### 출력 디렉토리
```
backend/app/services/ascr/output/
├── toc_structure_2025.json
├── mapping_config_2025.json
├── split_pdfs/
│   ├── section_1.pdf
│   ├── section_2.pdf
│   └── ...
└── analysis/
    └── ground_truth_analysis.json
```

## 🔧 설정

### 환경 변수
```bash
# ASCR 설정
ASCR_LOG_LEVEL=INFO
ASCR_OUTPUT_DIR=./output
ASCR_INPUT_DIR=./input
ASCR_TEMP_DIR=./temp

# 표준 가격 목록 설정
STANDARD_PRICE_URL=https://example.com/standard-price
STANDARD_PRICE_CACHE_DIR=./cache
```

### 설정 파일 (config/config.yaml)
```yaml
ascr:
  log_level: INFO
  output_dir: ./output
  input_dir: ./input
  temp_dir: ./temp
  
standard_price:
  url: https://example.com/standard-price
  cache_dir: ./cache
  force_update: false
  
pdf_processing:
  max_file_size: 100MB
  supported_formats: [pdf]
  text_extraction:
    min_confidence: 0.8
    language: ko
```

## 🚀 사용법

### 1. 기본 사용법
```python
from backend.app.services.ascr.main import ASCRProcessor

# ASCR 프로세서 초기화
processor = ASCRProcessor()

# PDF 목차 추출
toc_structure = processor.extract_toc("input/2025_standard_price.pdf")

# PDF 분할
split_files = processor.split_pdf("input/2025_standard_price.pdf", toc_structure)

# 표준 가격 목록 다운로드
processor.download_standard_price(2025)
```

### 2. FastAPI 통합
```python
from fastapi import APIRouter, UploadFile, File
from backend.app.services.ascr.main import ASCRProcessor

router = APIRouter(prefix="/ascr", tags=["ASCR"])

@router.post("/extract-toc")
async def extract_toc(file: UploadFile = File(...)):
    processor = ASCRProcessor()
    result = processor.extract_toc(file.file)
    return {"status": "success", "data": result}
```

## 🔍 모니터링 및 로깅

### 로그 구조
```
backend/app/services/ascr/logs/
├── ascr.log              # 메인 로그
├── pdf_processing.log    # PDF 처리 로그
├── download.log          # 다운로드 로그
└── error.log             # 에러 로그
```

### 메트릭
- PDF 처리 시간
- 파일 크기별 처리 성공률
- 다운로드 성공률
- 에러 발생 빈도

## 🧪 테스트

### 단위 테스트
```bash
cd backend/app/services/ascr
python -m pytest tests/ -v
```

### 통합 테스트
```bash
# CMA 프로젝트 루트에서
python -m pytest backend/tests/test_ascr_integration.py -v
```

## 🔒 보안 고려사항

### 파일 업로드 보안
- 파일 크기 제한 (100MB)
- 파일 형식 검증 (PDF만 허용)
- 악성 파일 스캔

### 데이터 보안
- 민감한 데이터 암호화
- 임시 파일 자동 삭제
- 접근 권한 제어

## 📊 성능 최적화

### 메모리 사용량 최적화
- 대용량 PDF 스트리밍 처리
- 임시 파일 자동 정리
- 메모리 사용량 모니터링

### 처리 속도 최적화
- 병렬 처리 지원
- 캐싱 시스템
- 배치 처리

## 🔄 버전 관리

### ASCR 모듈 버전
- 현재 버전: 2.0
- CMA 통합 버전: 1.0
- 호환성: Python 3.12+, FastAPI 0.115+

### 업데이트 계획
- 월별 보안 업데이트
- 분기별 기능 개선
- 연간 메이저 버전 업데이트

## 📞 지원 및 문제 해결

### 일반적인 문제
1. **메모리 부족**: PDF 파일 크기 줄이기
2. **처리 시간 초과**: 배치 크기 조정
3. **파일 권한 오류**: 디렉토리 권한 확인

### 로그 확인
```bash
tail -f backend/app/services/ascr/logs/ascr.log
```

### 디버그 모드
```bash
export ASCR_LOG_LEVEL=DEBUG
python backend/app/services/ascr/main.py
```

---

**문서 버전**: 1.0  
**최종 업데이트**: 2025-01-23  
**작성자**: CMA Development Team 