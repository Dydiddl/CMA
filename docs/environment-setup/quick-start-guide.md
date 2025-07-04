# 🚀 D 드라이브 WSL2 환경 설정 - 빠른 시작 가이드

## 📋 개요

이 가이드는 **D 드라이브(1TB SSD)에 WSL2를 설치하여 CMA 프로젝트 개발 환경을 구축**하는 방법을 단계별로 설명합니다.

### 🎯 목표
- ✅ **1TB SSD 전체 활용** (빠른 성능)
- ✅ **Windows + Linux 동시 사용**
- ✅ **충분한 용량** (여러 프로젝트 개발)
- ✅ **VS Code/Cursor 완벽 연동**

---

## 🛠️ 1단계: Windows 환경 설정

### 1.1 PowerShell 관리자 권한으로 실행
```powershell
# Windows 키 + X → "Windows PowerShell (관리자)"
# 또는 Windows 키 + R → "powershell" → Ctrl + Shift + Enter
```

### 1.2 자동 설정 스크립트 실행
```powershell
# CMA 프로젝트 폴더로 이동
cd "D:\Projects\CMA"

# PowerShell 스크립트 실행
.\scripts\setup-d-drive-wsl2.ps1
```

### 1.3 수동 설정 (스크립트 실패 시)

#### WSL2 기능 활성화
```powershell
# WSL 기능 활성화
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 재부팅 후
wsl --set-default-version 2
```

#### Ubuntu 설치
```powershell
# Ubuntu 설치
wsl --install -d Ubuntu

# 또는 Microsoft Store에서 Ubuntu 설치
```

#### WSL2 설정 최적화
```powershell
# .wslconfig 파일 생성 (C:\Users\[사용자명]\.wslconfig)
[wsl2]
memory=8GB
processors=4
swap=2GB
swapFile=D:\WSL\swap.vhdx
localhostForwarding=true
pageReporting=false
```

---

## 🐧 2단계: Ubuntu 환경 설정

### 2.1 WSL2 Ubuntu 실행
```bash
# Windows에서
wsl -d Ubuntu

# 또는 Windows Terminal에서 Ubuntu 탭 선택
```

### 2.2 자동 설정 스크립트 실행
```bash
# CMA 프로젝트 폴더로 이동
cd /mnt/d/Projects/CMA

# 실행 권한 부여
chmod +x scripts/setup-d-drive-wsl2.sh

# 스크립트 실행
./scripts/setup-d-drive-wsl2.sh
```

### 2.3 수동 설정 (스크립트 실패 시)

#### 기본 도구 설치
```bash
# 패키지 업데이트
sudo apt update

# 기본 도구 설치
sudo apt install -y git curl wget build-essential python3 python3-pip python3-venv
```

#### Node.js 설치
```bash
# Node.js 18.x 설치
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 버전 확인
node --version
npm --version
```

#### PostgreSQL 설치
```bash
# PostgreSQL 설치
sudo apt install -y postgresql postgresql-contrib

# 서비스 시작
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 기본 데이터베이스 생성
sudo -u postgres createdb cma_db
```

#### Redis 설치
```bash
# Redis 설치
sudo apt install -y redis-server

# 서비스 시작
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

---

## 📁 3단계: 프로젝트 구조 설정

### 3.1 폴더 구조 생성
```bash
# 홈 디렉토리에 폴더 생성
mkdir -p ~/projects
mkdir -p ~/venvs
mkdir -p ~/data
mkdir -p ~/logs
mkdir -p ~/backups
```

### 3.2 CMA 프로젝트 클론
```bash
# 프로젝트 클론
cd ~/projects
git clone [CMA_GIT_REPOSITORY_URL] CMA

# 또는 기존 프로젝트 복사
cp -r /mnt/d/Projects/CMA ~/projects/
```

### 3.3 가상환경 설정
```bash
# 백엔드 가상환경
cd ~/projects/CMA/backend
python3 -m venv ~/venvs/backend_venv
source ~/venvs/backend_venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# 데스크탑 가상환경
cd ~/projects/CMA/desktop
python3 -m venv ~/venvs/desktop_venv
source ~/venvs/desktop_venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
```

### 3.4 프론트엔드 설정
```bash
# 프론트엔드 의존성 설치
cd ~/projects/CMA/frontend
npm install
```

---

## 🔧 4단계: VS Code/Cursor 연동

### 4.1 WSL 확장 설치
1. VS Code/Cursor 실행
2. 확장 마켓플레이스에서 "WSL" 검색
3. "WSL" 확장 설치

### 4.2 WSL에서 프로젝트 열기
```bash
# WSL Ubuntu에서
cd ~/projects/CMA
code .
```

### 4.3 Python 인터프리터 설정
1. `Ctrl + Shift + P` → "Python: Select Interpreter"
2. `~/venvs/backend_venv/bin/python` 선택

### 4.4 권장 확장 프로그램 설치
```bash
# VS Code/Cursor에서 자동 설치
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
code --install-extension ms-vscode.vscode-json
code --install-extension bradlc.vscode-tailwindcss
code --install-extension esbenp.prettier-vscode
```

---

## 🚀 5단계: 개발 환경 테스트

### 5.1 백엔드 서버 테스트
```bash
# 백엔드 가상환경 활성화
source ~/venvs/backend_venv/bin/activate
cd ~/projects/CMA/backend

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5.2 프론트엔드 서버 테스트
```bash
# 새 터미널에서
cd ~/projects/CMA/frontend

# 개발 서버 실행
npm run dev
```

### 5.3 브라우저에서 확인
- 백엔드: http://localhost:8000
- 프론트엔드: http://localhost:3000

---

## 📝 6단계: 환경 변수 및 별칭 설정

### 6.1 환경 변수 설정
```bash
# .bashrc에 추가
echo 'export CMA_PROJECT_ROOT="$HOME/projects/CMA"' >> ~/.bashrc
echo 'export CMA_VENV_ROOT="$HOME/venvs"' >> ~/.bashrc
echo 'export CMA_DATA_ROOT="$HOME/data"' >> ~/.bashrc
echo 'export CMA_LOG_ROOT="$HOME/logs"' >> ~/.bashrc
echo 'export PYTHONPATH="$CMA_PROJECT_ROOT/backend:$PYTHONPATH"' >> ~/.bashrc
```

### 6.2 유용한 별칭 설정
```bash
# .bashrc에 추가
echo 'alias cma-backend="source $HOME/venvs/backend_venv/bin/activate && cd $HOME/projects/CMA/backend"' >> ~/.bashrc
echo 'alias cma-desktop="source $HOME/venvs/desktop_venv/bin/activate && cd $HOME/projects/CMA/desktop"' >> ~/.bashrc
echo 'alias cma-frontend="cd $HOME/projects/CMA/frontend"' >> ~/.bashrc
echo 'alias cma-status="echo \"=== CMA 프로젝트 상태 ===\" && ps aux | grep -E \"(uvicorn|fastapi|vite|npm)\" | grep -v grep"' >> ~/.bashrc

# 환경 변수 적용
source ~/.bashrc
```

---

## 🔍 7단계: 문제 해결

### 7.1 WSL2 관련 문제

#### WSL2가 시작되지 않는 경우
```powershell
# Windows에서
wsl --shutdown
wsl --update
wsl -d Ubuntu
```

#### 메모리 부족 문제
```powershell
# .wslconfig 파일 수정
memory=4GB  # 메모리 사용량 줄이기
```

### 7.2 포트 포워딩 문제

#### 포트가 사용 중인 경우
```powershell
# Windows에서 포트 확인
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# 프로세스 종료
taskkill /PID [프로세스ID] /F
```

#### 포트 포워딩 재설정
```powershell
# 기존 포트 포워딩 제거
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0
netsh interface portproxy delete v4tov4 listenport=3000 listenaddress=0.0.0.0

# 새로운 포트 포워딩 설정
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=localhost
netsh interface portproxy add v4tov4 listenport=3000 listenaddress=0.0.0.0 connectport=3000 connectaddress=localhost
```

### 7.3 가상환경 문제

#### 가상환경이 활성화되지 않는 경우
```bash
# 가상환경 재생성
rm -rf ~/venvs/backend_venv
python3 -m venv ~/venvs/backend_venv
source ~/venvs/backend_venv/bin/activate
pip install -r requirements.txt
```

#### 패키지 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip

# 캐시 정리
pip cache purge

# 강제 재설치
pip install --force-reinstall -r requirements.txt
```

---

## 📊 8단계: 성능 최적화

### 8.1 WSL2 성능 최적화
```powershell
# .wslconfig 파일 최적화
[wsl2]
memory=8GB
processors=4
swap=2GB
swapFile=D:\WSL\swap.vhdx
localhostForwarding=true
pageReporting=false
nestedVirtualization=true
```

### 8.2 Ubuntu 성능 최적화
```bash
# 불필요한 서비스 비활성화
sudo systemctl disable snapd
sudo systemctl disable snapd.socket

# 스왑 파일 생성
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 영구 설정
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 8.3 개발 도구 최적화
```bash
# Git 설정 최적화
git config --global core.preloadindex true
git config --global core.fscache true
git config --global pack.threads 0

# npm 캐시 최적화
npm config set cache ~/.npm-cache --global
```

---

## 🎯 9단계: 개발 워크플로우

### 9.1 일일 개발 시작
```bash
# 1. WSL2 Ubuntu 실행
wsl -d Ubuntu

# 2. 백엔드 개발 환경
cma-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. 새 터미널에서 프론트엔드 개발 환경
cma-frontend
npm run dev
```

### 9.2 프로젝트 상태 확인
```bash
# 프로젝트 상태 확인
cma-status

# 서비스 상태 확인
sudo systemctl status postgresql
sudo systemctl status redis-server
```

### 9.3 백업 및 복원
```bash
# 프로젝트 백업
cp -r ~/projects/CMA ~/backups/CMA_$(date +%Y%m%d_%H%M%S)

# 가상환경 백업
cp -r ~/venvs ~/backups/venvs_$(date +%Y%m%d_%H%M%S)
```

---

## 📚 10단계: 추가 리소스

### 10.1 유용한 명령어
```bash
# WSL 관리
wsl --list --verbose          # WSL 배포판 목록
wsl --shutdown               # WSL 종료
wsl --update                 # WSL 업데이트

# 프로젝트 관리
cma-backend                  # 백엔드 개발 환경
cma-desktop                  # 데스크탑 개발 환경
cma-frontend                 # 프론트엔드 개발 환경
cma-status                   # 프로젝트 상태 확인

# 시스템 모니터링
htop                         # 시스템 리소스 모니터링
df -h                        # 디스크 사용량 확인
free -h                      # 메모리 사용량 확인
```

### 10.2 문서 참조
- [상세 설정 가이드](D-drive-wsl2-setup.md)
- [문제 해결 가이드](troubleshooting.md)
- [성능 최적화 가이드](performance-optimization.md)

### 10.3 지원 및 문의
- GitHub Issues: [CMA 프로젝트 이슈](https://github.com/your-repo/CMA/issues)
- 문서 업데이트: `docs/environment-setup/` 폴더

---

## 🎉 완료!

축하합니다! D 드라이브 WSL2 환경 설정이 완료되었습니다.

### 다음 단계:
1. **개발 시작**: `cma-backend` 또는 `cma-frontend` 명령어로 개발 환경 시작
2. **문서 학습**: CMA 프로젝트 문서 읽기
3. **첫 번째 기능 개발**: 간단한 기능부터 시작

### 유지보수:
- 정기적으로 WSL2 업데이트
- 가상환경 패키지 업데이트
- 시스템 성능 모니터링

**즐거운 개발 되세요! 🚀** 