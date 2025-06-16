# 색상 정의
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Red = [System.ConsoleColor]::Red

Write-Host "CMA 프로젝트 초기 설정을 시작합니다..." -ForegroundColor $Yellow

# Python 버전 확인
try {
    $pythonVersion = python --version
    if (-not $?) {
        throw "Python이 설치되어 있지 않습니다."
    }
} catch {
    Write-Host "Error: Python이 설치되어 있지 않습니다." -ForegroundColor $Red
    exit 1
}

# 가상환경 생성
Write-Host "가상환경을 생성합니다..." -ForegroundColor $Yellow
python -m venv venv

# 가상환경 활성화
Write-Host "가상환경을 활성화합니다..." -ForegroundColor $Yellow
.\venv\Scripts\Activate.ps1

# pip 업그레이드
Write-Host "pip를 최신 버전으로 업그레이드합니다..." -ForegroundColor $Yellow
python -m pip install --upgrade pip

# 의존성 설치
Write-Host "필요한 패키지들을 설치합니다..." -ForegroundColor $Yellow
pip install -r requirements.txt

Write-Host "설정이 완료되었습니다!" -ForegroundColor $Green
Write-Host "다음 명령어로 서버를 실행할 수 있습니다:" -ForegroundColor $Yellow
Write-Host ".\venv\Scripts\Activate.ps1"
Write-Host "uvicorn app.main:app --reload --port 8000" 