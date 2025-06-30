# 데이터베이스 스키마 문서

## 테이블 구조

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

### contracts
계약 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 계약 고유 식별자 |
| contract_number | VARCHAR(50) | UNIQUE, NOT NULL | 계약 번호 |
| client_id | UUID | FK, NOT NULL | 거래처 ID |
| project_name | VARCHAR(255) | NOT NULL | 프로젝트명 |
| contract_amount | NUMERIC(15,2) | NOT NULL | 계약 금액 |
| start_date | DATE | NOT NULL | 시작일 |
| end_date | DATE | NULL | 종료일 |
| status | VARCHAR(20) | NOT NULL | 계약 상태 |
| contract_type | VARCHAR(50) | NOT NULL | 계약 유형 |
| created_by | UUID | FK, NOT NULL | 생성자 ID |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### workers
작업자 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 작업자 고유 식별자 |
| full_name | VARCHAR(100) | NOT NULL | 작업자 이름 |
| phone | VARCHAR(20) | NULL | 전화번호 |
| id_number | VARCHAR(20) | UNIQUE | 주민등록번호 |
| bank_account | VARCHAR(50) | NULL | 계좌번호 |
| bank_name | VARCHAR(50) | NULL | 은행명 |
| hourly_rate | NUMERIC(10,2) | NOT NULL | 시급 |
| is_active | BOOLEAN | DEFAULT TRUE | 재직 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### labor_costs
인건비 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 인건비 고유 식별자 |
| contract_id | UUID | FK, NOT NULL | 계약 ID |
| worker_id | UUID | FK, NOT NULL | 작업자 ID |
| work_date | DATE | NOT NULL | 작업일 |
| hours_worked | NUMERIC(5,2) | NOT NULL | 작업시간 |
| hourly_rate | NUMERIC(10,2) | NOT NULL | 시급 |
| total_amount | NUMERIC(15,2) | NOT NULL | 총액 |
| payment_status | VARCHAR(20) | DEFAULT 'pending' | 지급 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### revenues
수입 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 수입 고유 식별자 |
| contract_id | UUID | FK, NOT NULL | 계약 ID |
| amount | NUMERIC(15,2) | NOT NULL | 수입금액 |
| payment_date | DATE | NOT NULL | 수입일 |
| payment_type | VARCHAR(20) | NOT NULL | 지불 방식 |
| status | VARCHAR(20) | DEFAULT 'pending' | 상태 |
| description | TEXT | NULL | 비고 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### expenses
비용 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 비용 고유 식별자 |
| contract_id | UUID | FK, NOT NULL | 계약 ID |
| category | VARCHAR(50) | NOT NULL | 비용 카테고리 |
| amount | NUMERIC(15,2) | NOT NULL | 비용금액 |
| expense_date | DATE | NOT NULL | 지출일 |
| description | TEXT | NULL | 비고 |
| payment_status | VARCHAR(20) | DEFAULT 'pending' | 지급 상태 |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

### documents
문서 정보를 저장하는 테이블

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | UUID | PK | 문서 고유 식별자 |
| contract_id | UUID | FK, NOT NULL | 계약 ID |
| document_type | VARCHAR(50) | NOT NULL | 문서 유형 |
| file_name | VARCHAR(255) | NOT NULL | 파일명 |
| file_path | VARCHAR(255) | NOT NULL | 파일 경로 |
| file_size | INTEGER | NOT NULL | 파일 크기 |
| mime_type | VARCHAR(100) | NOT NULL | 파일 형식 |
| uploaded_by | UUID | FK, NOT NULL | 업로드한 사용자 ID |
| created_at | TIMESTAMP | NOT NULL | 생성 일시 |
| updated_at | TIMESTAMP | NOT NULL | 수정 일시 |

## 관계

### 외래 키 제약조건

1. contracts
   - client_id → clients.id
   - created_by → users.id

2. labor_costs
   - contract_id → contracts.id
   - worker_id → workers.id

3. revenues
   - contract_id → contracts.id

4. expenses
   - contract_id → contracts.id

5. documents
   - contract_id → contracts.id
   - uploaded_by → users.id

## 인덱스

1. users
   - email (UNIQUE)

2. clients
   - business_number (UNIQUE)

3. contracts
   - contract_number (UNIQUE)
   - client_id
   - created_by

4. workers
   - id_number (UNIQUE)

5. labor_costs
   - contract_id
   - worker_id
   - work_date

6. revenues
   - contract_id
   - payment_date

7. expenses
   - contract_id
   - expense_date

8. documents
   - contract_id
   - document_type 