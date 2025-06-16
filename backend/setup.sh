#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}CMA 프로젝트 초기 설정을 시작합니다...${NC}"

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3가 설치되어 있지 않습니다.${NC}"
    exit 1
fi

# 가상환경 생성
echo -e "${YELLOW}가상환경을 생성합니다...${NC}"
python3 -m venv venv

# 가상환경 활성화
echo -e "${YELLOW}가상환경을 활성화합니다...${NC}"
source venv/bin/activate

# pip 업그레이드
echo -e "${YELLOW}pip를 최신 버전으로 업그레이드합니다...${NC}"
pip install --upgrade pip

# 의존성 설치
echo -e "${YELLOW}필요한 패키지들을 설치합니다...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}설정이 완료되었습니다!${NC}"
echo -e "${YELLOW}다음 명령어로 서버를 실행할 수 있습니다:${NC}"
echo -e "source venv/bin/activate"
echo -e "uvicorn app.main:app --reload --port 8000" 