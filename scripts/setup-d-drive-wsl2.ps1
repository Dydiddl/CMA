# 🚀 D 드라이브 WSL2 개발 환경 자동 설정 스크립트 (PowerShell)
# CMA 프로젝트용 WSL2 환경 구축

param(
    [switch]$SkipConfirmation,
    [string]$WslInstallPath = "D:\WSL",
    [string]$ProjectPath = "D:\Projects"
)

# 오류 발생 시 스크립트 중단
$ErrorActionPreference = "Stop"

# 색상 정의
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

# 로그 함수
function Write-LogInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-LogSuccess {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-LogWarning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-LogError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

# 제목 출력
function Write-Title {
    Write-Host "==========================================" -ForegroundColor $Blue
    Write-Host "  D 드라이브 WSL2 개발 환경 설정 스크립트" -ForegroundColor $Blue
    Write-Host "  CMA 프로젝트용" -ForegroundColor $Blue
    Write-Host "==========================================" -ForegroundColor $Blue
    Write-Host ""
}

# 관리자 권한 확인
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# 시스템 정보 확인
function Get-SystemInfo {
    Write-LogInfo "시스템 정보 확인 중..."
    
    # Windows 버전 확인
    $osInfo = Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion
    Write-LogInfo "OS: $($osInfo.WindowsProductName) $($osInfo.WindowsVersion)"
    
    # 메모리 확인
    $memory = Get-ComputerInfo | Select-Object TotalPhysicalMemory
    $memoryGB = [math]::Round($memory.TotalPhysicalMemory / 1GB, 1)
    Write-LogInfo "총 메모리: ${memoryGB}GB"
    
    # D 드라이브 확인
    if (Test-Path "D:\") {
        $dDrive = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='D:'"
        $freeSpaceGB = [math]::Round($dDrive.FreeSpace / 1GB, 1)
        Write-LogInfo "D 드라이브 여유 공간: ${freeSpaceGB}GB"
    } else {
        Write-LogError "D 드라이브를 찾을 수 없습니다."
        exit 1
    }
    
    # WSL 상태 확인
    try {
        $wslStatus = wsl --list --verbose 2>$null
        if ($wslStatus) {
            Write-LogInfo "현재 WSL 배포판:"
            Write-Host $wslStatus
        } else {
            Write-LogInfo "WSL이 설치되어 있지 않습니다."
        }
    } catch {
        Write-LogInfo "WSL이 설치되어 있지 않습니다."
    }
}

# WSL2 설치 및 설정
function Install-WSL2 {
    Write-LogInfo "WSL2 설치 및 설정 중..."
    
    # WSL 기능 활성화
    Write-LogInfo "WSL 기능 활성화 중..."
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    
    Write-LogWarning "시스템 재부팅이 필요합니다. 재부팅 후 스크립트를 다시 실행하세요."
    $reboot = Read-Host "지금 재부팅하시겠습니까? (y/N)"
    if ($reboot -eq 'y' -or $reboot -eq 'Y') {
        Restart-Computer -Force
    } else {
        Write-LogInfo "수동으로 재부팅 후 스크립트를 다시 실행하세요."
        exit 0
    }
}

# WSL2 커널 업데이트
function Update-WSL2Kernel {
    Write-LogInfo "WSL2 커널 업데이트 중..."
    
    # 커널 업데이트 패키지 다운로드
    $kernelUrl = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
    $kernelPath = "$env:TEMP\wsl_update_x64.msi"
    
    try {
        Invoke-WebRequest -Uri $kernelUrl -OutFile $kernelPath
        Write-LogInfo "커널 업데이트 패키지 다운로드 완료"
        
        # 설치
        Start-Process msiexec.exe -Wait -ArgumentList "/i $kernelPath /quiet"
        Write-LogSuccess "WSL2 커널 업데이트 완료"
        
        # 임시 파일 삭제
        Remove-Item $kernelPath -Force
    } catch {
        Write-LogError "커널 업데이트 실패: $($_.Exception.Message)"
        Write-LogInfo "수동으로 다운로드하여 설치하세요: https://aka.ms/wsl2kernel"
    }
}

# Ubuntu 설치 (D 드라이브)
function Install-UbuntuOnDDrive {
    Write-LogInfo "D 드라이브에 Ubuntu 설치 중..."
    
    # D 드라이브에 WSL 폴더 생성
    if (!(Test-Path $WslInstallPath)) {
        New-Item -ItemType Directory -Path $WslInstallPath -Force
        Write-LogInfo "WSL 설치 폴더 생성: $WslInstallPath"
    }
    
    # 기존 Ubuntu 확인
    $existingUbuntu = wsl --list --verbose 2>$null | Select-String "Ubuntu"
    
    if ($existingUbuntu) {
        Write-LogWarning "기존 Ubuntu가 발견되었습니다."
        $backupChoice = Read-Host "기존 Ubuntu를 D 드라이브로 이동하시겠습니까? (y/N)"
        
        if ($backupChoice -eq 'y' -or $backupChoice -eq 'Y') {
            # 기존 Ubuntu 백업
            $backupPath = "$WslInstallPath\ubuntu-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss').tar"
            wsl --export Ubuntu $backupPath
            Write-LogInfo "기존 Ubuntu 백업 완료: $backupPath"
            
            # 기존 Ubuntu 제거
            wsl --unregister Ubuntu
            Write-LogInfo "기존 Ubuntu 제거 완료"
            
            # D 드라이브에 복원
            wsl --import Ubuntu $WslInstallPath $backupPath --version 2
            Write-LogSuccess "Ubuntu를 D 드라이브로 이동 완료"
        }
    } else {
        # 새로 설치
        try {
            wsl --install -d Ubuntu
            Write-LogSuccess "Ubuntu 설치 완료"
        } catch {
            Write-LogError "Ubuntu 설치 실패: $($_.Exception.Message)"
            Write-LogInfo "Microsoft Store에서 Ubuntu를 수동으로 설치하세요."
        }
    }
}

# WSL2 설정 최적화
function Optimize-WSL2Config {
    Write-LogInfo "WSL2 설정 최적화 중..."
    
    # .wslconfig 파일 생성
    $wslConfigPath = "$env:USERPROFILE\.wslconfig"
    $wslConfig = @"
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
"@
    
    $wslConfig | Out-File -FilePath $wslConfigPath -Encoding UTF8
    Write-LogSuccess "WSL2 설정 파일 생성 완료: $wslConfigPath"
}

# 포트 포워딩 설정
function Set-PortForwarding {
    Write-LogInfo "포트 포워딩 설정 중..."
    
    # 기존 포트 포워딩 제거
    netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0 2>$null
    netsh interface portproxy delete v4tov4 listenport=3000 listenaddress=0.0.0.0 2>$null
    
    # 새로운 포트 포워딩 설정
    netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=localhost
    netsh interface portproxy add v4tov4 listenport=3000 listenaddress=0.0.0.0 connectport=3000 connectaddress=localhost
    
    Write-LogSuccess "포트 포워딩 설정 완료"
    Write-LogInfo "백엔드 서버: http://localhost:8000"
    Write-LogInfo "프론트엔드 서버: http://localhost:3000"
}

# 프로젝트 폴더 생성
function Create-ProjectFolders {
    Write-LogInfo "프로젝트 폴더 생성 중..."
    
    # D 드라이브에 프로젝트 폴더 생성
    if (!(Test-Path $ProjectPath)) {
        New-Item -ItemType Directory -Path $ProjectPath -Force
        Write-LogInfo "프로젝트 폴더 생성: $ProjectPath"
    }
    
    # 하위 폴더 생성
    $subFolders = @("CMA", "Backups", "Downloads", "Documents")
    
    foreach ($folder in $subFolders) {
        $folderPath = Join-Path $ProjectPath $folder
        if (!(Test-Path $folderPath)) {
            New-Item -ItemType Directory -Path $folderPath -Force
            Write-LogInfo "폴더 생성: $folderPath"
        }
    }
    
    Write-LogSuccess "프로젝트 폴더 생성 완료"
}

# VS Code 설정
function Setup-VSCode {
    Write-LogInfo "VS Code 설정 중..."
    
    # VS Code가 설치되어 있는지 확인
    $vscodePath = Get-Command code -ErrorAction SilentlyContinue
    
    if ($vscodePath) {
        Write-LogInfo "VS Code가 설치되어 있습니다."
        
        # WSL 확장 설치
        try {
            code --install-extension ms-vscode-remote.remote-wsl
            Write-LogSuccess "WSL 확장 설치 완료"
        } catch {
            Write-LogWarning "WSL 확장 설치 실패. 수동으로 설치하세요."
        }
        
        # 권장 확장 설치
        $recommendedExtensions = @(
            "ms-python.python",
            "ms-python.black-formatter",
            "ms-python.isort",
            "ms-vscode.vscode-json",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode"
        )
        
        foreach ($extension in $recommendedExtensions) {
            try {
                code --install-extension $extension
                Write-LogInfo "확장 설치: $extension"
            } catch {
                Write-LogWarning "확장 설치 실패: $extension"
            }
        }
    } else {
        Write-LogWarning "VS Code가 설치되어 있지 않습니다."
        Write-LogInfo "VS Code를 설치한 후 WSL 확장을 설치하세요."
    }
}

# Windows Terminal 설정
function Setup-WindowsTerminal {
    Write-LogInfo "Windows Terminal 설정 중..."
    
    # Windows Terminal이 설치되어 있는지 확인
    $terminalPath = Get-Command wt -ErrorAction SilentlyContinue
    
    if ($terminalPath) {
        Write-LogInfo "Windows Terminal이 설치되어 있습니다."
        
        # 설정 파일 경로
        $settingsPath = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
        
        if (Test-Path $settingsPath) {
            Write-LogInfo "Windows Terminal 설정 파일이 존재합니다."
            Write-LogInfo "WSL 프로필을 수동으로 추가하세요."
        } else {
            Write-LogInfo "Windows Terminal 설정 파일을 찾을 수 없습니다."
        }
    } else {
        Write-LogWarning "Windows Terminal이 설치되어 있지 않습니다."
        Write-LogInfo "Microsoft Store에서 Windows Terminal을 설치하세요."
    }
}

# 환경 검증
function Test-Environment {
    Write-LogInfo "환경 검증 중..."
    
    # WSL 상태 확인
    try {
        $wslStatus = wsl --list --verbose
        if ($wslStatus -match "Ubuntu") {
            Write-LogSuccess "WSL Ubuntu 정상 작동"
        } else {
            Write-LogError "WSL Ubuntu를 찾을 수 없습니다."
        }
    } catch {
        Write-LogError "WSL 상태 확인 실패"
    }
    
    # 포트 포워딩 확인
    try {
        $portForwarding = netsh interface portproxy show all
        if ($portForwarding -match "8000|3000") {
            Write-LogSuccess "포트 포워딩 정상 작동"
        } else {
            Write-LogWarning "포트 포워딩이 설정되지 않았습니다."
        }
    } catch {
        Write-LogError "포트 포워딩 확인 실패"
    }
    
    # 폴더 확인
    if (Test-Path $WslInstallPath) {
        Write-LogSuccess "WSL 설치 폴더 정상"
    } else {
        Write-LogError "WSL 설치 폴더를 찾을 수 없습니다."
    }
    
    if (Test-Path $ProjectPath) {
        Write-LogSuccess "프로젝트 폴더 정상"
    } else {
        Write-LogError "프로젝트 폴더를 찾을 수 없습니다."
    }
}

# 완료 메시지
function Write-CompletionMessage {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor $Green
    Write-Host "  🎉 D 드라이브 WSL2 환경 설정 완료!" -ForegroundColor $Green
    Write-Host "==========================================" -ForegroundColor $Green
    Write-Host ""
    
    Write-Host "다음 단계:" -ForegroundColor $White
    Write-Host "1. WSL2 Ubuntu에서 개발 환경 설정 스크립트 실행" -ForegroundColor $White
    Write-Host "2. VS Code/Cursor에서 WSL 확장 설치" -ForegroundColor $White
    Write-Host "3. CMA 프로젝트 클론 및 설정" -ForegroundColor $White
    Write-Host ""
    
    Write-Host "유용한 명령어:" -ForegroundColor $White
    Write-Host "  wsl -d Ubuntu                    # Ubuntu 실행" -ForegroundColor $White
    Write-Host "  wsl --shutdown                   # WSL 종료" -ForegroundColor $White
    Write-Host "  wsl --list --verbose             # WSL 상태 확인" -ForegroundColor $White
    Write-Host ""
    
    Write-Host "설정 파일 위치:" -ForegroundColor $White
    Write-Host "  WSL 설정: $env:USERPROFILE\.wslconfig" -ForegroundColor $White
    Write-Host "  WSL 설치: $WslInstallPath" -ForegroundColor $White
    Write-Host "  프로젝트: $ProjectPath" -ForegroundColor $White
    Write-Host ""
    
    Write-Host "문서 참조: docs/environment-setup/D-drive-wsl2-setup.md" -ForegroundColor $White
}

# 메인 함수
function Main {
    Write-Title
    
    # 관리자 권한 확인
    if (!(Test-Administrator)) {
        Write-LogError "이 스크립트는 관리자 권한이 필요합니다."
        Write-LogInfo "PowerShell을 관리자 권한으로 실행하세요."
        exit 1
    }
    
    # 시스템 정보 확인
    Get-SystemInfo
    
    # 사용자 확인
    if (!$SkipConfirmation) {
        Write-Host "이 스크립트는 D 드라이브 WSL2 환경을 설정합니다." -ForegroundColor $Yellow
        $confirm = Read-Host "계속하시겠습니까? (y/N)"
        
        if ($confirm -ne 'y' -and $confirm -ne 'Y') {
            Write-LogInfo "설정을 취소했습니다."
            exit 0
        }
    }
    
    # 단계별 실행
    try {
        # WSL2 설치 (필요시)
        if (!(Get-Command wsl -ErrorAction SilentlyContinue)) {
            Install-WSL2
            return  # 재부팅 후 다시 실행 필요
        }
        
        Update-WSL2Kernel
        Install-UbuntuOnDDrive
        Optimize-WSL2Config
        Set-PortForwarding
        Create-ProjectFolders
        Setup-VSCode
        Setup-WindowsTerminal
        Test-Environment
        
        Write-CompletionMessage
        
    } catch {
        Write-LogError "설정 중 오류 발생: $($_.Exception.Message)"
        Write-LogInfo "문제 해결 섹션을 참조하세요."
        exit 1
    }
}

# 스크립트 실행
Main 