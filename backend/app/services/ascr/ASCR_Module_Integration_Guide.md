# 📄 ASCR 모듈 통합 및 개발 지시서

## ✅ 목적
ASCR(Auto Specification & Cost Report)은 CMS 시스템의 설계 문서 자동화 기능을 담당하며, 다음과 같은 역할을 수행한다:

- 표준품셈 / 노임단가 / 제비율 PDF 자료를 구조화
- 구조화된 데이터를 엑셀 내역서로 자동 생성
- 향후 계약서 및 설계보고서 자동 작성 기능과 연계 가능

---

## 📁 디렉토리 구조 및 핵심 파일

```
backend/app/services/ascr/
├── __init__.py
├── models.py                  # 데이터 모델 정의 (Pydantic)
├── parser.py                  # PDF → 구조화 데이터
├── excel_generator.py         # Excel 자동 생성기
└── service.py                 # 전체 자동화 파이프라인 처리
```

---

## 🔧 주요 개발 목표

| 모듈명 | 설명 |
|--------|------|
| `parser.py` | PDF로부터 표준품셈, 노임단가, 제비율 정보를 추출하여 리스트(dict)로 반환 |
| `excel_generator.py` | 엑셀 템플릿에 데이터를 채워 넣는 기능 수행 |
| `service.py` | 전체 자동화 파이프라인을 통합하여 실행 |

---

## 🛠 AI에게 수행 지시 예시

```json
{
  "module": "ascr",
  "task": "표준품셈 PDF 파싱 기능 작성",
  "file": "parser.py",
  "function": "parse_standard_cost",
  "input": "PDF 파일 경로",
  "output": "일위대가 항목 리스트: [{category, item, unit, price, note}]"
}
```

또는

```json
{
  "module": "ascr",
  "task": "엑셀 템플릿에 노임단가 삽입 기능 구현",
  "file": "excel_generator.py",
  "function": "update_labor_rates_in_excel",
  "input": "노임단가 리스트",
  "output": "기존 엑셀 파일에 최신 노임단가 업데이트"
}
```

---

## 📌 통합 고려 사항

- 이 모듈은 CMS 시스템의 계약서/보고서/문서관리 기능과 연동됩니다.
- PDF → 데이터 → 엑셀로 흐름이 구성되며, 필요 시 CLI 또는 REST API화 예정
- 템플릿 엑셀 파일은 `/resources/templates/`에 저장 예정