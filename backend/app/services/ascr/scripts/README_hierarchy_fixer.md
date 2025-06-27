# 계층 구조 수정 스크립트 사용법

## 📋 개요

이 스크립트들은 추출된 목차 구조의 계층 레벨, 부문 분류, 장 구조 등을 수정하는 도구입니다.

## 🚀 사용 가능한 스크립트

### 1. `fix_hierarchy_structure.py` (기본 버전)
- **기능**: 기본적인 계층 구조 수정
- **입력**: `output/toc_structure_20250624_220446.json`
- **출력**: `output/toc_structure_fixed.json`

### 2. `fix_hierarchy_structure_v2.py` (개선 버전)
- **기능**: 개선된 계층 구조 수정 (절 포함)
- **입력**: `output/toc_structure_20250624_220446.json`
- **출력**: `output/toc_structure_fixed_v2.json`

### 3. `fix_hierarchy_structure_final.py` (최종 버전)
- **기능**: 최종 개선된 계층 구조 수정
- **입력**: `output/toc_structure_20250624_220446.json`
- **출력**: `output/toc_structure_fixed_final.json`

### 4. `fix_hierarchy_structure_complete.py` (완전 버전) ⭐ **권장**
- **기능**: 완전한 계층 구조 수정 (모든 레벨 포함)
- **입력**: `output/toc_structure_20250624_220446.json`
- **출력**: `output/toc_structure_fixed_complete.json`

## 🔧 실행 방법

```bash
# 완전 버전 실행 (권장)
python scripts/fix_hierarchy_structure_complete.py

# 다른 버전 실행
python scripts/fix_hierarchy_structure.py
python scripts/fix_hierarchy_structure_v2.py
python scripts/fix_hierarchy_structure_final.py
```

## 📊 수정 내용

### 1. 계층 레벨 수정
- **레벨 0**: 부문 헤더 (공통부문, 토목부문, 건축부문, 기계설비부문, 유지관리부문)
- **레벨 1**: 장 (제1장, 제2장, ...)
- **레벨 2**: 절 (1-1, 1-2, 2-1, ...)
- **레벨 3**: 조/항목 (1-1-1, 1-1-2, ...)

### 2. 부문 분류 수정
페이지 번호를 기반으로 부문을 자동 분류:
- **공통부문**: 3~298페이지
- **토목부문**: 299~400페이지
- **건축부문**: 401~600페이지
- **기계설비부문**: 601~800페이지
- **유지관리부문**: 801~900페이지

### 3. 번호 체계 정규화
- 장 번호: "제1장" → "1"
- 절 번호: "1-1" 유지
- 조 번호: "1-1-1" 유지

### 4. 부모-자식 관계 수정
계층 구조에 따라 부모-자식 관계를 자동 설정

## 📈 결과 예시

### 수정 전
```json
{
  "number": "1-1",
  "title": "일반사항",
  "level": 2,  // 모든 항목이 level 2
  "section": "공통부문",
  "type": "unknown"
}
```

### 수정 후
```json
{
  "number": "1-1",
  "title": "일반사항",
  "level": 2,  // 올바른 level
  "section": "공통부문",
  "type": "section",
  "parent": "1",
  "children": []
}
```

## 📊 통계 출력

실행 후 다음과 같은 통계가 출력됩니다:

```
=== 계층 구조 수정 통계 ===
레벨별 항목 수:
  부문헤더 (레벨 0): 5개
  장 (레벨 1): 45개
  절 (레벨 2): 1045개

부문별 항목 수:
  건축부문: 194개
  공통부문: 271개
  기계설비부문: 300개
  유지관리부문: 141개
  토목부문: 184개

타입별 항목 수:
  chapter: 45개
  section: 1045개
  section_header: 5개

페이지 범위: 3 ~ 896
```

## 🔍 샘플 구조 출력

실행 후 처음 30개 항목의 계층 구조가 출력됩니다:

```
=== 샘플 구조 ===
공통부문 공통부문 (미분류) [section_header]
  1 적용기준 (공통부문) [chapter]
    1-1 일반사항 (공통부문) [section]
    1-1 목적 (공통부문) [section]
    1-2 적용범위 (공통부문) [section]
    ...
```

## ⚠️ 주의사항

1. **입력 파일 확인**: 실행 전 `output/toc_structure_20250624_220446.json` 파일이 존재하는지 확인
2. **백업**: 중요한 데이터는 실행 전 백업
3. **페이지 범위**: 부문별 페이지 범위는 실제 PDF에 맞게 조정 필요
4. **조/항목**: 원본 데이터에 조/항목(n-n-n 형태)이 없으면 level 3 항목이 생성되지 않음

## 🛠️ 커스터마이징

### 페이지 범위 수정
```python
self.section_page_ranges = {
    "공통부문": (3, 298),      # 실제 범위로 수정
    "토목부문": (299, 400),    # 실제 범위로 수정
    "건축부문": (401, 600),    # 실제 범위로 수정
    "기계설비부문": (601, 800), # 실제 범위로 수정
    "유지관리부문": (801, 900)  # 실제 범위로 수정
}
```

### 패턴 수정
```python
# 장 패턴 추가
self.chapter_patterns.append(r'^새로운장패턴')

# 절 패턴 추가
self.section_patterns.append(r'^새로운절패턴')

# 조/항목 패턴 추가
self.item_patterns.append(r'^새로운조패턴')
```

## 📝 로그

실행 중 다음과 같은 로그가 출력됩니다:

```
INFO:__main__:계층 구조 수정 시작: output/toc_structure_20250624_220446.json
INFO:__main__:총 1095개 항목 로드
INFO:__main__:계층 레벨 수정 완료
INFO:__main__:부문 분류 수정 완료
INFO:__main__:번호 체계 정규화 완료
INFO:__main__:부모-자식 관계 수정 완료
INFO:__main__:수정된 구조 저장 완료: output/toc_structure_fixed_complete.json
```

## ✅ 성공 메시지

성공적으로 완료되면 다음 메시지가 출력됩니다:

```
✅ 계층 구조 수정 완료!
📁 수정된 파일: output/toc_structure_fixed_complete.json
``` 