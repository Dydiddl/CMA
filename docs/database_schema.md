# 데이터베이스 스키마 문서

## 1. 사용자 관리

### users
사용자 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 사용자 고유 식별자 |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 이메일 주소 |
| password_hash | VARCHAR(255) | NOT NULL | 암호화된 비밀번호 |
| full_name | VARCHAR(100) | NOT NULL | 사용자 이름 |
| role | VARCHAR(20) | NOT NULL | 사용자 역할 (admin, manager, employee) |
| department | VARCHAR(50) | NULL | 부서 |
| phone | VARCHAR(20) | NULL | 전화번호 |
| is_active | BOOLEAN | DEFAULT TRUE | 계정 활성화 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### permissions
사용자 권한 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 권한 고유 식별자 |
| name | VARCHAR(50) | NOT NULL | 권한 이름 |
| description | TEXT | NULL | 권한 설명 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### departments
부서 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 부서 고유 식별자 |
| name | VARCHAR(100) | NOT NULL | 부서명 |
| parent_id | UUID | FK | 상위 부서 ID |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

## 2. 거래처 관리

### clients
거래처 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 거래처 고유 식별자 |
| company_name | VARCHAR(255) | NOT NULL | 회사명 |
| business_number | VARCHAR(20) | UNIQUE | 사업자등록번호 |
| representative_name | VARCHAR(100) | NULL | 대표자명 |
| contact_person | VARCHAR(100) | NULL | 담당자명 |
| phone | VARCHAR(20) | NULL | 전화번호 |
| email | VARCHAR(255) | NULL | 이메일 |
| address | TEXT | NULL | 주소 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### client_contacts
거래처 담당자 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 담당자 고유 식별자 |
| client_id | UUID | FK, NOT NULL | 거래처 ID |
| name | VARCHAR(100) | NOT NULL | 담당자명 |
| position | VARCHAR(100) | NULL | 직책 |
| phone | VARCHAR(20) | NULL | 전화번호 |
| email | VARCHAR(255) | NULL | 이메일 |
| is_primary | BOOLEAN | DEFAULT FALSE | 주요 담당자 여부 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

## 3. 공사 관리

### projects
공사 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 공사 고유 식별자 |
| project_name | VARCHAR(255) | NOT NULL | 공사명 |
| project_code | VARCHAR(50) | UNIQUE | 공사 코드 |
| client_id | UUID | FK, NOT NULL | 발주처 ID |
| start_date | DATE | NOT NULL | 착공일 |
| end_date | DATE | NULL | 준공일 |
| status | VARCHAR(20) | NOT NULL | 공사 상태 |
| total_amount | NUMERIC(15,2) | NOT NULL | 공사 금액 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### contracts
계약 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 계약 고유 식별자 |
| project_id | UUID | FK, NOT NULL | 공사 ID |
| contract_number | VARCHAR(50) | UNIQUE, NOT NULL | 계약 번호 |
| contract_type | VARCHAR(50) | NOT NULL | 계약 유형 |
| contract_amount | NUMERIC(15,2) | NOT NULL | 계약 금액 |
| start_date | DATE | NOT NULL | 시작일 |
| end_date | DATE | NULL | 종료일 |
| status | VARCHAR(20) | NOT NULL | 계약 상태 |
| created_by | UUID | FK, NOT NULL | 생성자 ID |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### bids
입찰 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 입찰 고유 식별자 |
| project_id | UUID | FK, NOT NULL | 공사 ID |
| bid_number | VARCHAR(50) | UNIQUE, NOT NULL | 입찰 번호 |
| bid_type | VARCHAR(50) | NOT NULL | 입찰 유형 |
| bid_amount | NUMERIC(15,2) | NOT NULL | 입찰 금액 |
| bid_date | DATE | NOT NULL | 입찰일 |
| status | VARCHAR(20) | NOT NULL | 입찰 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

## 4. 계약 관리

### pre_contracts
계약 전 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 계약 전 고유 식별자 |
| project_id | UUID | FK, NOT NULL | 공사 ID |
| document_type | VARCHAR(50) | NOT NULL | 문서 유형 |
| document_number | VARCHAR(50) | NOT NULL | 문서 번호 |
| submission_date | DATE | NOT NULL | 제출일 |
| status | VARCHAR(20) | NOT NULL | 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### construction_starts
착공 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 착공 고유 식별자 |
| project_id | UUID | FK, NOT NULL | 공사 ID |
| start_date | DATE | NOT NULL | 착공일 |
| completion_date | DATE | NULL | 준공예정일 |
| status | VARCHAR(20) | NOT NULL | 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### completions
준공 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 준공 고유 식별자 |
| project_id | UUID | FK, NOT NULL | 공사 ID |
| completion_date | DATE | NOT NULL | 준공일 |
| inspection_date | DATE | NULL | 검사일 |
| status | VARCHAR(20) | NOT NULL | 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### claims
청구 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 청구 고유 식별자 |
| project_id | UUID | FK, NOT NULL | 공사 ID |
| claim_number | VARCHAR(50) | NOT NULL | 청구 번호 |
| claim_date | DATE | NOT NULL | 청구일 |
| amount | NUMERIC(15,2) | NOT NULL | 청구 금액 |
| status | VARCHAR(20) | NOT NULL | 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

## 5. 문서 관리

### documents
문서 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 문서 고유 식별자 |
| project_id | UUID | FK, NOT NULL | 공사 ID |
| document_type | VARCHAR(50) | NOT NULL | 문서 유형 |
| file_name | VARCHAR(255) | NOT NULL | 파일명 |
| file_path | VARCHAR(255) | NOT NULL | 파일 경로 |
| file_size | INTEGER | NOT NULL | 파일 크기 |
| mime_type | VARCHAR(100) | NOT NULL | 파일 형식 |
| uploaded_by | UUID | FK, NOT NULL | 업로드한 사용자 ID |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### document_templates
문서 양식 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 양식 고유 식별자 |
| template_name | VARCHAR(255) | NOT NULL | 양식명 |
| template_type | VARCHAR(50) | NOT NULL | 양식 유형 |
| file_path | VARCHAR(255) | NOT NULL | 파일 경로 |
| is_active | BOOLEAN | DEFAULT TRUE | 사용 여부 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

## 관계

### 외래 키 제약조건

1. users
   - department_id → departments.id

2. client_contacts
   - client_id → clients.id

3. projects
   - client_id → clients.id

4. contracts
   - project_id → projects.id
   - created_by → users.id

5. bids
   - project_id → projects.id

6. pre_contracts
   - project_id → projects.id

7. construction_starts
   - project_id → projects.id

8. completions
   - project_id → projects.id

9. claims
   - project_id → projects.id

10. documents
    - project_id → projects.id
    - uploaded_by → users.id

## 인덱스

1. users
   - email (UNIQUE)
   - department_id

2. clients
   - business_number (UNIQUE)

3. projects
   - project_code (UNIQUE)
   - client_id

4. contracts
   - contract_number (UNIQUE)
   - project_id

5. bids
   - bid_number (UNIQUE)
   - project_id

6. documents
   - project_id
   - document_type 