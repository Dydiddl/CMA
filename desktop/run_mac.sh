#!/bin/bash
# Mac에서 CMA GUI 실행 스크립트

echo "=== CMA Mac GUI 실행 스크립트 ==="
echo "Mac 환경에서 GUI를 실행하기 위한 설정을 확인합니다..."

# 1. Python 버전 확인
echo "Python 버전 확인 중..."
python3 --version

# 2. 가상환경 확인 및 생성
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

# 4. Mac 환경 변수 설정
export LANG=ko_KR.UTF-8
export LC_ALL=ko_KR.UTF-8
export QT_QPA_PLATFORM=cocoa
export QT_MAC_WANTS_LAYER=1

# 5. GUI 실행
echo "CMA GUI를 실행합니다..."
echo "플랫폼: $(python -c 'import platform; print(platform.system())')"
echo "Python 경로: $(which python)"

# GUI 모드로 실행
python main.py

echo "CMA GUI가 종료되었습니다." 