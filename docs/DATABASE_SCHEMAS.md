# 📊 CMA 데이터베이스 스키마 문서

## 📋 개요

CMA 시스템의 데이터베이스는 **PostgreSQL**을 기반으로 하며, **SQLAlchemy ORM**을 통해 관리됩니다. 모든 데이터 모델은 Pydantic 스키마를 통해 검증되며, API 요청/응답의 타입 안전성을 보장합니다.

## 🏗️ 데이터베이스 아키텍처

### 전체 ERD (Entity Relationship Diagram)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Users       │    │    Vendors      │    │    Clients      │
│                 │    │                 │    │                 │
│ - id            │    │ - id            │    │ - id            │
│ - username      │    │ - name          │    │ - name          │
│ - email         │    │ - contact       │    │ - contact       │
│ - role          │    │ - address       │    │ - address       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │    Projects     │
                    │                 │
                    │ - id            │
                    │ - name          │
                    │ - code          │
                    │ - status        │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │    Contracts    │
                    │                 │
                    │ - id            │
                    │ - project_id    │
                    │ - contract_number│
                    │ - contract_amount│
                    │ - client_id     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │ FinancialRecords│
                    │                 │
                    │ - id            │
                    │ - project_id    │
                    │ - contract_id   │
                    │ - amount        │
                    │ - type          │
                    │ - category      │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │      Labor      │
                    │                 │
                    │ - id            │
                    │ - contract_id   │
                    │ - worker_id     │
                    │ - hours         │
                    │ - rate          │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Workers     │
                    │                 │
                    │ - id            │
                    │ - name          │
                    │ - position      │
                    │ - hourly_rate   │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │    Documents    │
                    │                 │
                    │ - id            │
                    │ - project_id    │
                    │ - contract_id   │
                    │ - document_type │
                    │ - file_path     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │    Progress     │
                    │                 │
                    │ - id            │
                    │ - project_id    │
                    │ - progress_percentage│
                    │ - stage         │
                    └─────────────────┘
```

## 📊 데이터 모델 상세

### 1. 프로젝트 관리 (Projects)

#### Project 모델
```python
class Project(BaseModel):
    """프로젝트(공사) 모델"""
    __tablename__ = "projects"
    
    # 기본 정보
    name = Column(String(255), nullable=False, index=True, comment="공사명")
    code = Column(String(50), unique=True, nullable=False, index=True, comment="공사 코드")
    description = Column(Text, nullable=True, comment="공사 설명")
    status = Column(String(50), nullable=False, default="진행중", comment="공사 상태")
    
    # 관계 설정
    contracts = relationship("Contract", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="project", cascade="all, delete-orphan")
    financial_records = relationship("FinancialRecord", back_populates="project", cascade="all, delete-orphan")
```

#### 프로젝트 상태 정의
```python
PROJECT_STATUS = {
    "PLANNING": "기획중",
    "ACTIVE": "진행중", 
    "COMPLETED": "완료",
    "CANCELLED": "취소",
    "SUSPENDED": "중단"
}
```

### 2. 계약 관리 (Contracts)

#### Contract 모델
```python
class Contract(BaseModel):
    """계약 모델"""
    __tablename__ = "contracts"
    
    # 기본 정보
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="프로젝트 ID")
    contract_number = Column(String(50), unique=True, nullable=False, index=True, comment="계약번호")
    contract_date = Column(Date, nullable=False, comment="계약일")
    contract_amount = Column(Decimal(15,2), nullable=False, comment="계약금액")
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, comment="발주처 ID")
    start_date = Column(Date, nullable=True, comment="착공일")
    completion_date = Column(Date, nullable=True, comment="준공일")
    status = Column(String(50), nullable=False, default="진행중", comment="계약 상태")
    
    # 관계 설정
    project = relationship("Project", back_populates="contracts")
    client = relationship("Client", back_populates="contracts")
    documents = relationship("Document", back_populates="contract", cascade="all, delete-orphan")
    financial_records = relationship("FinancialRecord", back_populates="contract", cascade="all, delete-orphan")
    labor_records = relationship("Labor", back_populates="contract", cascade="all, delete-orphan")
```

#### 계약 상태 정의
```python
CONTRACT_STATUS = {
    "DRAFT": "초안",
    "ACTIVE": "진행중", 
    "COMPLETED": "완료",
    "CANCELLED": "취소",
    "SUSPENDED": "중단"
}
```

### 3. 발주처 관리 (Clients)

#### Client 모델
```python
class Client(BaseModel):
    """발주처 모델"""
    __tablename__ = "clients"
    
    # 기본 정보
    name = Column(String(255), nullable=False, index=True, comment="발주처명")
    business_number = Column(String(20), unique=True, nullable=False, comment="사업자등록번호")
    address = Column(Text, nullable=True, comment="주소")
    contact_person = Column(String(100), nullable=True, comment="담당자")
    contact_phone = Column(String(20), nullable=True, comment="연락처")
    
    # 관계 설정
    contracts = relationship("Contract", back_populates="client", cascade="all, delete-orphan")
```

### 4. 거래처 관리 (Vendors)

#### Vendor 모델
```python
class Vendor(BaseModel):
    """거래처 모델"""
    __tablename__ = "vendors"
    
    # 기본 정보
    name = Column(String(255), nullable=False, index=True, comment="거래처명")
    business_number = Column(String(20), unique=True, nullable=False, comment="사업자등록번호")
    address = Column(Text, nullable=True, comment="주소")
    contact_person = Column(String(100), nullable=True, comment="담당자")
    contact_phone = Column(String(20), nullable=True, comment="연락처")
    
    # 관계 설정
    financial_records = relationship("FinancialRecord", back_populates="vendor", cascade="all, delete-orphan")
```

### 5. 재무 관리 (Financial)

#### FinancialRecord 모델
```python
class FinancialRecord(BaseModel):
    """재무 기록 모델"""
    __tablename__ = "financial_records"
    
    # 기본 정보
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="프로젝트 ID")
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=True, comment="계약 ID")
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True, comment="거래처 ID")
    transaction_type = Column(String(50), nullable=False, comment="거래 유형")
    amount = Column(Decimal(15,2), nullable=False, comment="금액")
    transaction_date = Column(Date, nullable=False, comment="거래일")
    description = Column(Text, nullable=True, comment="설명")
    
    # 관계 설정
    project = relationship("Project", back_populates="financial_records")
    contract = relationship("Contract", back_populates="financial_records")
    vendor = relationship("Vendor", back_populates="financial_records")
```

#### 재무 카테고리 정의
```python
TRANSACTION_TYPES = {
    "INCOME": "수입",
    "EXPENSE": "지출"
}

FINANCIAL_CATEGORIES = {
    "MATERIAL": "자재비",
    "LABOR": "노무비", 
    "EQUIPMENT": "장비비",
    "OVERHEAD": "경비",
    "PROFIT": "이익",
    "OTHER": "기타"
}

PAYMENT_METHODS = {
    "CASH": "현금",
    "BANK_TRANSFER": "계좌이체",
    "CARD": "카드",
    "CHECK": "수표",
    "OTHER": "기타"
}

TRANSACTION_STATUS = {
    "PENDING": "미지급",
    "PAID": "지급완료",
    "CANCELLED": "취소",
    "OVERDUE": "연체"
}
```

### 6. 노무 관리 (Labor)

#### Labor 모델
```python
class Labor(BaseModel):
    """노무 기록 모델"""
    __tablename__ = "labor_records"
    
    # 기본 정보
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False, comment="계약 ID")
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False, comment="근로자 ID")
    work_date = Column(Date, nullable=False, comment="작업일")
    hours_worked = Column(Float, nullable=False, comment="작업 시간")
    hourly_rate = Column(Decimal(10,2), nullable=False, comment="시급")
    total_amount = Column(Decimal(15,2), nullable=False, comment="총 금액")
    work_type = Column(String(100), nullable=True, comment="작업 유형")
    description = Column(Text, nullable=True, comment="작업 설명")
    status = Column(String(50), default="미지급", comment="지급 상태")
    
    # 관계 설정
    contract = relationship("Contract", back_populates="labor_records")
    worker = relationship("Worker", back_populates="labor_records")
```

#### Worker 모델
```python
class Worker(BaseModel):
    """근로자 모델"""
    __tablename__ = "workers"
    
    # 기본 정보
    name = Column(String(255), nullable=False, index=True, comment="근로자명")
    position = Column(String(100), nullable=True, comment="직종")
    hourly_rate = Column(Decimal(10,2), default=0.0, comment="시급")
    contact = Column(String(100), nullable=True, comment="연락처")
    address = Column(Text, nullable=True, comment="주소")
    hire_date = Column(Date, nullable=True, comment="고용일")
    status = Column(String(50), default="활성", comment="상태")
    
    # 관계 설정
    labor_records = relationship("Labor", back_populates="worker", cascade="all, delete-orphan")
```

#### 근로자 상태 정의
```python
WORKER_STATUS = {
    "ACTIVE": "활성",
    "INACTIVE": "비활성",
    "RESIGNED": "퇴사"
}

WORK_TYPES = {
    "GENERAL": "일반공사",
    "SPECIAL": "특수공사",
    "MANAGEMENT": "관리업무",
    "OTHER": "기타"
}
```

### 7. 문서 관리 (Documents)

#### Document 모델
```python
class Document(BaseModel):
    """문서 모델"""
    __tablename__ = "documents"
    
    # 기본 정보
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="프로젝트 ID")
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=True, comment="계약 ID")
    document_type = Column(String(50), nullable=False, comment="문서 유형")
    file_path = Column(String(255), nullable=False, comment="파일 경로")
    original_filename = Column(String(255), nullable=False, comment="원본 파일명")
    file_size = Column(Integer, nullable=False, comment="파일 크기")
    uploaded_at = Column(DateTime, default=datetime.utcnow, comment="업로드 일시")
    
    # 관계 설정
    project = relationship("Project", back_populates="documents")
    contract = relationship("Contract", back_populates="documents")
```

#### 문서 유형 정의
```python
DOCUMENT_TYPES = {
    "CONTRACT": "계약서",
    "TAX_INVOICE": "세금계산서",
    "PROGRESS_REPORT": "진행보고서",
    "COMPLETION_REPORT": "완료보고서",
    "DRAWING": "도면",
    "SPECIFICATION": "시방서",
    "OTHER": "기타"
}
```

### 8. 진행상황 관리 (Progress)

#### Progress 모델
```python
class Progress(BaseModel):
    """진행상황 모델"""
    __tablename__ = "progress"
    
    # 기본 정보
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="프로젝트 ID")
    progress_percentage = Column(Integer, nullable=False, comment="진행률")
    stage = Column(String(100), nullable=False, comment="현재 단계")
    description = Column(Text, nullable=True, comment="설명")
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 일시")
    
    # 관계 설정
    project = relationship("Project", back_populates="progress")
```

#### 진행 단계 정의
```python
PROGRESS_STAGES = {
    "PLANNING": "기획",
    "DESIGN": "설계",
    "CONSTRUCTION": "시공",
    "INSPECTION": "검사",
    "COMPLETION": "완료"
}
```

## 🔗 데이터 무결성 제약조건

### 외래 키 제약조건
- `contracts.project_id` → `projects.id`
- `contracts.client_id` → `clients.id`
- `financial_records.project_id` → `projects.id`
- `financial_records.contract_id` → `contracts.id`
- `financial_records.vendor_id` → `vendors.id`
- `labor_records.contract_id` → `contracts.id`
- `labor_records.worker_id` → `workers.id`
- `documents.project_id` → `projects.id`
- `documents.contract_id` → `contracts.id`
- `progress.project_id` → `projects.id`

### 유니크 제약조건
- `projects.code`
- `contracts.contract_number`
- `clients.business_number`
- `vendors.business_number`

### 체크 제약조건
- `progress.progress_percentage`: 0 ≤ progress_percentage ≤ 100
- `contracts.contract_amount`: contract_amount > 0
- `contracts.start_date` ≤ `contracts.completion_date`
- `labor_records.hours_worked`: hours_worked > 0
- `labor_records.hourly_rate`: hourly_rate ≥ 0

## 📈 인덱스 전략

### 기본 인덱스
- `projects`: `name`, `code`, `status`
- `contracts`: `contract_number`, `project_id`, `status`
- `clients`: `business_number`, `name`
- `vendors`: `business_number`, `name`
- `workers`: `name`, `status`
- `documents`: `project_id`, `document_type`
- `progress`: `project_id`, `created_at`
- `financial_records`: `project_id`, `transaction_date`, `transaction_type`
- `labor_records`: `contract_id`, `work_date`, `worker_id`

### 복합 인덱스
- `contracts`: `(project_id, status)`
- `documents`: `(project_id, contract_id, document_type)`
- `financial_records`: `(project_id, transaction_type, transaction_date)`
- `labor_records`: `(contract_id, work_date, worker_id)`

## 🔍 데이터 접근 패턴

### 1. 공사대장 시스템
```sql
-- 공사 목록 조회
SELECT p.*, c.contract_number, c.contract_amount, pr.progress_percentage
FROM projects p
LEFT JOIN contracts c ON p.id = c.project_id
LEFT JOIN progress pr ON p.id = pr.project_id
WHERE p.status = 'ACTIVE';

-- 공사 상세 정보 조회
SELECT p.*, c.*, cl.name as client_name, pr.*
FROM projects p
JOIN contracts c ON p.id = c.project_id
JOIN clients cl ON c.client_id = cl.id
LEFT JOIN progress pr ON p.id = pr.project_id
WHERE p.id = :project_id;
```

### 2. 계약관리 시스템
```sql
-- 계약 목록 조회
SELECT c.*, p.name as project_name, cl.name as client_name
FROM contracts c
JOIN projects p ON c.project_id = p.id
JOIN clients cl ON c.client_id = cl.id
WHERE c.status = 'ACTIVE';

-- 계약 상세 정보 조회
SELECT c.*, p.*, cl.*, d.*
FROM contracts c
JOIN projects p ON c.project_id = p.id
JOIN clients cl ON c.client_id = cl.id
LEFT JOIN documents d ON c.id = d.contract_id
WHERE c.id = :contract_id;
```

### 3. 회계관리 시스템
```sql
-- 금액 거래 내역 조회
SELECT fr.*, p.name as project_name, c.contract_number
FROM financial_records fr
JOIN projects p ON fr.project_id = p.id
LEFT JOIN contracts c ON fr.contract_id = c.id
WHERE fr.transaction_date BETWEEN :start_date AND :end_date;

-- 프로젝트별 금액 집계
SELECT p.name, 
       SUM(CASE WHEN fr.transaction_type = 'INCOME' THEN fr.amount ELSE 0 END) as total_income,
       SUM(CASE WHEN fr.transaction_type = 'EXPENSE' THEN fr.amount ELSE 0 END) as total_expense
FROM projects p
LEFT JOIN financial_records fr ON p.id = fr.project_id
GROUP BY p.id, p.name;
```

### 4. 노무관리 시스템
```sql
-- 근로자별 작업 내역 조회
SELECT w.name, lr.*, c.contract_number, p.name as project_name
FROM labor_records lr
JOIN workers w ON lr.worker_id = w.id
JOIN contracts c ON lr.contract_id = c.id
JOIN projects p ON c.project_id = p.id
WHERE lr.work_date BETWEEN :start_date AND :end_date;

-- 계약별 노무비 집계
SELECT c.contract_number, 
       SUM(lr.total_amount) as total_labor_cost,
       SUM(lr.hours_worked) as total_hours
FROM labor_records lr
JOIN contracts c ON lr.contract_id = c.id
GROUP BY c.id, c.contract_number;
```

## 🚀 성능 최적화

### 1. 쿼리 최적화
- **인덱스 활용**: 자주 조회되는 컬럼에 인덱스 생성
- **조인 최적화**: 필요한 테이블만 조인
- **서브쿼리 최소화**: 가능한 경우 JOIN 사용

### 2. 데이터 파티셔닝
- **시간 기반 파티셔닝**: `financial_records`, `labor_records` 테이블
- **프로젝트 기반 파티셔닝**: 대용량 프로젝트의 경우

### 3. 캐싱 전략
- **Redis 캐싱**: 자주 조회되는 데이터 캐싱
- **애플리케이션 캐싱**: ORM 쿼리 결과 캐싱

## 🔒 보안 고려사항

### 1. 데이터 암호화
- **민감 정보 암호화**: 개인정보, 계약 정보
- **파일 암호화**: 업로드된 문서 파일

### 2. 접근 제어
- **사용자 권한 관리**: 역할 기반 접근 제어
- **데이터 접근 로그**: 모든 데이터 접근 기록

### 3. 백업 및 복구
- **정기 백업**: 일일/주간 백업
- **재해 복구**: 장애 시 복구 계획

---

**마지막 업데이트**: 2025년 1월 23일
**문서 버전**: v3.0 