# 공통 데이터베이스 스키마 설계

## 1. 프로젝트(공사) 기본 정보
```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,           -- 공사명
    code VARCHAR(50) UNIQUE,             -- 공사 코드
    description TEXT,                    -- 공사 설명
    status VARCHAR(50) NOT NULL,         -- 공사 상태
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 2. 계약 정보
```sql
CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    contract_number VARCHAR(50) UNIQUE,  -- 계약번호
    contract_date DATE NOT NULL,         -- 계약일
    contract_amount DECIMAL(15,2) NOT NULL, -- 계약금액
    client_id INTEGER REFERENCES clients(id), -- 발주처
    start_date DATE,                     -- 착공일
    completion_date DATE,                -- 준공일
    status VARCHAR(50) NOT NULL,         -- 계약 상태
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 3. 발주처 정보
```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,          -- 발주처명
    business_number VARCHAR(20) UNIQUE,  -- 사업자등록번호
    address TEXT,                        -- 주소
    contact_person VARCHAR(100),         -- 담당자
    contact_phone VARCHAR(20),           -- 연락처
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. 문서 관리
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    contract_id INTEGER REFERENCES contracts(id),
    document_type VARCHAR(50) NOT NULL,  -- 문서 유형 (계약서, 세금계산서 등)
    file_path VARCHAR(255) NOT NULL,     -- 파일 경로
    original_filename VARCHAR(255) NOT NULL, -- 원본 파일명
    file_size INTEGER NOT NULL,          -- 파일 크기
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 5. 진행상황 관리
```sql
CREATE TABLE progress (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    progress_percentage INTEGER NOT NULL, -- 진행률
    stage VARCHAR(100) NOT NULL,         -- 현재 단계
    description TEXT,                    -- 설명
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 6. 금액 관리
```sql
CREATE TABLE financial_records (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    contract_id INTEGER REFERENCES contracts(id),
    transaction_type VARCHAR(50) NOT NULL, -- 거래 유형
    amount DECIMAL(15,2) NOT NULL,        -- 금액
    transaction_date DATE NOT NULL,       -- 거래일
    description TEXT,                     -- 설명
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 7. 시스템 간 연관 관계

### 7.1 공사대장 시스템
- projects 테이블을 주 테이블로 사용
- contracts, documents, progress 테이블 연동
- 주로 공사 진행 상황과 문서 관리에 중점

### 7.2 계약관리 시스템
- contracts 테이블을 주 테이블로 사용
- projects, clients, documents 테이블 연동
- 주로 계약 정보와 금액 관리에 중점

### 7.3 회계관리 시스템
- financial_records 테이블을 주 테이블로 사용
- projects, contracts 테이블 연동
- 주로 금액 관리와 세금계산서 관리에 중점

## 8. 데이터 무결성 제약조건

### 8.1 외래 키 제약조건
- project_id는 projects 테이블의 id를 참조
- contract_id는 contracts 테이블의 id를 참조
- client_id는 clients 테이블의 id를 참조

### 8.2 유니크 제약조건
- projects.code
- contracts.contract_number
- clients.business_number

### 8.3 체크 제약조건
- progress_percentage는 0에서 100 사이
- contract_amount는 0보다 커야 함
- start_date는 completion_date보다 이전이어야 함

## 9. 인덱스 전략

### 9.1 기본 인덱스
- projects: name, code
- contracts: contract_number, project_id
- clients: business_number, name
- documents: project_id, document_type
- progress: project_id, created_at
- financial_records: project_id, transaction_date

### 9.2 복합 인덱스
- contracts: (project_id, status)
- documents: (project_id, contract_id, document_type)
- financial_records: (project_id, transaction_type, transaction_date)

## 10. 데이터 접근 패턴

### 10.1 공사대장 시스템
```sql
-- 공사 목록 조회
SELECT p.*, c.contract_number, c.contract_amount, pr.progress_percentage
FROM projects p
LEFT JOIN contracts c ON p.id = c.project_id
LEFT JOIN progress pr ON p.id = pr.project_id
WHERE p.status = 'active';

-- 공사 상세 정보 조회
SELECT p.*, c.*, cl.name as client_name, pr.*
FROM projects p
JOIN contracts c ON p.id = c.project_id
JOIN clients cl ON c.client_id = cl.id
LEFT JOIN progress pr ON p.id = pr.project_id
WHERE p.id = :project_id;
```

### 10.2 계약관리 시스템
```sql
-- 계약 목록 조회
SELECT c.*, p.name as project_name, cl.name as client_name
FROM contracts c
JOIN projects p ON c.project_id = p.id
JOIN clients cl ON c.client_id = cl.id
WHERE c.status = 'active';

-- 계약 상세 정보 조회
SELECT c.*, p.*, cl.*, d.*
FROM contracts c
JOIN projects p ON c.project_id = p.id
JOIN clients cl ON c.client_id = cl.id
LEFT JOIN documents d ON c.id = d.contract_id
WHERE c.id = :contract_id;
```

### 10.3 회계관리 시스템
```sql
-- 금액 거래 내역 조회
SELECT fr.*, p.name as project_name, c.contract_number
FROM financial_records fr
JOIN projects p ON fr.project_id = p.id
LEFT JOIN contracts c ON fr.contract_id = c.id
WHERE fr.transaction_date BETWEEN :start_date AND :end_date;

-- 프로젝트별 금액 집계
SELECT p.name, 
       SUM(CASE WHEN fr.transaction_type = 'income' THEN fr.amount ELSE 0 END) as total_income,
       SUM(CASE WHEN fr.transaction_type = 'expense' THEN fr.amount ELSE 0 END) as total_expense
FROM projects p
LEFT JOIN financial_records fr ON p.id = fr.project_id
GROUP BY p.id, p.name;
``` 