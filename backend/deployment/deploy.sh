#!/bin/bash
# CMA 배포 스크립트

echo "CMA 배포 시작..."

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
alembic upgrade head

# 애플리케이션 시작
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "CMA 배포 완료"
