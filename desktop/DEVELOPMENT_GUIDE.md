# CMA 데스크톱 애플리케이션 개발 가이드

## 🎯 목표
- **개발자**: GUI를 직접 보면서 개발/테스트/개선
- **최종 사용자**: exe/app 설치 → 바로 실행 (개발 지식 불필요)
- **플랫폼**: Windows/Mac 우선 (Linux 배제)
- **라이선스**: 무료 우선, 유료 전환 가능성 열어둠

## 🚀 개발 환경 설정

### 1. WSL2에서 GUI 개발 (권장)

#### Windows에서 X 서버 설치
1. **VcXsrv 설치** (무료)
   - https://sourceforge.net/projects/vcxsrv/ 에서 다운로드
   - 설치 후 실행: `XLaunch`
   - 설정: "Disable access control" 체크

2. **X410 설치** (유료, 더 안정적)
   - Microsoft Store에서 "X410" 검색
   - 설치 후 실행

#### WSL2에서 GUI 실행
```bash
# WSL2에서 DISPLAY 설정
export DISPLAY=localhost:0.0
# 또는
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

# GUI 실행
cd desktop
./run_gui.sh
```

### 2. 네이티브 환경에서 개발

#### Windows
```bash
# 가상환경 생성
python -m venv venv
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# GUI 실행
python main.py
```

#### Mac
```bash
# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# GUI 실행
python main.py
```

## 📦 배포용 빌드

### Windows exe 파일 생성
```bash
# Windows에서 실행
python build_exe.py
```

### Mac app 파일 생성
```bash
# Mac에서 실행
python build_exe.py
```

### Docker 빌드 (선택사항)
```bash
# Docker 이미지 빌드
docker build -t cma-desktop .

# Docker에서 GUI 실행 (X 서버 필요)
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  cma-desktop
```

## 🛠 개발 워크플로우

### 1. 기능 개발
1. **GUI 직접 확인**: `python main.py`로 GUI 실행
2. **실시간 테스트**: 코드 수정 → GUI에서 바로 확인
3. **사용성 검토**: 실제 사용자 관점에서 UI/UX 검토

### 2. 테스트
1. **단위 테스트**: `pytest tests/`
2. **GUI 테스트**: 수동으로 모든 기능 테스트
3. **크로스 플랫폼 테스트**: Windows/Mac에서 각각 테스트

### 3. 배포
1. **빌드**: `python build_exe.py`
2. **테스트**: 생성된 exe/app 파일 실행 테스트
3. **배포**: 사용자에게 exe/app 파일 제공

## 📁 프로젝트 구조

```
desktop/
├── main.py                 # 메인 애플리케이션
├── run_gui.sh             # WSL2 GUI 실행 스크립트
├── build_exe.py           # 배포용 빌드 스크립트
├── Dockerfile             # Docker 설정
├── requirements.txt       # Python 의존성
├── config.json           # 설정 파일
├── core/                 # 핵심 모듈
│   ├── database.py       # 데이터베이스 관리
│   ├── config.py         # 설정 관리
│   └── exceptions.py     # 예외 처리
├── ui/                   # UI 모듈
│   ├── main_window.py    # 메인 윈도우
│   └── widgets/          # 커스텀 위젯
├── utils/                # 유틸리티
│   └── logger.py         # 로깅
└── assets/               # 리소스 파일
    ├── icon.ico          # Windows 아이콘
    └── icon.icns         # Mac 아이콘
```

## 🔧 설정 및 환경 변수

### 환경 변수
- `QT_QPA_PLATFORM`: Qt 플랫폼 (xcb, offscreen)
- `DISPLAY`: X 서버 연결 (WSL2)
- `LANG`: 로케일 설정 (ko_KR.UTF-8)

### 설정 파일 (config.json)
```json
{
  "database": {
    "url": "sqlite:///cma_desktop.db",
    "echo": false
  },
  "api": {
    "base_url": "http://localhost:8000",
    "timeout": 30
  },
  "ui": {
    "theme": "light",
    "language": "ko",
    "window_size": [1400, 900]
  },
  "logging": {
    "level": "INFO",
    "file": "cma_desktop.log"
  }
}
```

## 🐛 문제 해결

### GUI가 안 뜨는 경우
1. **WSL2**: X 서버 실행 확인, DISPLAY 환경변수 설정
2. **Windows**: PySide6 설치 확인, 그래픽 드라이버 업데이트
3. **Mac**: XQuartz 설치 확인

### 한글이 깨지는 경우
1. **폰트 설치**: D2Coding, JetBrains Mono 설치
2. **로케일 설정**: `LANG=ko_KR.UTF-8`
3. **Qt 설정**: `QT_QPA_PLATFORM=xcb`

### 빌드 실패하는 경우
1. **PyInstaller 설치**: `pip install pyinstaller`
2. **의존성 확인**: `pip install -r requirements.txt`
3. **권한 확인**: 관리자 권한으로 실행

## 📋 체크리스트

### 개발 시작 전
- [ ] 가상환경 생성 및 활성화
- [ ] 의존성 설치 완료
- [ ] GUI 실행 확인
- [ ] 한글 폰트 설정 확인

### 기능 개발 중
- [ ] GUI에서 직접 테스트
- [ ] 사용성 검토 완료
- [ ] 오류 처리 추가
- [ ] 로깅 추가

### 배포 전
- [ ] 모든 기능 테스트 완료
- [ ] exe/app 파일 빌드 성공
- [ ] 빌드된 파일 실행 테스트
- [ ] 사용자 매뉴얼 작성

## 🎯 다음 단계

1. **GUI 완성**: 메인 윈도우, 메뉴, 툴바 구현
2. **기능 구현**: 계약 관리, 재무 관리, 노무 관리
3. **백엔드 연동**: API 서버와 통신
4. **배포 준비**: 설치 프로그램, 사용자 가이드
5. **성능 최적화**: 로딩 시간, 메모리 사용량 개선 