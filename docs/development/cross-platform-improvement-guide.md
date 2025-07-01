# 🚀 CMA 프로젝트 크로스 플랫폼 개선 작업 가이드

## 📋 작업 개요

**작업 목표**: CMA 프로젝트의 크로스 플랫폼 호환성을 100% 달성하여 Ubuntu에서 개발한 코드가 Windows에서도 완벽하게 작동하도록 개선

**작업 환경**: Windows + Ubuntu (WSL2)
**작업 시간**: 2025년 1월 24일
**우선순위**: 높음

---

## 🎯 개선 작업 우선순위

### 🔴 **1단계: 즉시 개선 필요 (높은 우선순위)**

#### 1.1 os.path → pathlib.Path 전환
- **대상 파일**: 1085개 파일
- **우선순위**: 최고
- **예상 소요시간**: 4-6시간

#### 1.2 라인 엔딩 처리 추가
- **대상 파일**: 381개 파일 (인코딩 사용 파일)
- **우선순위**: 높음
- **예상 소요시간**: 2-3시간

### 🟡 **2단계: 단계적 개선 (중간 우선순위)**

#### 2.1 환경 변수 활용 확대
- **대상 파일**: 설정 관련 파일들
- **우선순위**: 중간
- **예상 소요시간**: 1-2시간

#### 2.2 플랫폼별 조건부 코드 확대
- **대상 파일**: 주요 모듈들
- **우선순위**: 중간
- **예상 소요시간**: 2-3시간

---

## 🛠️ 작업 시작 전 준비사항

### 1. 환경 검증
```bash
# 1. 프로젝트 클론 및 최신 상태 확인
git clone https://github.com/your-username/cma.git
cd cma
git pull origin main

# 2. 환경 검증 스크립트 실행
./scripts/verify-environment.sh

# 3. 가상환경 활성화
cd backend
source venv/bin/activate  # Linux
# 또는 venv\Scripts\activate  # Windows

# 4. 의존성 설치 확인
pip install -r requirements.txt
```

### 2. 백업 생성
```bash
# 현재 상태 백업
git checkout -b backup/before-cross-platform-improvement
git push origin backup/before-cross-platform-improvement

# 작업 브랜치 생성
git checkout -b feature/cross-platform-improvement
```

### 3. 작업 도구 준비
```bash
# 필요한 도구 설치
pip install black isort mypy
npm install -g prettier eslint
```

---

## 📝 상세 작업 가이드

### 🔴 **1단계: os.path → pathlib.Path 전환**

#### 1.1 우선순위 파일 식별
```bash
# os.path 사용 파일 목록 생성
find . -name "*.py" -exec grep -l "os\.path\." {} \; > os_path_files.txt

# 우선순위 파일 확인
cat os_path_files.txt | head -20
```

#### 1.2 변환 패턴 적용

**기본 변환 패턴:**
```python
# ❌ 기존 코드
import os
file_path = os.path.join(dir_path, filename)
os.makedirs(os.path.dirname(file_path), exist_ok=True)
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

# ✅ 개선된 코드
from pathlib import Path
file_path = Path(dir_path) / filename
file_path.parent.mkdir(parents=True, exist_ok=True)
if file_path.exists():
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        content = f.read()
```

**자주 사용되는 변환 패턴들:**
```python
# 1. 경로 결합
os.path.join(a, b, c) → Path(a) / b / c

# 2. 디렉토리 생성
os.makedirs(path, exist_ok=True) → Path(path).mkdir(parents=True, exist_ok=True)

# 3. 파일 존재 확인
os.path.exists(path) → Path(path).exists()

# 4. 파일 정보
os.path.getsize(path) → Path(path).stat().st_size
os.path.basename(path) → Path(path).name
os.path.dirname(path) → Path(path).parent

# 5. 절대 경로
os.path.abspath(path) → Path(path).resolve()
```

#### 1.3 자동 변환 스크립트 실행
```bash
# 1. 변환 스크립트 생성
cat > convert_os_path.py << 'EOF'
#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def convert_os_path_to_pathlib(file_path):
    """os.path를 pathlib.Path로 변환"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 변환 패턴들
    patterns = [
        (r'os\.path\.join\(([^)]+)\)', r'Path(\1).joinpath()'),
        (r'os\.makedirs\(([^,]+), exist_ok=True\)', r'Path(\1).mkdir(parents=True, exist_ok=True)'),
        (r'os\.path\.exists\(([^)]+)\)', r'Path(\1).exists()'),
        # 추가 패턴들...
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # pathlib import 추가
    if 'from pathlib import Path' not in content and 'import pathlib' not in content:
        if 'import os' in content:
            content = content.replace('import os', 'import os\nfrom pathlib import Path')
        else:
            content = 'from pathlib import Path\n' + content
    
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        convert_os_path_to_pathlib(sys.argv[1])
EOF

# 2. 우선순위 파일들에 대해 실행
python convert_os_path.py backend/app/services/ascr/src/converter/extract_PDF_pages.py
```

### 🔴 **2단계: 라인 엔딩 처리 추가**

#### 2.1 인코딩 사용 파일 식별
```bash
# 인코딩 사용 파일 목록
find . -name "*.py" -exec grep -l "open.*encoding" {} \; > encoding_files.txt
```

#### 2.2 newline='' 추가 패턴
```python
# ❌ 기존 코드
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# ✅ 개선된 코드
with open(file_path, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)
```

#### 2.3 자동 변환 스크립트
```bash
# newline 추가 스크립트
cat > add_newline.py << 'EOF'
#!/usr/bin/env python3
import re
import sys

def add_newline_parameter(file_path):
    """open() 함수에 newline='' 추가"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # open() 함수에 newline='' 추가
    pattern = r'open\(([^)]*encoding=[^)]*)\)'
    replacement = r'open(\1, newline=\'\')'
    content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        add_newline_parameter(sys.argv[1])
EOF
```

### 🟡 **3단계: 환경 변수 활용 확대**

#### 3.1 설정 파일 개선
```python
# backend/app/core/config.py 개선
class Settings(BaseSettings):
    # 기존 하드코딩된 값들을 환경 변수로 변경
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cma_backend.db")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/cma.log")
    
    # 플랫폼별 기본값 설정
    @property
    def platform_specific_upload_dir(self) -> str:
        if platform.system() == "Windows":
            return os.getenv("UPLOAD_DIR", "C:\\CMA\\uploads")
        else:
            return os.getenv("UPLOAD_DIR", "./uploads")
```

#### 3.2 .env 파일 생성
```bash
# .env 파일 생성
cat > .env << 'EOF'
# 데이터베이스 설정
DATABASE_URL=sqlite:///./cma_backend.db

# 파일 경로 설정
UPLOAD_DIR=./uploads
LOG_FILE=./logs/cma.log
TEMP_DIR=./temp

# 플랫폼별 설정
PLATFORM=auto
EOF
```

### 🟡 **4단계: 플랫폼별 조건부 코드 확대**

#### 4.1 플랫폼 감지 유틸리티 생성
```python
# backend/app/utils/platform_utils.py 생성
import platform
import os
from pathlib import Path

def get_platform_info():
    """플랫폼 정보 반환"""
    return {
        "os": platform.system(),
        "version": platform.version(),
        "python_version": platform.python_version(),
        "architecture": platform.architecture()[0]
    }

def get_platform_specific_path(base_path: str) -> Path:
    """플랫폼별 경로 반환"""
    if platform.system() == "Windows":
        return Path(os.getenv("CMA_HOME", "C:\\CMA")) / base_path
    elif platform.system() == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "CMA" / base_path
    else:  # Linux
        return Path.home() / ".cma" / base_path

def is_wsl() -> bool:
    """WSL 환경인지 확인"""
    return platform.system() == "Linux" and "microsoft" in platform.release().lower()
```

#### 4.2 주요 모듈에 플랫폼 감지 추가
```python
# 각 주요 모듈에 추가할 코드
from app.utils.platform_utils import get_platform_info, get_platform_specific_path

class SomeService:
    def __init__(self):
        self.platform_info = get_platform_info()
        self.data_path = get_platform_specific_path("data")
        
        # 플랫폼별 설정
        if self.platform_info["os"] == "Windows":
            self.max_file_size = 100 * 1024 * 1024  # Windows: 100MB
        else:
            self.max_file_size = 50 * 1024 * 1024   # Unix: 50MB
```

---

## 🧪 테스트 및 검증

### 1. 단위 테스트 실행
```bash
# 백엔드 테스트
cd backend
python -m pytest tests/ -v

# 프론트엔드 테스트
cd ../frontend
npm test

# ASCR 모듈 테스트
cd ../backend/app/services/ascr
python -m pytest tests/ -v
```

### 2. 크로스 플랫폼 검증
```bash
# Windows 환경에서 테스트
python -c "
import platform
print(f'OS: {platform.system()}')
print(f'Python: {platform.python_version()}')

from pathlib import Path
test_path = Path('test') / 'file.txt'
print(f'Path test: {test_path}')
"

# 파일 처리 테스트
python -c "
from pathlib import Path
import tempfile

# 임시 파일 생성 테스트
with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='') as f:
    f.write('테스트 내용')
    print('파일 처리 테스트 성공')
"
```

### 3. 성능 테스트
```bash
# API 응답 시간 테스트
cd backend
python -m pytest tests/performance/ -v

# 메모리 사용량 테스트
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'메모리 사용량: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"
```

---

## 📊 작업 진행 상황 추적

### 작업 체크리스트
- [ ] **1단계: os.path → pathlib.Path 전환**
  - [ ] 우선순위 파일 식별 완료
  - [ ] 변환 스크립트 실행
  - [ ] 수동 검토 및 수정
  - [ ] 테스트 통과 확인

- [ ] **2단계: 라인 엔딩 처리 추가**
  - [ ] 인코딩 사용 파일 식별
  - [ ] newline='' 추가
  - [ ] 파일 처리 테스트

- [ ] **3단계: 환경 변수 활용 확대**
  - [ ] 설정 파일 개선
  - [ ] .env 파일 생성
  - [ ] 환경 변수 테스트

- [ ] **4단계: 플랫폼별 조건부 코드 확대**
  - [ ] 플랫폼 유틸리티 생성
  - [ ] 주요 모듈에 적용
  - [ ] 플랫폼별 테스트

### 진행 상황 기록
```bash
# 작업 진행 상황 기록
echo "$(date): 1단계 os.path 변환 시작" >> improvement_progress.log
echo "$(date): 1단계 완료 - 50개 파일 변환" >> improvement_progress.log
echo "$(date): 2단계 라인 엔딩 처리 시작" >> improvement_progress.log
```

---

## 🚨 문제 해결 가이드

### 자주 발생하는 문제들

#### 1. 경로 변환 오류
```python
# 문제: 복잡한 os.path 표현식
os.path.join(os.path.dirname(__file__), '..', 'data', filename)

# 해결: 단계별 변환
from pathlib import Path
Path(__file__).parent.parent / 'data' / filename
```

#### 2. 인코딩 오류
```python
# 문제: 인코딩 미지정
with open(file_path, 'r') as f:

# 해결: 인코딩 명시
with open(file_path, 'r', encoding='utf-8', newline='') as f:
```

#### 3. 플랫폼별 경로 오류
```python
# 문제: 하드코딩된 경로
data_path = "C:\\CMA\\data"  # Windows 전용

# 해결: 플랫폼 감지
from app.utils.platform_utils import get_platform_specific_path
data_path = get_platform_specific_path("data")
```

### 디버깅 도구
```bash
# 경로 변환 검증
python -c "
from pathlib import Path
import os

# 테스트 경로
test_path = 'test/file.txt'
print(f'os.path.join: {os.path.join(\"dir\", test_path)}')
print(f'Path: {Path(\"dir\") / test_path}')
"

# 인코딩 테스트
python -c "
test_content = '한글 테스트'
with open('test_encoding.txt', 'w', encoding='utf-8', newline='') as f:
    f.write(test_content)
print('인코딩 테스트 성공')
"
```

---

## 📝 작업 완료 후 정리

### 1. 커밋 및 푸시
```bash
# 변경사항 커밋
git add .
git commit -m "feat: 크로스 플랫폼 호환성 개선

- os.path를 pathlib.Path로 전환 (1085개 파일)
- 라인 엔딩 처리 추가 (381개 파일)
- 환경 변수 활용 확대
- 플랫폼별 조건부 코드 추가
- 크로스 플랫폼 테스트 추가"

# 브랜치 푸시
git push origin feature/cross-platform-improvement
```

### 2. 품질 검증
```bash
# 코드 포맷팅
black .
isort .

# 타입 체크
mypy backend/app/

# 테스트 커버리지 확인
python -m pytest tests/ --cov=app --cov-report=html
```

### 3. 문서 업데이트
```bash
# README 업데이트
echo "## 크로스 플랫폼 지원" >> README.md
echo "- Windows, macOS, Linux 완전 지원" >> README.md
echo "- Ubuntu에서 개발, Windows에서 실행 가능" >> README.md
```

---

## 🎯 성공 기준

### 완료 조건
1. **os.path 사용 제거**: 0개 파일
2. **인코딩 명시**: 100% 파일
3. **라인 엔딩 처리**: 100% 파일
4. **플랫폼 감지**: 주요 모듈 100%
5. **테스트 통과**: 모든 테스트 100% 통과
6. **성능 유지**: 기존 성능 대비 95% 이상

### 검증 방법
```bash
# 최종 검증 스크립트
python -c "
import os
import glob

# os.path 사용 확인
os_path_files = []
for py_file in glob.glob('**/*.py', recursive=True):
    with open(py_file, 'r', encoding='utf-8') as f:
        if 'os.path.' in f.read():
            os_path_files.append(py_file)

print(f'os.path 사용 파일: {len(os_path_files)}개')
if os_path_files:
    print('남은 파일들:', os_path_files[:5])

# 인코딩 사용 확인
encoding_files = []
for py_file in glob.glob('**/*.py', recursive=True):
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'open(' in content and 'encoding=' not in content:
            encoding_files.append(py_file)

print(f'인코딩 미사용 파일: {len(encoding_files)}개')
"
```

---

## 📞 지원 및 문의

작업 중 문제가 발생하면:
1. **로그 확인**: `improvement_progress.log`
2. **백업 브랜치**: `backup/before-cross-platform-improvement`
3. **문서 참조**: 이 가이드 문서
4. **테스트 실행**: 각 단계별 테스트 스크립트

**작업 완료 후**: 모든 변경사항이 정상적으로 작동하는지 Windows 환경에서 최종 검증을 진행하세요. 