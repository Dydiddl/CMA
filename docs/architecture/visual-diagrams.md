# 건설 관리 시스템 - 시각적 다이어그램

## 📊 1. 전체 시스템 구조도

```mermaid
graph TB
    subgraph "건설 관리 시스템 (CMA)"
        subgraph "핵심 비즈니스"
            A[Contract<br/>계약]
            B[Vendor<br/>거래처]
            C[Labor<br/>인력]
        end
        
        subgraph "문서 관리"
            D[ContractDocument<br/>계약 문서]
            E[VendorDocument<br/>거래처 문서]
            F[FinancialDocument<br/>재무 문서]
        end
        
        subgraph "재무 관리"
            G[FinancialRecord<br/>재무 기록]
        end
        
        subgraph "작업 관리"
            H[WorkLog<br/>작업일지]
        end
    end
    
    A --> D
    B --> E
    G --> F
    C --> H
    A --> G
    B --> G
    A --> C
```

## 🔗 2. 관계 유형별 다이어그램

### **2.1 1:N 관계**
```mermaid
graph LR
    subgraph "1:N 관계들"
        A[Contract<br/>1개 계약] --> D[ContractDocument<br/>여러 문서]
        B[Vendor<br/>1개 거래처] --> E[VendorDocument<br/>여러 문서]
        C[Labor<br/>1명 인력] --> H[WorkLog<br/>여러 작업일지]
        G[FinancialRecord<br/>1개 재무기록] --> F[FinancialDocument<br/>여러 문서]
    end
```

### **2.2 N:1 관계**
```mermaid
graph LR
    subgraph "N:1 관계들"
        D[ContractDocument<br/>여러 문서] --> A[Contract<br/>1개 계약]
        E[VendorDocument<br/>여러 문서] --> B[Vendor<br/>1개 거래처]
        H[WorkLog<br/>여러 작업일지] --> C[Labor<br/>1명 인력]
        F[FinancialDocument<br/>여러 문서] --> G[FinancialRecord<br/>1개 재무기록]
    end
```

### **2.3 복합 관계**
```mermaid
graph TB
    subgraph "복합 관계 구조"
        A[Contract<br/>계약]
        B[Vendor<br/>거래처]
        G[FinancialRecord<br/>재무기록]
        
        A --> G
        B --> G
        A --> B
    end
```

## 🏗️ 3. 계층 구조 다이어그램

```mermaid
graph TD
    subgraph "Level 1: 핵심 엔티티"
        A[Contract<br/>계약]
        B[Vendor<br/>거래처]
        C[Labor<br/>인력]
    end
    
    subgraph "Level 2: 하위 엔티티"
        D[ContractDocument<br/>계약 문서]
        E[VendorDocument<br/>거래처 문서]
        F[FinancialDocument<br/>재무 문서]
        H[WorkLog<br/>작업일지]
    end
    
    subgraph "Level 3: 연결 엔티티"
        G[FinancialRecord<br/>재무 기록]
    end
    
    A --> D
    B --> E
    G --> F
    C --> H
    A --> G
    B --> G
    A --> C
```

## 🔄 4. 데이터 흐름 다이어그램

### **4.1 계약 체결 프로세스**
```mermaid
flowchart TD
    A[거래처 등록] --> B[Vendor 테이블]
    B --> C[VendorDocument 업로드]
    C --> D[계약 생성]
    D --> E[Contract 테이블]
    E --> F[ContractDocument 업로드]
    F --> G[재무 기록]
    G --> H[FinancialRecord 테이블]
    H --> I[FinancialDocument 업로드]
```

### **4.2 인력 관리 프로세스**
```mermaid
flowchart TD
    A[계약 확인] --> B[Contract 테이블]
    B --> C[인력 등록]
    C --> D[Labor 테이블]
    D --> E[작업 기록]
    E --> F[WorkLog 테이블]
    F --> G[급여 계산]
    G --> H[FinancialRecord 생성]
```

## 📈 5. 비즈니스 관점 다이어그램

### **5.1 계약 중심 구조**
```mermaid
graph TB
    subgraph "계약 중심 비즈니스 구조"
        A[Contract<br/>계약]
        
        subgraph "계약 관련 데이터"
            B[ContractDocument<br/>계약 문서]
            C[FinancialRecord<br/>재무 기록]
            D[Labor<br/>인력]
            E[WorkLog<br/>작업일지]
        end
        
        A --> B
        A --> C
        A --> D
        D --> E
    end
```

### **5.2 거래처 중심 구조**
```mermaid
graph TB
    subgraph "거래처 중심 비즈니스 구조"
        A[Vendor<br/>거래처]
        
        subgraph "거래처 관련 데이터"
            B[VendorDocument<br/>거래처 문서]
            C[Contract<br/>계약]
            D[FinancialRecord<br/>재무 기록]
        end
        
        A --> B
        A --> C
        A --> D
    end
```

## 🎯 6. 사용자 관점 다이어그램

### **6.1 관리자 관점**
```mermaid
graph TB
    subgraph "관리자 관점"
        A[전체 현황 대시보드]
        
        subgraph "관리 기능"
            B[계약 관리]
            C[재무 관리]
            D[인력 관리]
            E[거래처 관리]
        end
        
        A --> B
        A --> C
        A --> D
        A --> E
    end
```

### **6.2 현장 관리자 관점**
```mermaid
graph TB
    subgraph "현장 관리자 관점"
        A[현장 관리 대시보드]
        
        subgraph "현장 기능"
            B[작업일지 관리]
            C[인력 관리]
            D[진행상황 관리]
        end
        
        A --> B
        A --> C
        A --> D
    end
```

## 🔍 7. 데이터 접근 패턴 다이어그램

### **7.1 계약별 조회 패턴**
```mermaid
graph LR
    A[계약 ID] --> B[Contract 조회]
    B --> C[관련 문서 조회]
    B --> D[재무 기록 조회]
    B --> E[인력 정보 조회]
    E --> F[작업일지 조회]
    
    C --> G[ContractDocument]
    D --> H[FinancialRecord]
    F --> I[WorkLog]
```

### **7.2 거래처별 조회 패턴**
```mermaid
graph LR
    A[거래처 ID] --> B[Vendor 조회]
    B --> C[거래처 문서 조회]
    B --> D[관련 계약 조회]
    B --> E[재무 기록 조회]
    
    C --> F[VendorDocument]
    D --> G[Contract]
    E --> H[FinancialRecord]
```

## 📊 8. 성능 최적화 다이어그램

### **8.1 인덱스 전략**
```mermaid
graph TB
    subgraph "인덱스 전략"
        A[Primary Key Index]
        B[Foreign Key Index]
        C[Business Key Index]
        D[Composite Index]
        
        subgraph "인덱스 대상"
            E[contract_number]
            F[business_number]
            G[transaction_date]
            H[work_date]
        end
        
        A --> E
        B --> F
        C --> G
        D --> H
    end
```

### **8.2 쿼리 최적화**
```mermaid
graph LR
    A[사용자 요청] --> B[쿼리 분석]
    B --> C{인덱스 사용 가능?}
    C -->|Yes| D[인덱스 스캔]
    C -->|No| E[전체 테이블 스캔]
    D --> F[결과 반환]
    E --> F
```

## 🛡️ 9. 보안 및 권한 다이어그램

### **9.1 데이터 접근 권한**
```mermaid
graph TB
    subgraph "권한 구조"
        A[시스템 관리자]
        B[프로젝트 관리자]
        C[현장 관리자]
        D[일반 사용자]
        
        subgraph "접근 가능 데이터"
            E[전체 데이터]
            F[프로젝트별 데이터]
            G[현장별 데이터]
            H[제한된 데이터]
        end
        
        A --> E
        B --> F
        C --> G
        D --> H
    end
```

## 🔄 10. 데이터 동기화 다이어그램

### **10.1 온라인/오프라인 동기화**
```mermaid
graph TB
    subgraph "데이터 동기화"
        A[로컬 데이터베이스]
        B[클라우드 데이터베이스]
        C[동기화 서비스]
        
        A --> C
        B --> C
        C --> A
        C --> B
    end
```

이러한 시각적 다이어그램들을 통해 설계 요청자는 복잡한 데이터베이스 구조를 직관적으로 이해할 수 있습니다. 