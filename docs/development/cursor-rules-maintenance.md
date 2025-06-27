# Cursor Rules 유지보수 가이드

*최종 업데이트: 2025-01-23*

## 📋 개요

이 문서는 CMA 프로젝트의 `.cursorrules` 파일을 체계적으로 관리하고 갱신하기 위한 프로세스를 정의합니다.

## 🎯 목적

- 프로젝트 규칙의 일관성 유지
- 새로운 기능 추가 시 규칙 자동 갱신
- 개발 품질 표준화
- 팀 협업 효율성 증대

## 🔄 규칙 갱신 프로세스

### 1. 갱신 트리거 감지

#### 자동 감지 항목
- [ ] 새로운 모듈/패키지 추가
- [ ] 기술 스택 버전 업데이트
- [ ] 새로운 API 엔드포인트 추가
- [ ] 데이터베이스 스키마 변경
- [ ] 새로운 개발 도구 도입

#### 수동 감지 항목
- [ ] 성능 이슈 발생
- [ ] 보안 취약점 발견
- [ ] 코드 품질 문제
- [ ] 팀 피드백 수집
- [ ] 외부 요구사항 변경

### 2. 분석 단계

#### 현재 규칙 분석
```bash
# 규칙 파일 분석
cat .cursorrules | grep -n "###"  # 섹션별 분석
cat .cursorrules | grep -n "🆕"   # 새로운 규칙 확인
cat .cursorrules | grep -n "TODO" # 미완성 규칙 확인
```

#### 프로젝트 현황 분석
```bash
# 기술 스택 버전 확인
cat package.json | grep -E '"version"'
cat requirements.txt | grep -E "=="
cat Cargo.toml | grep -E 'version ='

# 새로운 파일/디렉토리 확인
git status --porcelain
find . -name "*.py" -o -name "*.ts" -o -name "*.tsx" | head -20
```

### 3. 기안 단계

#### 규칙 기안 템플릿
```markdown
## 🆕 [규칙명] - [날짜]

### 변경 사유
- [변경 사유 1]
- [변경 사유 2]

### 제안 내용
```[언어]
[코드 예시]
```

### 영향 범위
- [영향받는 파일/모듈]
- [영향받는 개발자]
- [예상 개발 시간]

### 검증 방법
- [테스트 방법]
- [검증 기준]
```

### 4. 검토 단계

#### 검토 체크리스트
- [ ] 규칙의 명확성
- [ ] 실제 적용 가능성
- [ ] 기존 규칙과의 일관성
- [ ] 성능 영향 분석
- [ ] 보안 고려사항
- [ ] 문서화 완성도

#### 검토자 역할
1. **기술 리드**: 기술적 정확성 검토
2. **팀 리드**: 팀 전체 영향도 검토
3. **QA 리드**: 테스트 가능성 검토
4. **보안 담당자**: 보안 영향 검토

### 5. 승인 단계

#### 승인 기준
- [ ] 모든 검토자 승인
- [ ] 충돌 사항 해결
- [ ] 테스트 계획 수립
- [ ] 롤백 계획 수립

#### 승인 프로세스
1. 검토 결과 요약
2. 최종 규칙안 작성
3. 팀 전체 투표
4. 승인/반려 결정

### 6. 적용 단계

#### 백업 및 버전 관리
```bash
# 백업 생성
cp .cursorrules .cursorrules.backup.$(date +%Y%m%d)

# Git 태그 생성
git add .cursorrules
git commit -m "feat(rules): 규칙 갱신 v2.0"
git tag -a v2.0-rules -m "Cursor Rules v2.0"
```

#### 규칙 적용
1. `.cursorrules` 파일 업데이트
2. 버전 정보 업데이트
3. 변경 로그 추가
4. 관련 문서 업데이트

### 7. 공지 단계

#### 공지 방법
- [ ] 팀 미팅에서 공지
- [ ] 이메일 발송
- [ ] 슬랙/팀즈 공지
- [ ] 문서 업데이트

#### 공지 내용
- 변경된 규칙 요약
- 적용 시점
- 영향받는 개발 영역
- 질문/피드백 방법

### 8. 모니터링 단계

#### 모니터링 지표
- [ ] 규칙 준수율
- [ ] 코드 품질 지표
- [ ] 개발 속도 변화
- [ ] 버그 발생률
- [ ] 팀 만족도

#### 모니터링 주기
- **일간**: 규칙 적용 현황 체크
- **주간**: 품질 지표 분석
- **월간**: 전체 효과 평가
- **분기별**: 규칙 개선 검토

## 📊 규칙 관리 도구

### 자동화 스크립트

#### 규칙 검증 스크립트
```bash
#!/bin/bash
# scripts/validate-rules.sh

echo "🔍 Cursor Rules 검증 시작..."

# 1. 문법 검증
echo "1. 문법 검증 중..."
if ! grep -q "## 🚨 CRITICAL RULES" .cursorrules; then
    echo "❌ CRITICAL RULES 섹션 누락"
    exit 1
fi

# 2. 버전 정보 확인
echo "2. 버전 정보 확인 중..."
if ! grep -q "version:" .cursorrules; then
    echo "❌ 버전 정보 누락"
    exit 1
fi

# 3. 최신 업데이트 확인
echo "3. 최신 업데이트 확인 중..."
last_update=$(grep "last_updated:" .cursorrules | cut -d'"' -f2)
days_since_update=$(( ($(date +%s) - $(date -d "$last_update" +%s)) / 86400 ))

if [ $days_since_update -gt 30 ]; then
    echo "⚠️  규칙이 30일 이상 업데이트되지 않음"
fi

echo "✅ 규칙 검증 완료"
```

#### 규칙 통계 스크립트
```bash
#!/bin/bash
# scripts/rules-stats.sh

echo "📊 Cursor Rules 통계"

# 총 규칙 수
total_rules=$(grep -c "###" .cursorrules)
echo "총 규칙 수: $total_rules"

# 새로운 규칙 수
new_rules=$(grep -c "🆕" .cursorrules)
echo "새로운 규칙 수: $new_rules"

# 언어별 규칙 수
python_rules=$(grep -c "```python" .cursorrules)
typescript_rules=$(grep -c "```typescript" .cursorrules)
echo "Python 규칙: $python_rules"
echo "TypeScript 규칙: $typescript_rules"
```

### 규칙 템플릿

#### 새로운 모듈 규칙 템플릿
```markdown
### 🆕 [모듈명] 모듈 개발 규칙

#### [모듈명] API 엔드포인트 설계
```python
# api/v1/endpoints/[module].py
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/[module]", tags=["[Module]"])

@router.post("/")
async def create_[module](
    data: [Module]Create,
    db: Session = Depends(get_db)
):
    """[모듈] 생성 API"""
    pass
```

#### [모듈명] 서비스 클래스 설계
```python
# services/[module].py
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class [Module]Service:
    """[모듈] 서비스 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def create_[module](self, data: [Module]Create) -> [Module]:
        """[모듈] 생성"""
        pass
```
```

## 🚨 긴급 규칙 변경

### 긴급 변경 조건
- [ ] 보안 취약점 발견
- [ ] 심각한 성능 이슈
- [ ] 프로덕션 장애
- [ ] 법적 요구사항

### 긴급 변경 프로세스
1. **즉시 적용**: 최소한의 검토 후 적용
2. **사후 검토**: 적용 후 상세 검토
3. **팀 공지**: 변경사항 즉시 공지
4. **모니터링**: 24시간 집중 모니터링

## 📈 규칙 효과 측정

### 측정 지표
- **코드 품질**: 코드 복잡도, 중복률, 테스트 커버리지
- **개발 효율성**: 개발 속도, 버그 발생률, 리뷰 시간
- **팀 만족도**: 규칙 준수율, 피드백 점수
- **시스템 안정성**: 장애 발생률, 성능 지표

### 개선 사이클
1. **측정**: 현재 상태 파악
2. **분석**: 문제점 식별
3. **개선**: 규칙 수정/추가
4. **적용**: 새로운 규칙 적용
5. **검증**: 개선 효과 확인

## 🔮 향후 계획

### 단기 계획 (1-3개월)
- [ ] 자동화 스크립트 완성
- [ ] 규칙 템플릿 확장
- [ ] 모니터링 대시보드 구축
- [ ] 팀 교육 프로그램 개발

### 중기 계획 (3-6개월)
- [ ] AI 기반 규칙 추천 시스템
- [ ] 실시간 규칙 위반 감지
- [ ] 규칙 효과 예측 모델
- [ ] 외부 프로젝트 벤치마킹

### 장기 계획 (6개월 이상)
- [ ] 업계 표준 규칙 수립
- [ ] 오픈소스 규칙 라이브러리
- [ ] 규칙 마켓플레이스 구축
- [ ] 글로벌 규칙 커뮤니티

---

**문서 버전**: 1.0  
**작성자**: CMA 개발팀  
**최종 검토**: 2025-01-23 