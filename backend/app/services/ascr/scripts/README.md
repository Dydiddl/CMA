# 📁 Scripts 폴더

ASCR 프로젝트의 다양한 스크립트들이 체계적으로 정리된 폴더입니다.

## 🗂️ 폴더 구조

```
scripts/
├── dev/                    # 개발·실험용 스크립트
│   ├── convert_dots_to_commas.py
│   ├── fix_hierarchy_structure*.py
│   ├── test_validation_rules.py
│   └── ...
├── main_entry/             # 주요 워크플로우 스크립트
│   ├── workflow_executor.py
│   ├── extract_and_split.py
│   ├── pdf_text_analyzer.py
│   └── ...
├── utils/                  # 유틸리티 스크립트
│   ├── rename_standard_price_files.py
│   ├── year_selector.py
│   └── ...
├── 개발 보류/              # 개발 중단/보류 스크립트
│   └── download_standard_price_list.py
└── README.md
```

## 🎯 주요 기능

### 1. **년도별 파일 경로 관리 시스템**

#### 📁 `config/file_paths.py`
- **목적**: 년도별 표준품셈 PDF 및 ground truth 파일 경로를 동적으로 관리
- **기능**:
  - 사용 가능한 년도 자동 감지
  - 파일 존재 여부 검증
  - 최신 년도 자동 선택
  - 수정본/적용본 우선순위 처리

#### 🎯 `scripts/utils/year_selector.py`
- **목적**: 사용자가 년도를 선택할 수 있는 대화형 인터페이스
- **사용법**:
  ```bash
  python scripts/utils/year_selector.py
  ```

### 2. **수정된 스크립트들**

#### 📋 `scripts/main_entry/workflow_executor.py`
- **변경사항**: 하드코딩된 PDF 경로를 동적 경로 관리로 변경
- **새로운 기능**:
  - `--year` 파라미터로 년도 지정 가능
  - 자동으로 최신 년도 선택
  - 파일 존재 여부 검증

#### 📄 `scripts/main_entry/pdf_text_analyzer.py`
- **변경사항**: 년도 기반 PDF 파일 선택 기능 추가
- **사용법**:
  ```bash
  # 최신 년도 사용
  python scripts/main_entry/pdf_text_analyzer.py
  
  # 특정 년도 지정
  python scripts/main_entry/pdf_text_analyzer.py --year 2024
  
  # 직접 PDF 파일 지정
  python scripts/main_entry/pdf_text_analyzer.py --pdf path/to/file.pdf
  ```

## 🚀 사용 방법

### 1. **년도 선택하기**
```bash
# 대화형 년도 선택
python scripts/utils/year_selector.py

# 또는 직접 년도 지정
python scripts/main_entry/workflow_executor.py --year 2024
```

### 2. **파일 경로 확인하기**
```bash
# 사용 가능한 파일 목록 확인
python config/file_paths.py
```

### 3. **워크플로우 실행하기**
```bash
# 최신 년도로 실행
python scripts/main_entry/workflow_executor.py

# 특정 년도로 실행
python scripts/main_entry/workflow_executor.py --year 2024 --output output_2024
```

## 🔧 개발 가이드

### 새로운 스크립트 작성 시

1. **년도 파라미터 지원**:
   ```python
   from config.file_paths import get_standard_price_pdf_path, validate_year
   
   def main():
       parser = argparse.ArgumentParser()
       parser.add_argument("--year", type=int, help="사용할 년도")
       args = parser.parse_args()
       
       year = args.year or get_latest_year()
       pdf_path = get_standard_price_pdf_path(year)
   ```

2. **파일 검증**:
   ```python
   if not validate_year(year):
       print(f"❌ 유효하지 않은 년도: {year}")
       return
   
   if not pdf_path or not pdf_path.exists():
       print(f"❌ PDF 파일이 없습니다: {year}년")
       return
   ```

### 파일 경로 관리 시스템 활용

```python
from config.file_paths import FilePathManager

# 파일 매니저 초기화
file_manager = FilePathManager()

# 사용 가능한 년도 확인
available_years = file_manager.get_available_standard_price_years()
print(f"사용 가능한 년도: {available_years}")

# 특정 년도 파일 경로 가져오기
pdf_path = file_manager.get_standard_price_pdf_path(2024)
gt_path = file_manager.get_ground_truth_path(2024)

# 파일 정보 확인
file_info = file_manager.get_file_info(2024)
print(f"2024년 파일 정보: {file_info}")
```

## 📋 주의사항

1. **년도 변경 시**: 새로운 년도 PDF가 추가되면 자동으로 감지됩니다
2. **파일명 규칙**: `{년도}_construction_work_standard_price_list.pdf` 형식을 따라야 합니다
3. **파일 위치**: `input/By_year_Construction_work_standard_price_list/` 폴더에 저장해야 합니다
4. **Ground Truth**: `toc_ground_truth_{년도}.md` 형식으로 저장해야 합니다
5. **우선순위**: 적용본 > 수정본 > 기본본 순으로 파일을 찾습니다

## 🔄 향후 개선 계획

- [ ] 더 많은 스크립트에 년도 선택 기능 적용
- [ ] 자동 파일 다운로드 기능 추가
- [ ] 배치 처리 기능 강화
- [ ] 웹 인터페이스 추가 (선택사항) 