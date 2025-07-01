#!/bin/bash
# WSL2에서 CMA GUI 실행 스크립트

echo "=== CMA GUI 실행 스크립트 ==="
echo "WSL2에서 GUI를 실행하기 위한 설정을 확인합니다..."

# 1. X 서버 연결 확인
if [ -z "$DISPLAY" ]; then
    echo "DISPLAY 환경변수가 설정되지 않았습니다."
    echo "Windows에서 X 서버(VcXsrv, X410 등)를 실행하고 다음 명령을 실행하세요:"
    echo "export DISPLAY=localhost:0.0"
    echo "또는"
    echo "export DISPLAY=\$(cat /etc/resolv.conf | grep nameserver | awk '{print \$2}'):0.0"
    exit 1
fi

# 2. 가상환경 활성화
if [ ! -d "venv" ]; then
    echo "가상환경이 없습니다. 생성합니다..."
    python3 -m venv venv
fi

echo "가상환경을 활성화합니다..."
source venv/bin/activate

# 3. 의존성 설치 확인
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt가 없습니다."
    exit 1
fi

echo "의존성을 설치합니다..."
pip install -r requirements.txt

# 4. GUI 실행
echo "CMA GUI를 실행합니다..."
echo "DISPLAY: $DISPLAY"
echo "플랫폼: $(python -c 'import platform; print(platform.system())')"

# GUI 모드로 실행
python main.py

echo "CMA GUI가 종료되었습니다." 