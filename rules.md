# CMA 프로젝트 규칙 (ASCR 모듈 포함)

## 1. 전체 구조 및 역할
- 본 프로젝트는 CMA(건설관리 자동화) 시스템의 일부로, ASCR(Automated Standard Construction Report) 모듈을 포함한다.
- ASCR는 표준품셈/노임단가/제비율 PDF → 데이터화 → 엑셀 자동화에 중점을 둔다.

## 2. ASCR 모듈 개발 규칙
- PDF(표준품셈, 노임단가, 제비율 등) → 텍스트/구조화 데이터 추출 시 pypdf, pandas, openpyxl 등 최신 라이브러리만 사용
- 연도별 데이터 버전 관리 필수 (예: 표준품셈_2025, 노임단가_Q2_2025)
- 엑셀 자동작성 시 기존 템플릿 구조(서식) 반드시 유지
- 자동화가 어려운 항목(자재단가 등)은 사용자 수동 입력 UI로 보완
- 데이터 처리 파이프라인은 반자동 구조(자동+수동 혼합)로 설계
- 원가계산서, 수량산출 등도 자동화 대상에 포함
- 향후 머신러닝 기반 고도화(공정 추천 등) 확장 고려
- 모든 데이터/문서 처리 로직은 docs/ 및 backend/app/services/ascr/에 문서화

## 3. 기술 스택 및 연동
- 백엔드: Python(FastAPI, pypdf, openpyxl, pandas, SQLAlchemy)
- 프론트엔드: React, TypeScript, MUI, Tauri
- 데이터베이스: PostgreSQL, Supabase(프로덕션)
- 배포: Tauri(데스크탑), Docker(서버)

## 4. 기타
- ASCR 모듈은 계약/노무/재무 등 CMA의 다른 모듈과 연동됨
- 모든 규칙은 기존 CMA 규칙과 충돌하지 않게 유지
- 상세 명세 및 예시는 docs/ 및 backend/app/services/ascr/ 참고 