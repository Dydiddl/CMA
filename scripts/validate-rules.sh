#!/bin/bash
# scripts/validate-rules.sh
# Cursor Rules 검증 스크립트

set -e

echo "🔍 Cursor Rules 검증 시작..."
echo "=================================="

# 1. 파일 존재 확인
echo "1. 파일 존재 확인 중..."
if [ ! -f ".cursorrules" ]; then
    echo "❌ .cursorrules 파일이 존재하지 않습니다."
    exit 1
fi
echo "✅ .cursorrules 파일 확인됨"

# 2. 문법 검증
echo "2. 문법 검증 중..."
if ! grep -q "## 🚨 CRITICAL RULES" .cursorrules; then
    echo "❌ CRITICAL RULES 섹션 누락"
    exit 1
fi

if ! grep -q "## 📁 Project Structure" .cursorrules; then
    echo "❌ Project Structure 섹션 누락"
    exit 1
fi

if ! grep -q "## 🎯 Project Overview" .cursorrules; then
    echo "❌ Project Overview 섹션 누락"
    exit 1
fi
echo "✅ 기본 섹션 확인됨"

# 3. 버전 정보 확인
echo "3. 버전 정보 확인 중..."
if ! grep -q "version:" .cursorrules; then
    echo "❌ 버전 정보 누락"
    exit 1
fi

if ! grep -q "last_updated:" .cursorrules; then
    echo "❌ 최종 업데이트 정보 누락"
    exit 1
fi
echo "✅ 버전 정보 확인됨"

# 4. 최신 업데이트 확인
echo "4. 최신 업데이트 확인 중..."
last_update=$(grep "last_updated:" .cursorrules | cut -d'"' -f2)
if [ -z "$last_update" ]; then
    echo "❌ 최종 업데이트 날짜를 찾을 수 없습니다."
    exit 1
fi

# 날짜 형식 검증 (YYYY-MM-DD)
if ! echo "$last_update" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
    echo "❌ 날짜 형식이 올바르지 않습니다: $last_update"
    exit 1
fi

# 30일 이상 업데이트되지 않았는지 확인
days_since_update=$(( ($(date +%s) - $(date -d "$last_update" +%s)) / 86400 ))

if [ $days_since_update -gt 30 ]; then
    echo "⚠️  규칙이 30일 이상 업데이트되지 않음 (${days_since_update}일 전)"
else
    echo "✅ 최신 업데이트 확인됨 (${days_since_update}일 전)"
fi

# 5. 새로운 규칙 확인
echo "5. 새로운 규칙 확인 중..."
new_rules_count=$(grep -c "🆕" .cursorrules || echo "0")
echo "새로운 규칙 수: $new_rules_count"

# 6. 코드 예시 검증
echo "6. 코드 예시 검증 중..."
python_examples=$(grep -c "```python" .cursorrules || echo "0")
typescript_examples=$(grep -c "```typescript" .cursorrules || echo "0")
echo "Python 예시: $python_examples개"
echo "TypeScript 예시: $typescript_examples개"

# 7. 프로젝트 구조 검증
echo "7. 프로젝트 구조 검증 중..."
if ! grep -q "backend/" .cursorrules; then
    echo "⚠️  backend 디렉토리 구조 누락"
fi

if ! grep -q "frontend/" .cursorrules; then
    echo "⚠️  frontend 디렉토리 구조 누락"
fi

if ! grep -q "src-tauri/" .cursorrules; then
    echo "⚠️  src-tauri 디렉토리 구조 누락"
fi

# 8. 기술 스택 검증
echo "8. 기술 스택 검증 중..."
if ! grep -q "Python" .cursorrules; then
    echo "⚠️  Python 기술 스택 정보 누락"
fi

if ! grep -q "React" .cursorrules; then
    echo "⚠️  React 기술 스택 정보 누락"
fi

if ! grep -q "FastAPI" .cursorrules; then
    echo "⚠️  FastAPI 기술 스택 정보 누락"
fi

# 9. 규칙 통계
echo "9. 규칙 통계 생성 중..."
total_rules=$(grep -c "###" .cursorrules || echo "0")
total_sections=$(grep -c "## " .cursorrules || echo "0")

echo "=================================="
echo "📊 규칙 통계"
echo "총 섹션 수: $total_sections"
echo "총 규칙 수: $total_rules"
echo "새로운 규칙 수: $new_rules_count"
echo "Python 예시: $python_examples개"
echo "TypeScript 예시: $typescript_examples개"
echo "최종 업데이트: $last_update"
echo "=================================="

# 10. 권장사항
echo "10. 권장사항 확인 중..."
if [ $days_since_update -gt 30 ]; then
    echo "💡 권장사항: 규칙을 최신 상태로 업데이트하세요."
fi

if [ $new_rules_count -eq 0 ]; then
    echo "💡 권장사항: 새로운 기능에 대한 규칙을 추가하세요."
fi

if [ $python_examples -lt 5 ]; then
    echo "💡 권장사항: Python 코드 예시를 더 추가하세요."
fi

if [ $typescript_examples -lt 5 ]; then
    echo "💡 권장사항: TypeScript 코드 예시를 더 추가하세요."
fi

echo "=================================="
echo "✅ Cursor Rules 검증 완료"
echo "모든 필수 항목이 확인되었습니다." 