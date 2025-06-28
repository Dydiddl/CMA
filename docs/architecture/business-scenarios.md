# 건설 관리 시스템 - 비즈니스 시나리오 기반 스키마 설명

## 🎯 실제 업무 시나리오로 이해하는 데이터 관계

### **시나리오 1: 새로운 건설 프로젝트 시작**

#### **1단계: 거래처 등록**
```
업무: 새로운 발주처(거래처) 등록
관련 테이블: Vendor, VendorDocument

데이터 흐름:
1. Vendor 테이블에 거래처 기본정보 입력
   - 거래처명: "ABC건설(주)"
   - 사업자등록번호: "123-45-67890"
   - 대표자: "김철수"
   - 주소: "서울시 강남구..."
   - 연락처: "02-1234-5678"

2. VendorDocument 테이블에 필수 문서 업로드
   - 사업자등록증: "business_license.pdf"
   - 통장사본: "bank_copy.pdf"
   - 기타 서류: "other_docs.pdf"

관계 설명:
- 1개 거래처(Vendor) → 여러 문서(VendorDocument)
- 거래처가 삭제되면 관련 문서도 함께 삭제됨
```

#### **2단계: 계약 체결**
```
업무: 발주처와 계약 체결
관련 테이블: Contract, ContractDocument

데이터 흐름:
1. Contract 테이블에 계약정보 입력
   - 계약명: "강남구 아파트 신축공사"
   - 계약번호: "CON-2024-001"
   - 계약금액: 1,000,000,000원
   - 계약일: 2024-01-15
   - 시작일: 2024-02-01
   - 종료일: 2024-12-31
   - vendor_id: "ABC건설(주)의 ID"

2. ContractDocument 테이블에 계약 관련 문서 업로드
   - 계약서: "contract_agreement.pdf"
   - 견적서: "quotation.xlsx"
   - 명세서: "specifications.pdf"

관계 설명:
- 1개 계약(Contract) → 여러 문서(ContractDocument)
- 계약이 거래처(Vendor)를 참조함
- 계약이 삭제되면 관련 문서도 함께 삭제됨
```

#### **3단계: 인력 등록**
```
업무: 프로젝트에 참여할 인력 등록
관련 테이블: Labor

데이터 흐름:
1. Labor 테이블에 인력정보 입력
   - 이름: "박영희"
   - 전화번호: "010-1234-5678"
   - 주민번호: "900101-1234567"
   - 은행명: "국민은행"
   - 계좌번호: "123-456-789012"
   - 일당: 150,000원
   - contract_id: "강남구 아파트 신축공사 계약 ID"

관계 설명:
- 1개 계약(Contract) → 여러 인력(Labor)
- 인력은 특정 계약에 소속됨
- 계약이 삭제되면 관련 인력도 함께 삭제됨
```

### **시나리오 2: 일일 작업 관리**

#### **1단계: 작업일지 작성**
```
업무: 인력별 일일 작업 기록
관련 테이블: WorkLog

데이터 흐름:
1. WorkLog 테이블에 작업정보 입력
   - labor_id: "박영희의 ID"
   - 작업일: 2024-02-15
   - 시작시간: 08:00
   - 종료시간: 18:00
   - 작업시간: 10시간
   - 일당: 150,000원
   - 총액: 1,500,000원 (10시간 × 150,000원)
   - 설명: "기초공사 - 철근 배근 작업"
   - 상태: "작업완료"

관계 설명:
- 1명의 인력(Labor) → 여러 작업일지(WorkLog)
- 작업일지는 특정 인력에 소속됨
- 인력이 삭제되면 관련 작업일지도 함께 삭제됨
```

### **시나리오 3: 재무 관리**

#### **1단계: 수입 기록**
```
업무: 계약금 수령
관련 테이블: FinancialRecord, FinancialDocument

데이터 흐름:
1. FinancialRecord 테이블에 수입 기록
   - contract_id: "강남구 아파트 신축공사 계약 ID"
   - transaction_date: 2024-02-01
   - amount: 100,000,000원
   - type: "수입"
   - category: "계약금"
   - description: "1차 계약금 수령"
   - payment_method: "계좌이체"
   - status: "완료"
   - vendor_id: "ABC건설(주)의 ID"

2. FinancialDocument 테이블에 증빙 문서 업로드
   - 입금확인서: "payment_confirmation.pdf"
   - 세금계산서: "tax_invoice.pdf"

관계 설명:
- 1개 재무기록(FinancialRecord) → 여러 문서(FinancialDocument)
- 재무기록이 계약(Contract)과 거래처(Vendor)를 모두 참조
- 재무기록이 삭제되면 관련 문서도 함께 삭제됨
```

#### **2단계: 지출 기록**
```
업무: 자재비 지출
관련 테이블: FinancialRecord, FinancialDocument

데이터 흐름:
1. FinancialRecord 테이블에 지출 기록
   - contract_id: "강남구 아파트 신축공사 계약 ID"
   - transaction_date: 2024-02-10
   - amount: 50,000,000원
   - type: "지출"
   - category: "자재비"
   - description: "철근 구매"
   - payment_method: "계좌이체"
   - status: "완료"
   - vendor_id: "철근공급업체 ID"

2. FinancialDocument 테이블에 증빙 문서 업로드
   - 영수증: "receipt.pdf"
   - 세금계산서: "tax_invoice.pdf"
   - 계약서: "material_contract.pdf"

관계 설명:
- 동일한 구조로 지출도 기록
- 모든 금전적 거래가 계약과 연결되어 추적 가능
```

## 🔄 데이터 관계의 실제 활용

### **1. 계약별 현황 조회**
```sql
-- 특정 계약의 전체 현황 조회
SELECT 
    c.name as contract_name,
    c.contract_amount,
    v.name as vendor_name,
    COUNT(DISTINCT l.id) as labor_count,
    COUNT(DISTINCT wl.id) as work_log_count,
    SUM(CASE WHEN fr.type = '수입' THEN fr.amount ELSE 0 END) as total_income,
    SUM(CASE WHEN fr.type = '지출' THEN fr.amount ELSE 0 END) as total_expense
FROM contracts c
LEFT JOIN vendors v ON c.vendor_id = v.id
LEFT JOIN labors l ON c.id = l.contract_id
LEFT JOIN work_logs wl ON l.id = wl.labor_id
LEFT JOIN financial_records fr ON c.id = fr.contract_id
WHERE c.id = :contract_id
GROUP BY c.id, c.name, c.contract_amount, v.name;
```

### **2. 거래처별 거래 내역**
```sql
-- 특정 거래처의 모든 거래 내역 조회
SELECT 
    v.name as vendor_name,
    c.name as contract_name,
    fr.transaction_date,
    fr.amount,
    fr.type,
    fr.category,
    fr.description
FROM vendors v
JOIN contracts c ON v.id = c.vendor_id
JOIN financial_records fr ON c.id = fr.contract_id
WHERE v.id = :vendor_id
ORDER BY fr.transaction_date DESC;
```

### **3. 인력별 작업 현황**
```sql
-- 특정 인력의 작업 현황 조회
SELECT 
    l.name as labor_name,
    c.name as contract_name,
    wl.work_date,
    wl.work_hours,
    wl.total_amount,
    wl.description
FROM labors l
JOIN contracts c ON l.contract_id = c.id
JOIN work_logs wl ON l.id = wl.labor_id
WHERE l.id = :labor_id
ORDER BY wl.work_date DESC;
```

## 📊 비즈니스 인사이트 도출

### **1. 수익성 분석**
```
계약별 수익성 = (총 수입 - 총 지출) / 계약금액 × 100

데이터 소스:
- Contract.contract_amount (계약금액)
- FinancialRecord.amount (수입/지출 금액)
- FinancialRecord.type (수입/지출 구분)
```

### **2. 인력 효율성 분석**
```
인력별 작업 효율성 = 총 작업시간 / 총 지급금액

데이터 소스:
- WorkLog.work_hours (작업시간)
- WorkLog.total_amount (지급금액)
```

### **3. 거래처 신뢰도 분석**
```
거래처별 거래 빈도 = 거래 건수 / 계약 건수

데이터 소스:
- Contract.vendor_id (거래처 연결)
- FinancialRecord.vendor_id (거래처 연결)
```

## 🎯 핵심 비즈니스 가치

### **1. 데이터 무결성**
- 모든 거래가 계약과 연결되어 추적 가능
- 문서가 실제 거래와 연결되어 증빙 관리
- 인력과 작업이 계약과 연결되어 책임 소재 명확

### **2. 실시간 현황 파악**
- 계약별 진행상황 실시간 조회
- 재무 현황 실시간 모니터링
- 인력 작업 현황 실시간 추적

### **3. 의사결정 지원**
- 수익성 분석을 통한 사업 판단
- 인력 효율성 분석을 통한 인사 관리
- 거래처 신뢰도 분석을 통한 파트너십 관리 