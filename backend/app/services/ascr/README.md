# ASCR - 건설업계 표준 문서 자동화 처리 시스템

## 📋 프로젝트 개요
ASCR(Automated Standard Construction Report)는 건설업계 표준 문서의 자동화 처리를 위한 Python 기반 시스템입니다.

## 🏗️ 시스템 아키텍처

### 디렉토리 구조
```
ASCR/
├── src/                    # 핵심 소스 코드
│   ├── common/            # 공통 모듈 (types, constants, exceptions, utils)
│   ├── utils/             # 유틸리티 모듈
│   │   ├── extract/       # 추출 관련 (toc_extractor, pdf_text_extractor)
│   │   ├── split/         # 분할 관련 (pdf_split_utils, pdf_merger)
│   │   └── config/        # 설정 관리
│   ├── classifier/        # 분류기
│   ├── converter/         # 변환기
│   └── validate/          # 검증
├── scripts/               # 실행 스크립트
├── input/                 # 입력 파일
│   └── By_year_Construction_work_standard_price_list/  # 연도별 표준품셈 PDF
├── output/                # 출력 파일
├── logs/                  # 로그 파일
└── main.py               # 메인 인터페이스
```

### 핵심 모듈 설명
- **TOCExtractor**: PDF에서 목차 구조 추출
- **PDFSplitter**: 목차 기반 PDF 분할
- **PDFTextExtractor**: PDF 텍스트 추출
- **ConfigManager**: 설정 관리

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 가상환경 활성화 (필수!)
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# 또는
venv\Scripts\activate.bat   # Windows Command Prompt

# 패키지 설치
pip install -r requirements.txt
```

### 2. 기본 사용법
```bash
# 메인 프로그램 실행
python main.py

# 1단계: 표준품셈 목차 추출
# 2단계: 텍스트 추출 및 목차 분석
# 3단계: 부문별 PDF 분할
```

## 📋 주요 기능

### 1. 표준품셈 목차 추출
- 입력: `input/By_year_Construction_work_standard_price_list/{년도}_construction_work_standard_price_list.pdf`
- 출력: `input/By_year_Construction_work_standard_price_list/index.pdf`
- 기능: PDF에서 목차 부분만 추출하여 별도 파일 생성

### 2. 텍스트 추출 및 목차 분석
- 입력: `input/By_year_Construction_work_standard_price_list/index.pdf`
- 출력: `output/toc_structure_*.json`, `output/mapping_config_*.json`
- 기능: 목차 구조 분석 및 JSON 형태로 저장

### 3. 부문별 PDF 분할
- 입력: `input/By_year_Construction_work_standard_price_list/index.pdf`, `output/toc_structure_*.json`
- 출력: `output/split_pdfs/`
- 기능: 부문별로 PDF 분할

## 🔧 개발 가이드

### 코드 구조 원칙
1. **계층적 구조**: common → utils → scripts → main
2. **단일 책임**: 각 모듈은 하나의 명확한 책임
3. **의존성 최소화**: 모듈 간 결합도 최소화
4. **확장 가능성**: 새로운 기능 추가 용이

### 개발 워크플로우
1. 가상환경 활성화 확인
2. 기능 개발/수정
3. 테스트 실행
4. 문서 업데이트

## 📊 현재 상태

### ✅ 완료된 기능
- [x] PDF 목차 추출
- [x] 텍스트 추출 및 분석
- [x] 목차 구조 JSON 생성
- [x] 기본 PDF 분할

### 🔄 진행 중인 개선
- [ ] 코드 구조 최적화
- [ ] 에러 처리 강화
- [ ] 로깅 시스템 개선
- [ ] 설정 관리 중앙화

### 📋 향후 계획
- [ ] 웹 인터페이스
- [ ] 고급 분석 기능
- [ ] 자동 다운로드 기능

## 🐛 문제 해결

### 자주 발생하는 문제
1. **가상환경 미활성화**: `ModuleNotFoundError` 발생
   - 해결: `.\venv\Scripts\Activate.ps1` 실행
2. **입력 파일 누락**: `FileNotFoundError` 발생
   - 해결: `input/By_year_Construction_work_standard_price_list/` 폴더에 필요한 PDF 파일 추가
3. **권한 문제**: 파일 생성 실패
   - 해결: 관리자 권한으로 실행

## 📞 지원

문제가 발생하면 다음을 확인해주세요:
1. 가상환경이 활성화되어 있는지
2. 필요한 파일이 올바른 위치에 있는지
3. 로그 파일에서 오류 메시지 확인

---

**버전**: 2.0  
**개발자**: ASCR Team  
**최종 업데이트**: 2025-01-23
