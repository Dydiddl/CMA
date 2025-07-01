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
                    │    Contracts    │
                    │                 │
                    │ - id            │
                    │ - name          │
                    │ - contract_number│
                    │ - contract_amount│
                    │ - vendor_id     │
                    │ - client_name   │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │ FinancialRecords│
                    │                 │
                    │ - id            │
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
```

## 📊 데이터 모델 상세

### 1. 계약 관리 (Contracts)

#### Contract 모델
```python
class Contract(BaseModel):
    """계약 모델"""
    __tablename__ = "contracts"
    
    # 기본 정보
    name = Column(String(255), nullable=False, index=True, comment="계약명")
    contract_number = Column(String(50), unique=True, nullable=False, index=True, comment="계약번호")
    contract_amount = Column(Float, nullable=False, comment="계약금액")
    contract_date = Column(DateTime, nullable=False, comment="계약일")
    start_date = Column(DateTime, nullable=True, comment="시작일")
    end_date = Column(DateTime, nullable=True, comment="종료일")
    
    # 발주처 정보
    client_name = Column(String(255), nullable=False, comment="발주처명")
    client_contact = Column(String(100), nullable=True, comment="발주처 연락처")
    
    # 상태 및 설명
    status = Column(String(50), nullable=False, default="진행중", comment="계약 상태")
    description = Column(Text, nullable=True, comment="계약 설명")
    
    # 외래키
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False, comment="거래처 ID")
```

#### Contract 스키마
```python
class ContractBase(BaseModel):
    """계약 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=255, description="계약명")
    contract_number: str = Field(..., min_length=1, max_length=50, description="계약번호")
    contract_amount: float = Field(..., gt=0, description="계약금액")
    contract_date: datetime = Field(..., description="계약일")
    start_date: Optional[datetime] = Field(None, description="시작일")
    end_date: Optional[datetime] = Field(None, description="종료일")
    client_name: str = Field(..., min_length=1, max_length=255, description="발주처명")
    client_contact: Optional[str] = Field(None, max_length=100, description="발주처 연락처")
    status: str = Field(default="진행중", description="계약 상태")
    description: Optional[str] = Field(None, description="계약 설명")
    vendor_id: str = Field(..., description="거래처 ID")
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

### 2. 재무 관리 (Financial)

#### FinancialRecord 모델
```python
class FinancialRecord(BaseModel):
    """재무 기록 모델"""
    __tablename__ = "financial_records"
    
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    transaction_date = Column(Date)
    amount = Column(Float)
    type = Column(String)  # 수입, 지출
    category = Column(String)  # 자재비, 노무비, 경비 등
    description = Column(Text)
    payment_method = Column(String)  # 현금, 계좌이체, 카드 등
    status = Column(String)  # 미지급, 지급완료 등
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
```

#### 재무 카테고리 정의
```python
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

### 3. 노무 관리 (Labor)

#### Labor 모델
```python
class Labor(BaseModel):
    """노무 기록 모델"""
    __tablename__ = "labor_records"
    
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    worker_id = Column(Integer, ForeignKey("workers.id"))
    work_date = Column(Date)
    hours_worked = Column(Float)
    hourly_rate = Column(Float)
    total_amount = Column(Float)
    work_type = Column(String)  # 일반공사, 특수공사 등
    description = Column(Text)
    status = Column(String)  # 미지급, 지급완료 등
```

#### Worker 모델
```python
class Worker(BaseModel):
    """근로자 모델"""
    __tablename__ = "workers"
    
    name = Column(String(255), nullable=False)
    position = Column(String(100))  # 직종
    hourly_rate = Column(Float, default=0.0)
    contact = Column(String(100))
    address = Column(Text)
    hire_date = Column(Date)
    status = Column(String(50), default="활성")  # 활성, 비활성, 퇴사
```

### 4. 거래처 관리 (Vendors)

#### Vendor 모델
```python
class Vendor(BaseModel):
    """거래처 모델"""
    __tablename__ = "vendors"
    
    name = Column(String(255), nullable=False, index=True)
    contact_person = Column(String(100))
    contact_number = Column(String(100))
    email = Column(String(255))
    address = Column(Text)
    business_number = Column(String(50))  # 사업자번호
    vendor_type = Column(String(50))  # 자재업체, 하청업체 등
    status = Column(String(50), default="활성")
```

### 5. 문서 관리 (Documents)

#### ContractDocument 모델
```python
class ContractDocument(BaseModel):
    """계약 문서 모델"""
    __tablename__ = "contract_documents"
    
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    document_type = Column(String(50), nullable=False)  # 계약서, 도면, 명세서 등
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
```

## 🔗 관계 정의

### 1. 계약 관련 관계
```python
# Contract 모델의 관계
vendor = relationship("Vendor", back_populates="contracts")
documents = relationship("ContractDocument", back_populates="contract", cascade="all, delete-orphan")
financial_records = relationship("FinancialRecord", back_populates="contract", cascade="all, delete-orphan")
labors = relationship("Labor", back_populates="contract", cascade="all, delete-orphan")
```

### 2. 재무 관련 관계
```python
# FinancialRecord 모델의 관계
contract = relationship("Contract", back_populates="financial_records")
vendor = relationship("Vendor", back_populates="financial_records")
documents = relationship("FinancialDocument", back_populates="financial_record", cascade="all, delete-orphan")
```

### 3. 노무 관련 관계
```python
# Labor 모델의 관계
contract = relationship("Contract", back_populates="labors")
worker = relationship("Worker", back_populates="labor_records")
```

## 📋 데이터 검증 규칙

### 1. 계약 데이터 검증
```python
@validator('end_date')
def validate_end_date(cls, v, values):
    """종료일 검증"""
    if v and 'start_date' in values and values['start_date']:
        if v <= values['start_date']:
            raise ValueError('종료일은 시작일보다 늦어야 합니다.')
    return v

@validator('contract_amount')
def validate_contract_amount(cls, v):
    """계약금액 검증"""
    if v <= 0:
        raise ValueError('계약금액은 0보다 커야 합니다.')
    return v
```

### 2. 재무 데이터 검증
```python
@validator('amount')
def validate_amount(cls, v):
    """금액 검증"""
    if v <= 0:
        raise ValueError('금액은 0보다 커야 합니다.')
    return v

@validator('type')
def validate_transaction_type(cls, v):
    """거래 유형 검증"""
    allowed_types = ['수입', '지출']
    if v not in allowed_types:
        raise ValueError(f'거래 유형은 {allowed_types} 중 하나여야 합니다.')
    return v
```

### 3. 노무 데이터 검증
```python
@validator('hours_worked')
def validate_hours_worked(cls, v):
    """근무 시간 검증"""
    if v <= 0 or v > 24:
        raise ValueError('근무 시간은 0보다 크고 24 이하여야 합니다.')
    return v

@validator('hourly_rate')
def validate_hourly_rate(cls, v):
    """시급 검증"""
    if v < 0:
        raise ValueError('시급은 0 이상이어야 합니다.')
    return v
```

## 🔄 데이터 마이그레이션

### 마이그레이션 파일 구조
```
migrations/
├── versions/
│   ├── 001_initial_schema.py
│   ├── 002_add_financial_tables.py
│   ├── 003_add_labor_tables.py
│   └── 004_add_document_tables.py
├── env.py
├── script.py.mako
└── alembic.ini
```

### 마이그레이션 실행
```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Add new table"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1

# 마이그레이션 상태 확인
alembic current
alembic history
```

## 📊 인덱스 최적화

### 성능 최적화를 위한 인덱스
```sql
-- 계약 테이블 인덱스
CREATE INDEX idx_contracts_contract_number ON contracts(contract_number);
CREATE INDEX idx_contracts_vendor_id ON contracts(vendor_id);
CREATE INDEX idx_contracts_status ON contracts(status);
CREATE INDEX idx_contracts_contract_date ON contracts(contract_date);

-- 재무 기록 테이블 인덱스
CREATE INDEX idx_financial_records_contract_id ON financial_records(contract_id);
CREATE INDEX idx_financial_records_transaction_date ON financial_records(transaction_date);
CREATE INDEX idx_financial_records_type ON financial_records(type);
CREATE INDEX idx_financial_records_category ON financial_records(category);

-- 노무 기록 테이블 인덱스
CREATE INDEX idx_labor_records_contract_id ON labor_records(contract_id);
CREATE INDEX idx_labor_records_worker_id ON labor_records(worker_id);
CREATE INDEX idx_labor_records_work_date ON labor_records(work_date);

-- 거래처 테이블 인덱스
CREATE INDEX idx_vendors_name ON vendors(name);
CREATE INDEX idx_vendors_vendor_type ON vendors(vendor_type);
```

## 🔒 데이터 보안

### 민감 데이터 암호화
```python
# 민감한 정보 암호화
from cryptography.fernet import Fernet

class EncryptedField:
    """암호화된 필드"""
    
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """데이터 암호화"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """데이터 복호화"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

### 접근 권한 관리
```python
# 데이터 접근 권한
DATA_ACCESS_PERMISSIONS = {
    "ADMIN": ["READ", "WRITE", "DELETE", "MANAGE_USERS"],
    "MANAGER": ["READ", "WRITE", "DELETE"],
    "USER": ["READ", "WRITE"],
    "VIEWER": ["READ"]
}
```

## 📈 데이터 백업 및 복구

### 백업 전략
```python
# 자동 백업 설정
BACKUP_CONFIG = {
    "schedule": "0 2 * * *",  # 매일 새벽 2시
    "retention_days": 30,
    "backup_path": "/backups",
    "compression": True
}
```

### 복구 절차
```bash
# 데이터베이스 백업
pg_dump -h localhost -U username -d cma_db > backup.sql

# 데이터베이스 복구
psql -h localhost -U username -d cma_db < backup.sql
```

이 스키마 설계를 통해 **확장 가능하고 유지보수하기 쉬운** 데이터베이스 구조를 구축할 수 있습니다. 