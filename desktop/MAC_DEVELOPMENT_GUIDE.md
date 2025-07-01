# Mac에서 CMA GUI 개발 환경 설정 가이드

## 🍎 Mac 환경에서 GUI 개발하기

### **장점**
- **네이티브 GUI 지원**: X 서버 없이도 PySide6 GUI가 바로 뜸
- **한글 폰트 자동 지원**: macOS 기본 한글 폰트 사용
- **성능 최적화**: 네이티브 환경에서 최고 성능
- **배포 테스트**: 실제 Mac 사용자 환경과 동일

---

## 🚀 1단계: 기본 환경 설정

### Python 설치 확인
```bash
# Python 3.12+ 설치 확인
python3 --version

# Homebrew로 Python 설치 (필요시)
brew install python@3.12
```

### 프로젝트 클론
```bash
# GitHub에서 프로젝트 클론
git clone https://github.com/Dydiddl/CMA.git
cd CMA/desktop
```

---

## 🛠 2단계: 가상환경 설정

### 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# Python 경로 확인
which python
# → /path/to/CMA/desktop/venv/bin/python
```

### 의존성 설치
```bash
# 의존성 설치
pip install -r requirements.txt

# 설치 확인
pip list | grep -E "(PySide6|SQLAlchemy|pandas)"
```

---

## 🎨 3단계: 한글 폰트 설정

### macOS 기본 한글 폰트 사용
Mac에서는 기본적으로 한글 폰트가 잘 지원되므로, 추가 설치 없이 바로 사용 가능합니다.

### 커스텀 폰트 설치 (선택사항)
```bash
# Homebrew로 폰트 관리자 설치
brew install fontforge

# D2Coding 폰트 설치 (개발자용)
# 1. https://github.com/naver/d2codingfont 에서 다운로드
# 2. Font Book 앱에서 설치
# 3. 또는 터미널에서:
# cp D2Coding.ttf ~/Library/Fonts/
```

---

## 🖥 4단계: GUI 실행

### 기본 실행
```bash
# GUI 모드로 실행
python main.py
```

### 콘솔 모드 실행 (백엔드만 테스트)
```bash
# 콘솔 모드로 실행
python main.py --console
```

### 디버그 모드 실행
```bash
# 디버그 정보와 함께 실행
QT_DEBUG_PLUGINS=1 python main.py
```

---

## 🔧 5단계: 개발 워크플로우

### 실시간 개발
1. **GUI 실행**: `python main.py`
2. **코드 수정**: 에디터에서 파일 수정
3. **GUI 확인**: 수정사항이 바로 반영되는지 확인
4. **반복**: 기능 완성까지 반복

### 테스트
```bash
# 단위 테스트 (필요시)
pytest tests/

# GUI 테스트
# → 수동으로 모든 기능 테스트
```

---

## 📦 6단계: Mac용 배포 파일 생성

### Mac app 파일 생성
```bash
# 배포용 app 파일 생성
python build_exe.py

# 생성된 파일 확인
ls -la dist/
# → CMA_Construction_Manager (실행 파일)
```

### 앱 번들 생성 (고급)
```bash
# PyInstaller로 앱 번들 생성
pyinstaller --onedir --windowed --name="CMA" main.py

# 생성된 앱 번들 확인
ls -la dist/CMA.app/
```

---

## 🐛 7단계: 문제 해결

### GUI가 안 뜨는 경우
```bash
# 1. PySide6 설치 확인
pip show PySide6

# 2. Qt 플러그인 확인
python -c "from PySide6.QtWidgets import QApplication; print('Qt OK')"

# 3. 디버그 모드로 실행
QT_DEBUG_PLUGINS=1 python main.py
```

### 한글이 깨지는 경우
```bash
# 1. 로케일 확인
locale

# 2. 폰트 확인
fc-list | grep -i korean

# 3. 환경변수 설정
export LANG=ko_KR.UTF-8
export LC_ALL=ko_KR.UTF-8
```

### 성능 문제
```bash
# 1. 메모리 사용량 확인
ps aux | grep python

# 2. CPU 사용량 확인
top -pid $(pgrep python)

# 3. 프로파일링 (필요시)
python -m cProfile -o profile.stats main.py
```

---

## 🎯 8단계: 최적화

### Mac 특화 최적화
```python
# main.py에 Mac 최적화 코드 추가
import platform

if platform.system() == "Darwin":
    # Mac 특화 설정
    os.environ['QT_MAC_WANTS_LAYER'] = '1'  # Metal 렌더링 사용
    os.environ['QT_QPA_PLATFORM'] = 'cocoa'  # Cocoa 플랫폼 사용
```

### 성능 모니터링
```bash
# Activity Monitor로 성능 확인
open -a "Activity Monitor"

# 또는 터미널에서
top -pid $(pgrep python)
```

---

## 📋 9단계: 체크리스트

### 초기 설정
- [ ] Python 3.12+ 설치 확인
- [ ] 프로젝트 클론 완료
- [ ] 가상환경 생성 및 활성화
- [ ] 의존성 설치 완료
- [ ] GUI 실행 확인
- [ ] 한글 표시 확인

### 개발 준비
- [ ] 에디터 설정 (VS Code, PyCharm 등)
- [ ] 디버거 설정
- [ ] Git 설정
- [ ] 테스트 환경 준비

### 배포 준비
- [ ] Mac app 파일 생성 성공
- [ ] 다른 Mac에서 테스트
- [ ] 사용자 매뉴얼 작성
- [ ] App Store 배포 준비 (선택사항)

---

## 🚀 10단계: 고급 기능

### 코드 서명 (배포용)
```bash
# 개발자 인증서로 코드 서명
codesign --force --deep --sign "Developer ID Application: Your Name" dist/CMA_Construction_Manager

# 공증 (App Store 배포용)
xcrun altool --notarize-app --primary-bundle-id "com.yourcompany.cma" --username "your@email.com" --password "@env:APP_PASSWORD" --file dist/CMA_Construction_Manager
```

### 자동화 스크립트
```bash
# 개발용 실행 스크립트 생성
cat > run_dev.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
export LANG=ko_KR.UTF-8
export LC_ALL=ko_KR.UTF-8
python main.py
EOF

chmod +x run_dev.sh
```

---

## 💡 팁

### 1. **터미널 설정**
```bash
# .zshrc에 추가
export LANG=ko_KR.UTF-8
export LC_ALL=ko_KR.UTF-8
alias cma="cd ~/CMA/desktop && source venv/bin/activate && python main.py"
```

### 2. **에디터 설정**
- **VS Code**: Python 확장, PySide6 지원
- **PyCharm**: GUI 디자이너 내장
- **Xcode**: Interface Builder 사용 가능

### 3. **디버깅**
```bash
# 디버그 모드 실행
python -m pdb main.py

# 또는 IDE 디버거 사용
```

---

## 🎯 다음 단계

1. **GUI 완성**: 메인 윈도우, 메뉴, 툴바 구현
2. **기능 구현**: 계약 관리, 재무 관리, 노무 관리
3. **백엔드 연동**: API 서버와 통신
4. **Mac 최적화**: Metal 렌더링, 터치바 지원 등
5. **App Store 배포**: Mac App Store 등록 (선택사항)

---

## 📞 지원

문제가 발생하면:
1. **로그 확인**: `python main.py` 실행 시 오류 메시지
2. **환경 확인**: Python 버전, 의존성 설치 상태
3. **GitHub 이슈**: 프로젝트 저장소에 이슈 등록
4. **커뮤니티**: Python, PySide6 커뮤니티 활용 