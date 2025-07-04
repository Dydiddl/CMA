# 🚀 D 드라이브 WSL2 개발 환경 설정 가이드

## 📋 목차
1. [개요](#개요)
2. [시스템 요구사항](#시스템-요구사항)
3. [WSL2 설치 및 설정](#wsl2-설치-및-설정)
4. [Ubuntu 설치 (D 드라이브)](#ubuntu-설치-d-드라이브)
5. [개발 환경 설정](#개발-환경-설정)
6. [CMA 프로젝트 설정](#cma-프로젝트-설정)
7. [VS Code/Cursor 연동](#vs-codecursor-연동)
8. [성능 최적화](#성능-최적화)
9. [문제 해결](#문제-해결)
10. [유지보수](#유지보수)

---

## 🎯 개요

이 문서는 **D 드라이브(1TB SSD)에 WSL2를 설치하여 CMA 프로젝트 개발 환경을 구축**하는 방법을 설명합니다.

### 장점
- ✅ **1TB SSD 전체 활용** (빠른 성능)
- ✅ **Windows + Linux 동시 사용**
- ✅ **충분한 용량** (여러 프로젝트 개발)
- ✅ **VS Code/Cursor 완벽 연동**
- ✅ **유연한 개발 환경**

### 시스템 구성
```
C 드라이브 (500GB SSD): Windows 시스템
D 드라이브 (1TB SSD): WSL2 + 개발 환경
```

---

## 💻 시스템 요구사항

### 최소 요구사항
- **Windows 10 버전 2004 이상** 또는 **Windows 11**
- **8GB RAM** (16GB 권장)
- **D 드라이브 50GB 이상 여유 공간**
- **가상화 지원** (BIOS에서 VT-x/AMD-V 활성화)

### 권장 사양
- **Windows 11**
- **16GB RAM**
- **D 드라이브 100GB 이상 여유 공간**
- **SSD (성능 향상)**

---

## 🔧 WSL2 설치 및 설정

### 1단계: Windows 기능 활성화

#### PowerShell 관리자 권한으로 실행
```powershell
# WSL 기능 활성화
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 가상 머신 플랫폼 활성화
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 시스템 재부팅
Restart-Computer
```

#### 재부팅 후 WSL2 설정
```powershell
# WSL2를 기본 버전으로 설정
wsl --set-default-version 2

# 현재 WSL 상태 확인
wsl --list --verbose
```

### 2단계: WSL2 커널 업데이트

#### Microsoft Store에서 업데이트
1. **Microsoft Store** 열기
2. **"Windows Subsystem for Linux"** 검색
3. **업데이트** 클릭

#### 또는 수동 다운로드
```powershell
# WSL2 커널 업데이트 패키지 다운로드
# https://aka.ms/wsl2kernel
# 다운로드 후 설치
```

---

## 🐧 Ubuntu 설치 (D 드라이브)

### 1단계: D 드라이브에 WSL 설치

#### 방법 1: 직접 설치 (권장)
```powershell
# D 드라이브에 Ubuntu 설치
wsl --install -d Ubuntu -d D:\WSL

# 설치 확인
wsl --list --verbose
```

#### 방법 2: 기존 설치 이동
```powershell
# 기존 Ubuntu가 있다면 D 드라이브로 이동
wsl --export Ubuntu D:\WSL\ubuntu-backup.tar
wsl --unregister Ubuntu
wsl --import Ubuntu D:\WSL D:\WSL\ubuntu-backup.tar --version 2
```

### 2단계: Ubuntu 초기 설정

#### WSL2 Ubuntu 실행
```bash
# Ubuntu 실행
wsl -d Ubuntu

# 또는 Windows Terminal에서 Ubuntu 탭 선택
```

#### 사용자 계정 설정
```bash
# Ubuntu 내부에서
sudo apt update && sudo apt upgrade

# 사용자 이름 설정 (선택사항)
sudo usermod -l your-username $USER
```

---

## 🛠️ 개발 환경 설정

### 1단계: 기본 도구 설치

#### 시스템 업데이트
```bash
# 패키지 목록 업데이트
sudo apt update && sudo apt upgrade -y

# 기본 도구 설치
sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release
```

#### Python 환경 설정
```bash
# Python 3 설치 (기본 포함)
sudo apt install -y python3 python3-pip python3-venv

# Python 버전 확인
python3 --version
pip3 --version

# pip 업그레이드
python3 -m pip install --upgrade pip
```

#### Node.js 설치
```bash
# Node.js 18.x 저장소 추가
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# Node.js 설치
sudo apt install -y nodejs

# 버전 확인
node --version
npm --version

# npm 업그레이드
sudo npm install -g npm@latest
```

### 2단계: 데이터베이스 설치

#### PostgreSQL 설치
```bash
# PostgreSQL 설치
sudo apt install -y postgresql postgresql-contrib

# 서비스 시작
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 상태 확인
sudo systemctl status postgresql

# 사용자 설정
sudo -u postgres createuser --interactive
sudo -u postgres createdb cma_db
```

#### Redis 설치
```bash
# Redis 설치
sudo apt install -y redis-server

# 서비스 시작
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 상태 확인
sudo systemctl status redis-server
```

### 3단계: 개발 도구 설치

#### 추가 도구 설치
```bash
# 개발 도구 설치
sudo apt install -y \
    htop \
    tree \
    vim \
    nano \
    unzip \
    zip \
    jq \
    httpie \
    tmux

# Git 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

---

## 📁 CMA 프로젝트 설정

### 1단계: 프로젝트 폴더 구조 생성

#### 폴더 구조 생성
```bash
# 홈 디렉토리로 이동
cd ~

# 프로젝트 폴더 생성
mkdir -p projects
mkdir -p venvs
mkdir -p data
mkdir -p logs

# 폴더 구조 확인
tree -L 2
```

#### 예상 폴더 구조
```
/home/$USER/
├── projects/
│   └── CMA/                 # CMA 프로젝트
├── venvs/
│   ├── backend_venv/        # 백엔드 가상환경
│   └── desktop_venv/        # 데스크탑 가상환경
├── data/
│   ├── postgresql/          # PostgreSQL 데이터
│   └── redis/               # Redis 데이터
└── logs/                    # 로그 파일들
```

### 2단계: CMA 프로젝트 클론

#### 프로젝트 다운로드
```bash
# 프로젝트 폴더로 이동
cd ~/projects

# Git 저장소 클론
git clone [repository-url] CMA

# 프로젝트 폴더로 이동
cd CMA

# 프로젝트 구조 확인
ls -la
```

### 3단계: 가상환경 설정

#### 백엔드 가상환경 설정
```bash
# 백엔드 폴더로 이동
cd ~/projects/CMA/backend

# 가상환경 생성
python3 -m venv ~/venvs/backend_venv

# 가상환경 활성화
source ~/venvs/backend_venv/bin/activate

# pip 업그레이드
pip install --upgrade pip

# 의존성 설치
pip install -r requirements.txt

# 가상환경 비활성화
deactivate
```

#### 데스크탑 가상환경 설정
```bash
# 데스크탑 폴더로 이동
cd ~/projects/CMA/desktop

# 가상환경 생성
python3 -m venv ~/venvs/desktop_venv

# 가상환경 활성화
source ~/venvs/desktop_venv/bin/activate

# pip 업그레이드
pip install --upgrade pip

# 의존성 설치
pip install -r requirements.txt

# 가상환경 비활성화
deactivate
```

### 4단계: 프론트엔드 설정

#### Node.js 의존성 설치
```bash
# 프론트엔드 폴더로 이동
cd ~/projects/CMA/frontend

# 의존성 설치
npm install

# 개발 서버 테스트
npm run dev
```

---

## 🔗 VS Code/Cursor 연동

### 1단계: WSL 확장 설치

#### VS Code/Cursor에서 확장 설치
1. **VS Code/Cursor** 열기
2. **확장(Extensions)** 탭 열기
3. **"WSL"** 검색
4. **"WSL"** 확장 설치

### 2단계: WSL에서 프로젝트 열기

#### WSL 터미널에서 VS Code 실행
```bash
# CMA 프로젝트 폴더로 이동
cd ~/projects/CMA

# VS Code 실행
code .

# 또는 Cursor 실행
cursor .
```

#### 또는 VS Code/Cursor에서 직접 열기
1. **VS Code/Cursor** 열기
2. **File > Open Folder**
3. **WSL: Ubuntu** 선택
4. **/home/$USER/projects/CMA** 폴더 선택

### 3단계: Python 인터프리터 설정

#### VS Code/Cursor 설정
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "/home/$USER/venvs/backend_venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"]
}
```

### 4단계: 터미널 설정

#### Windows Terminal 설정
```json
// Windows Terminal settings.json
{
    "profiles": {
        "list": [
            {
                "guid": "{your-guid}",
                "name": "WSL Ubuntu",
                "source": "Windows.Terminal.Wsl",
                "startingDirectory": "//wsl$/Ubuntu/home/$USER/projects/CMA"
            }
        ]
    }
}
```

---

## ⚡ 성능 최적화

### 1단계: WSL2 설정 최적화

#### .wslconfig 파일 생성
```powershell
# Windows에서 실행
notepad "$env:USERPROFILE\.wslconfig"
```

#### 설정 내용
```ini
[wsl2]
# 메모리 설정
memory=8GB
processors=4

# 스왑 설정
swap=2GB
swapFile=D:\\WSL\\swap.vhdx

# 네트워크 설정
localhostForwarding=true

# 성능 설정
pageReporting=false
```

### 2단계: Ubuntu 내부 최적화

#### 시스템 최적화
```bash
# 불필요한 서비스 비활성화
sudo systemctl disable snapd
sudo systemctl disable snapd.socket

# 로그 로테이션 설정
sudo nano /etc/logrotate.conf
```

#### 메모리 최적화
```bash
# 스왑 파일 생성
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 영구 설정
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 3단계: 개발 환경 최적화

#### Python 최적화
```bash
# pip 캐시 정리
pip cache purge

# 가상환경 최적화
python3 -m venv --copies venv_name
```

#### Node.js 최적화
```bash
# npm 캐시 정리
npm cache clean --force

# 글로벌 패키지 정리
npm list -g --depth=0
```

---

## 🔧 문제 해결

### 1단계: 일반적인 문제들

#### WSL2 시작 실패
```powershell
# WSL2 재시작
wsl --shutdown
wsl -d Ubuntu

# 또는 완전 재설치
wsl --unregister Ubuntu
wsl --install -d Ubuntu -d D:\WSL
```

#### 메모리 부족
```powershell
# .wslconfig 수정
[wsl2]
memory=4GB  # 메모리 줄이기
swap=4GB    # 스왑 늘리기
```

#### 네트워크 문제
```powershell
# 포트 포워딩 설정
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=localhost
netsh interface portproxy add v4tov4 listenport=3000 listenaddress=0.0.0.0 connectport=3000 connectaddress=localhost
```

### 2단계: 성능 문제

#### 느린 파일 접근
```bash
# WSL2 내부에서 작업 권장
# Windows 파일시스템 접근 최소화
```

#### 높은 CPU 사용률
```bash
# 프로세스 모니터링
htop

# 불필요한 프로세스 종료
pkill -f process_name
```

### 3단계: 데이터베이스 문제

#### PostgreSQL 연결 실패
```bash
# 서비스 상태 확인
sudo systemctl status postgresql

# 서비스 재시작
sudo systemctl restart postgresql

# 설정 확인
sudo nano /etc/postgresql/*/main/postgresql.conf
```

#### Redis 연결 실패
```bash
# 서비스 상태 확인
sudo systemctl status redis-server

# 서비스 재시작
sudo systemctl restart redis-server
```

---

## 🔄 유지보수

### 1단계: 정기적인 업데이트

#### 시스템 업데이트
```bash
# Ubuntu 업데이트
sudo apt update && sudo apt upgrade

# 패키지 정리
sudo apt autoremove
sudo apt autoclean
```

#### WSL2 업데이트
```powershell
# Windows에서 WSL 업데이트
wsl --update
```

### 2단계: 백업 및 복원

#### WSL2 백업
```powershell
# 전체 WSL2 백업
wsl --export Ubuntu D:\WSL\ubuntu-backup-$(Get-Date -Format 'yyyyMMdd').tar

# 특정 폴더 백업
wsl -d Ubuntu tar -czf /mnt/d/WSL/projects-backup-$(date +%Y%m%d).tar.gz /home/$USER/projects
```

#### 프로젝트 백업
```bash
# Git 저장소 백업
cd ~/projects/CMA
git push origin main

# 데이터베이스 백업
pg_dump cma_db > ~/backups/cma_db_$(date +%Y%m%d).sql
```

### 3단계: 성능 모니터링

#### 시스템 모니터링
```bash
# 실시간 모니터링
htop
iotop
df -h

# 로그 확인
journalctl -f
```

#### 개발 환경 모니터링
```bash
# Python 프로세스 확인
ps aux | grep python

# Node.js 프로세스 확인
ps aux | grep node

# 포트 사용 확인
netstat -tulpn
```

---

## 📋 체크리스트

### 설치 완료 확인
- [ ] WSL2 활성화 완료
- [ ] Ubuntu 설치 완료 (D 드라이브)
- [ ] 기본 도구 설치 완료
- [ ] Python 환경 설정 완료
- [ ] Node.js 설치 완료
- [ ] PostgreSQL 설치 완료
- [ ] Redis 설치 완료
- [ ] CMA 프로젝트 클론 완료
- [ ] 가상환경 설정 완료
- [ ] VS Code/Cursor 연동 완료
- [ ] 성능 최적화 완료

### 테스트 확인
- [ ] WSL2 Ubuntu 실행 테스트
- [ ] Python 가상환경 활성화 테스트
- [ ] Node.js 실행 테스트
- [ ] PostgreSQL 연결 테스트
- [ ] Redis 연결 테스트
- [ ] CMA 프로젝트 실행 테스트
- [ ] VS Code/Cursor에서 WSL 연동 테스트

---

## 📞 지원 및 문의

### 문제 발생 시
1. **이 문서의 문제 해결 섹션** 확인
2. **WSL2 공식 문서** 참조
3. **CMA 프로젝트 이슈 트래커** 확인
4. **개발팀에 문의**

### 유용한 링크
- [WSL2 공식 문서](https://docs.microsoft.com/en-us/windows/wsl/)
- [Ubuntu WSL 가이드](https://ubuntu.com/wsl)
- [VS Code WSL 확장](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)

---

## 📝 버전 정보

- **문서 버전**: 1.0
- **최종 업데이트**: 2025-01-23
- **작성자**: CMA 개발팀
- **검토자**: 시스템 관리자

---

**이 문서를 참조하여 D 드라이브 WSL2 환경을 성공적으로 설정하시기 바랍니다!** 