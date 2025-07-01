#!/bin/bash
# CMA 프로젝트 확장 프로그램 일괄 설치 스크립트
# Cursor에서 실행

set -e  # 오류 발생 시 스크립트 중단

echo "🚀 CMA 프로젝트 확장 프로그램 설치를 시작합니다..."
echo "📋 설치 대상: Cursor (VSCode 기반)"
echo ""

# Python 개발 확장
echo "📦 Python 개발 확장 설치 중..."
cursor --install-extension ms-python.python
cursor --install-extension ms-python.black-formatter
cursor --install-extension ms-python.isort
cursor --install-extension ms-python.flake8
cursor --install-extension ms-python.pylint
cursor --install-extension ms-python.pytest-adapter
cursor --install-extension ms-python.fastapi
cursor --install-extension ms-python.pydantic
cursor --install-extension ms-python.sqlalchemy
cursor --install-extension ms-python.jupyter
echo "✅ Python 개발 확장 설치 완료"
echo ""

# React/TypeScript 개발 확장
echo "⚛️ React/TypeScript 개발 확장 설치 중..."
cursor --install-extension ms-vscode.vscode-typescript-next
cursor --install-extension esbenp.prettier-vscode
cursor --install-extension dbaeumer.vscode-eslint
cursor --install-extension formulahendry.auto-rename-tag
cursor --install-extension christian-kohler.path-intellisense
cursor --install-extension ms-vscode.vscode-css-peek
cursor --install-extension formulahendry.auto-close-tag
echo "✅ React/TypeScript 개발 확장 설치 완료"
echo ""

# 데이터베이스 확장
echo "🗄️ 데이터베이스 확장 설치 중..."
cursor --install-extension ckolkman.vscode-postgres
cursor --install-extension cweijan.vscode-redis-client
cursor --install-extension mtxr.sqltools
cursor --install-extension mtxr.sqltools-driver-pg
echo "✅ 데이터베이스 확장 설치 완료"
echo ""

# 파일 처리 확장
echo "📊 파일 처리 확장 설치 중..."
cursor --install-extension ms-vscode.vscode-pdf
cursor --install-extension janisdd.vscode-edit-csv
cursor --install-extension mechatroner.rainbow-csv
cursor --install-extension yzhang.markdown-all-in-one
cursor --install-extension ms-vscode.vscode-yaml
echo "✅ 파일 처리 확장 설치 완료"
echo ""

# 개발 생산성 확장
echo "🔧 개발 생산성 확장 설치 중..."
cursor --install-extension eamodio.gitlens
cursor --install-extension mhutchie.git-graph
cursor --install-extension ms-vscode.vscode-docker
cursor --install-extension ms-vscode.vscode-terminal
echo "✅ 개발 생산성 확장 설치 완료"
echo ""

# 테스트 및 디버깅 확장
echo "🧪 테스트 및 디버깅 확장 설치 중..."
cursor --install-extension ms-vscode.vscode-jest
cursor --install-extension ms-vscode.vscode-js-debug
echo "✅ 테스트 및 디버깅 확장 설치 완료"
echo ""

# UI/UX 확장
echo "🎨 UI/UX 확장 설치 중..."
cursor --install-extension pkief.material-icon-theme
cursor --install-extension zhuangtongfa.material-theme
echo "✅ UI/UX 확장 설치 완료"
echo ""

echo "🎉 모든 확장 프로그램 설치가 완료되었습니다!"
echo ""
echo "📋 설치된 확장 프로그램 목록:"
cursor --list-extensions
echo ""
echo "🔄 다음 단계:"
echo "1. Cursor를 재시작하여 확장 프로그램을 활성화하세요"
echo "2. .vscode/settings.json 파일을 생성하여 프로젝트 설정을 적용하세요"
echo "3. .vscode/launch.json 파일을 생성하여 디버깅 설정을 추가하세요"
echo ""
echo "📖 자세한 설정 방법은 docs/development/vscode-extensions.md 파일을 참조하세요" 