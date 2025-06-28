# 건설 관리 시스템 - 계층구조형 스키마 설명

## 🏗️ 전체 시스템 계층 구조

```
건설 관리 시스템 (CMA)
├── 1. 핵심 비즈니스 엔티티 (Core Business Entities)
│   ├── 1.1 계약 관리 (Contract Management)
│   │   ├── Contract (계약)
│   │   └── ContractDocument (계약 문서)
│   │
│   ├── 1.2 거래처 관리 (Vendor Management)
│   │   ├── Vendor (거래처)
│   │   └── VendorDocument (거래처 문서)
│   │
│   └── 1.3 인력 관리 (Labor Management)
│       ├── Labor (인력)
│       └── WorkLog (작업일지)
│
├── 2. 재무 관리 (Financial Management)
│   ├── FinancialRecord (재무 기록)
│   └── FinancialDocument (재무 문서)
│
└── 3. 공통 요소 (Common Elements)
    ├── BaseModel (기본 모델)
    └── 공통 필드들 (id, created_at, updated_at)
```

## 📊 상세 계층 구조

### **1단계: 핵심 비즈니스 엔티티**

#### **1.1 계약 관리 계층**
```
Contract (계약)
├── 기본 정보
│   ├── 계약명, 계약번호, 계약금액
│   ├── 계약일, 시작일, 종료일
│   └── 발주처, 상태, 설명
├── 관계 정보
│   ├── vendor_id (거래처 연결)
│   └── created_at, updated_at (시간 정보)
└── 하위 엔티티
    └── ContractDocument (계약 문서)
        ├── 문서 유형, 파일 경로
        ├── 파일명, 업로드일
        └── 설명
```

#### **1.2 거래처 관리 계층**
```
Vendor (거래처)
├── 기본 정보
│   ├── 거래처명, 사업자등록번호
│   ├── 대표자, 주소, 연락처
│   └── 이메일, 상태, 설명
├── 금융 정보
│   ├── 은행명, 계좌번호
│   └── bank_info (JSON 형태)
├── 문서 정보
│   └── documents (JSON 형태)
└── 하위 엔티티
    └── VendorDocument (거래처 문서)
        ├── 문서 유형, 파일 경로
        ├── 파일명, 업로드일
        └── 설명
```

#### **1.3 인력 관리 계층**
```
Labor (인력)
├── 기본 정보
│   ├── 이름, 전화번호, 주민번호
│   ├── 은행명, 계좌번호
│   └── 일당, 상태
├── 관계 정보
│   └── contract_id (계약 연결)
└── 하위 엔티티
    └── WorkLog (작업일지)
        ├── 작업일, 시작시간, 종료시간
        ├── 작업시간, 일당, 총액
        └── 설명, 상태
```

### **2단계: 재무 관리 계층**

```
FinancialRecord (재무 기록)
├── 기본 정보
│   ├── 거래일, 금액, 유형
│   ├── 카테고리, 설명
│   └── 결제방법, 상태
├── 관계 정보
│   ├── contract_id (계약 연결)
│   └── vendor_id (거래처 연결)
└── 하위 엔티티
    └── FinancialDocument (재무 문서)
        ├── 문서 유형, 파일 경로
        ├── 파일명, 업로드일
        └── 설명
```

### **3단계: 공통 요소 계층**

```
BaseModel (기본 모델)
├── 공통 필드
│   ├── id (UUID, Primary Key)
│   ├── created_at (생성일시)
│   └── updated_at (수정일시)
└── 공통 메서드
    └── __tablename__ (테이블명 자동 생성)
```

## 🔗 계층 간 관계 매핑

### **수직 관계 (상하 관계)**
```
1. Contract → ContractDocument
   - 1개 계약이 여러 문서를 가질 수 있음
   - 계약이 삭제되면 관련 문서도 삭제됨

2. Vendor → VendorDocument
   - 1개 거래처가 여러 문서를 가질 수 있음
   - 거래처가 삭제되면 관련 문서도 삭제됨

3. Labor → WorkLog
   - 1명의 인력이 여러 작업일지를 가질 수 있음
   - 인력이 삭제되면 관련 작업일지도 삭제됨

4. FinancialRecord → FinancialDocument
   - 1개의 재무기록이 여러 문서를 가질 수 있음
   - 재무기록이 삭제되면 관련 문서도 삭제됨
```

### **수평 관계 (동등 관계)**
```
1. Contract ↔ Vendor
   - 계약과 거래처는 1:1 관계
   - 계약이 거래처를 참조함

2. Contract ↔ FinancialRecord
   - 계약과 재무기록은 1:N 관계
   - 1개 계약이 여러 재무기록을 가질 수 있음

3. Vendor ↔ FinancialRecord
   - 거래처와 재무기록은 1:N 관계
   - 1개 거래처가 여러 재무기록을 가질 수 있음

4. Contract ↔ Labor
   - 계약과 인력은 1:N 관계
   - 1개 계약에 여러 인력이 참여할 수 있음
```

## 🎯 비즈니스 관점에서의 계층 구조

### **업무 프로세스별 계층**

#### **1. 계약 체결 프로세스**
```
1단계: 거래처 등록
   Vendor → VendorDocument

2단계: 계약 생성
   Contract → ContractDocument

3단계: 재무 기록
   FinancialRecord → FinancialDocument
```

#### **2. 인력 관리 프로세스**
```
1단계: 계약 확인
   Contract

2단계: 인력 등록
   Labor (contract_id 연결)

3단계: 작업 기록
   WorkLog (labor_id 연결)
```

#### **3. 재무 관리 프로세스**
```
1단계: 거래처/계약 확인
   Vendor, Contract

2단계: 재무 기록 생성
   FinancialRecord (vendor_id, contract_id 연결)

3단계: 증빙 문서 첨부
   FinancialDocument (financial_record_id 연결)
```

## 📋 계층별 데이터 접근 패턴

### **상위 계층 → 하위 계층 접근**
```sql
-- 계약의 모든 문서 조회
SELECT cd.* FROM contracts c
JOIN contract_documents cd ON c.id = cd.contract_id
WHERE c.id = :contract_id;

-- 거래처의 모든 문서 조회
SELECT vd.* FROM vendors v
JOIN vendor_documents vd ON v.id = vd.vendor_id
WHERE v.id = :vendor_id;
```

### **하위 계층 → 상위 계층 접근**
```sql
-- 문서의 계약 정보 조회
SELECT c.* FROM contract_documents cd
JOIN contracts c ON cd.contract_id = c.id
WHERE cd.id = :document_id;

-- 작업일지의 인력 정보 조회
SELECT l.* FROM work_logs wl
JOIN labors l ON wl.labor_id = l.id
WHERE wl.id = :work_log_id;
```

### **동등 계층 간 접근**
```sql
-- 계약의 모든 재무기록 조회
SELECT fr.* FROM contracts c
JOIN financial_records fr ON c.id = fr.contract_id
WHERE c.id = :contract_id;

-- 거래처의 모든 계약 조회
SELECT c.* FROM vendors v
JOIN contracts c ON v.id = c.vendor_id
WHERE v.id = :vendor_id;
``` 