#!/bin/bash

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate

# pip 업그레이드
pip install --upgrade pip

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
alembic upgrade head

# 테스트 실행
pytest

echo "설치가 완료되었습니다." 