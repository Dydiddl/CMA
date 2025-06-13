# 설계 방향 문서

## 목표
건설회사 전용 관리 프로그램을 설치형으로 개발하되, 클라우드 DB와 연동하여 여러 컴퓨터에서 동시에 자료를 조회 및 처리할 수 있도록 설계합니다.

---

## 주요 기술 스택

- **Frontend (UI)**: React + TypeScript + Tauri
  - 설치형 GUI 구성
  - 직관적인 화면 구성, 빠른 반응성

- **Backend**: Python + FastAPI
  - 문서 처리 (엑셀, 한글 등)
  - Supabase 클라우드 DB 연동

- **Database**: Supabase (PostgreSQL 기반)
  - 보안 인증, REST API 제공
  - 사용자 권한 설정 가능

---

## 구조

```
├── frontend (Tauri)
├── backend (FastAPI)
└── Supabase (클라우드 DB)
```

> Tauri는 웹 UI를 설치형 프로그램으로 감쌉니다. FastAPI는 로컬에서 실행되며 클라우드 DB와 통신합니다.

---

## 개발 순서

1. DB 스키마 설계 및 Supabase 구축
2. FastAPI 기반 백엔드 API 및 문서 처리 기능 개발
3. React + Tauri 기반 UI 컴포넌트 개발
4. 프론트와 백엔드 연동
5. 배포 스크립트 제작 및 `.exe` 빌드 테스트

---

## 배포 방식

- 최종 결과물: `.exe` 형태의 설치 프로그램
- 실행 시, FastAPI와 Supabase에 자동 연결됨
- 설정 파일을 통해 DB 주소 및 인증 정보를 지정 가능

---

## 보안 및 확장성

- 초기에는 로컬 사용자 기반
- 추후 Supabase 인증 및 다중 사용자 관리 기능 추가 가능
- 내부망 전환 시 FastAPI 서버를 로컬 서버로 운영 가능
