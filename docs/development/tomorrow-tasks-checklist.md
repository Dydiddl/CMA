# 📋 내일 Windows 환경 작업 체크리스트

## 🎯 작업 목표
**날짜**: 2025년 1월 24일  
**환경**: Windows + Ubuntu (WSL2)  
**목표**: CMA 프로젝트 크로스 플랫폼 호환성 100% 달성

---

## ✅ 사전 준비 체크리스트

### 1. 환경 설정
- [ ] 프로젝트 클론 완료
- [ ] 최신 코드 pull 완료
- [ ] 환경 검증 스크립트 실행: `./scripts/verify-environment.sh`
- [ ] 환경 설정 스크립트 실행 (필요시): `./scripts/setup-development-environment.sh`

### 2. 개발 환경 확인
- [ ] Python 3.12+ 설치 확인
- [ ] 가상환경 활성화: `source backend/venv/bin/activate`
- [ ] 의존성 설치: `pip install -r backend/requirements.txt`
- [ ] Cursor/VSCode 실행: `cursor CMA.code-workspace`

---

## 🔴 1단계: 즉시 개선 작업 (높은 우선순위)

### 1.1 os.path → pathlib.Path 전환
**예상 소요시간**: 4-6시간  
**대상 파일**: 1085개 파일

#### 작업 순서:
1. [ ] **우선순위 파일 처리** (ASCR 모듈 중심)
   ```bash
   # ASCR 모듈 우선 처리
   python scripts/convert_os_path.py backend/app/services/ascr/src/common/file_utils.py
   python scripts/convert_os_path.py backend/app/services/ascr/src/common/pdf_utils.py
   ```

2. [ ] **핵심 모듈 처리**
   ```bash
   # 백엔드 핵심 모듈
   python scripts/convert_os_path.py backend/app/core/
   python scripts/convert_os_path.py backend/app/utils/
   python scripts/convert_os_path.py backend/app/models/
   ```

3. [ ] **데스크톱 앱 처리**
   ```bash
   # 데스크톱 앱 모듈
   python scripts/convert_os_path.py desktop/
   ```

4. [ ] **전체 프로젝트 일괄 처리**
   ```bash
   # 전체 프로젝트에서 os.path 사용 파일 변환
   python scripts/convert_os_path.py
   ```

#### 검증 방법:
- [ ] 변환된 파일에서 `os.path.` 사용 여부 확인
- [ ] `from pathlib import Path` import 확인
- [ ] 경로 처리 로직 정상 작동 확인

### 1.2 라인 엔딩 처리 추가
**예상 소요시간**: 2-3시간  
**대상 파일**: 381개 파일

#### 작업 순서:
1. [ ] **인코딩 사용 파일 처리**
   ```bash
   # 인코딩을 사용하는 파일들에 newline='' 추가
   python scripts/add_newline.py
   ```

2. [ ] **open() 함수 사용 파일 처리**
   ```bash
   # 모든 open() 함수에 newline='' 추가
   python scripts/add_newline.py
   ```

#### 검증 방법:
- [ ] `open()` 함수에 `newline=''` 파라미터 추가 확인
- [ ] 파일 읽기/쓰기 시 라인 엔딩 문제 없음 확인

---

## 🟡 2단계: 단계적 개선 작업 (중간 우선순위)

### 2.1 환경 변수 활용 확대
**예상 소요시간**: 1-2시간

#### 작업 순서:
1. [ ] **설정 파일 업데이트**
   ```python
   # backend/app/core/config.py 업데이트
   # 환경 변수 활용 확대
   ```

2. [ ] **플랫폼 유틸리티 적용**
   ```python
   # backend/app/utils/platform_utils.py 활용
   # 모든 모듈에서 플랫폼별 설정 사용
   ```

### 2.2 플랫폼별 조건부 코드 확대
**예상 소요시간**: 2-3시간

#### 작업 순서:
1. [ ] **주요 모듈에 플랫폼 감지 추가**
   ```python
   # platform.system() 사용 확대
   # Windows/Linux/macOS별 분기 처리
   ```

2. [ ] **파일 경로 처리 개선**
   ```python
   # 플랫폼별 경로 구분자 처리
   # 임시 디렉토리 경로 처리
   ```

---

## 🟢 3단계: 검증 및 테스트

### 3.1 크로스 플랫폼 테스트
**예상 소요시간**: 1-2시간

#### 테스트 항목:
1. [ ] **경로 처리 테스트**
   ```bash
   # Windows 경로 처리 테스트
   python -c "from pathlib import Path; print(Path('test', 'file.txt'))"
   ```

2. [ ] **파일 읽기/쓰기 테스트**
   ```bash
   # UTF-8 인코딩 테스트
   python -c "Path('test.txt').write_text('한글 테스트', encoding='utf-8')"
   ```

3. [ ] **플랫폼 감지 테스트**
   ```bash
   # 플랫폼 정보 출력 테스트
   python backend/app/utils/platform_utils.py
   ```

### 3.2 기능 테스트
**예상 소요시간**: 2-3시간

#### 테스트 항목:
1. [ ] **백엔드 API 테스트**
   ```bash
   # FastAPI 서버 실행 및 테스트
   cd backend
   uvicorn app.main:app --reload
   ```

2. [ ] **ASCR 모듈 테스트**
   ```bash
   # PDF 처리 기능 테스트
   python backend/app/services/ascr/main.py
   ```

3. [ ] **데스크톱 앱 테스트**
   ```bash
   # PySide6 앱 실행 테스트
   cd desktop
   python main.py
   ```

---

## 📊 작업 진행 상황 추적

### 시간별 진행 상황:
- **09:00-10:00**: 환경 설정 및 준비
- **10:00-12:00**: os.path → pathlib.Path 전환 (1차)
- **12:00-13:00**: 점심 시간
- **13:00-15:00**: os.path → pathlib.Path 전환 (2차)
- **15:00-16:00**: 라인 엔딩 처리 추가
- **16:00-17:00**: 환경 변수 활용 확대
- **17:00-18:00**: 플랫폼별 조건부 코드 확대
- **18:00-19:00**: 검증 및 테스트

### 완료 기준:
- [ ] 모든 Python 파일에서 `os.path.` 사용 제거
- [ ] 모든 `open()` 함수에 `newline=''` 추가
- [ ] 플랫폼별 조건부 코드 적용
- [ ] 크로스 플랫폼 테스트 통과
- [ ] 기능 테스트 통과

---

## 🚨 주의사항

### 1. 백업 및 버전 관리
- [ ] 작업 시작 전 `git stash` 또는 브랜치 생성
- [ ] 각 단계별로 커밋 생성
- [ ] 문제 발생 시 롤백 가능하도록 준비

### 2. 테스트 우선
- [ ] 변경 전후 기능 테스트 필수
- [ ] 각 파일 변환 후 개별 테스트
- [ ] 전체 시스템 통합 테스트

### 3. 문서화
- [ ] 변경사항 문서화
- [ ] 새로운 규칙 적용 사례 기록
- [ ] 문제 해결 과정 기록

---

## 📞 문제 발생 시 대응

### 1. 스크립트 오류
```bash
# 스크립트 디버깅
python -c "import scripts.convert_os_path; print('스크립트 로드 성공')"
```

### 2. 변환 실패
```bash
# 개별 파일 수동 변환
# 문제 파일 백업 후 수동 수정
```

### 3. 테스트 실패
```bash
# 단계별 롤백
git log --oneline -5  # 최근 커밋 확인
git reset --hard HEAD~1  # 필요시 롤백
```

---

## 🎉 완료 후 확인사항

### 1. 코드 품질
- [ ] 모든 파일에서 `pathlib.Path` 사용
- [ ] 모든 `open()` 함수에 `newline=''` 추가
- [ ] 플랫폼별 조건부 코드 적용

### 2. 기능 정상성
- [ ] 백엔드 API 정상 작동
- [ ] ASCR 모듈 정상 작동
- [ ] 데스크톱 앱 정상 작동

### 3. 크로스 플랫폼 호환성
- [ ] Windows에서 정상 작동
- [ ] Linux에서 정상 작동
- [ ] macOS에서 정상 작동 (가능시)

### 4. 문서 업데이트
- [ ] 변경사항 문서화 완료
- [ ] 새로운 규칙 적용 사례 기록
- [ ] 팀원들과 공유

---

**작업 완료 후**: `git add . && git commit -m "feat: 크로스 플랫폼 호환성 개선 완료" && git push` 