# 건설 관리 시스템 - 복합적 스키마 관계도

## 🏗️ 전체 시스템 복합 관계도 (Comprehensive Schema Relationship)

### **1. 완전한 ERD 다이어그램**

```mermaid
erDiagram
    %% 핵심 비즈니스 엔티티
    CONTRACT {
        uuid id PK "고유 식별자"
        string name "계약명"
        string contract_number UK "계약번호 (고유)"
        float contract_amount "계약금액"
        datetime contract_date "계약일"
        datetime start_date "시작일"
        datetime end_date "종료일"
        string client_name "발주처명"
        string client_contact "발주처 연락처"
        string status "계약 상태"
        text description "계약 설명"
        string vendor_id FK "거래처 참조"
        datetime created_at "생성일시"
        datetime updated_at "수정일시"
    }
    
    VENDOR {
        string id PK "고유 식별자"
        string name "거래처명"
        string business_number UK "사업자등록번호 (고유)"
        string representative "대표자"
        string address "주소"
        string phone "전화번호"
        string email "이메일"
        string bank_name "은행명"
        string bank_account "계좌번호"
        string status "거래처 상태"
        text description "거래처 설명"
        json bank_info "은행 정보 (JSON)"
        json documents "문서 메타데이터 (JSON)"
        datetime created_at "생성일시"
        datetime updated_at "수정일시"
    }
    
    LABOR {
        uuid id PK "고유 식별자"
        string name "인력명"
        string phone "전화번호"
        string id_number UK "주민번호 (고유)"
        string bank_name "은행명"
        string bank_account "계좌번호"
        float daily_wage "일당"
        string status "재직 상태"
        string contract_id FK "계약 참조"
        datetime created_at "생성일시"
        datetime updated_at "수정일시"
    }
    
    %% 문서 관리 엔티티
    CONTRACT_DOCUMENT {
        uuid id PK "고유 식별자"
        string contract_id FK "계약 참조"
        string document_type "문서 유형"
        string file_path "파일 경로"
        string file_name "파일명"
        datetime upload_date "업로드일"
        text description "문서 설명"
        datetime created_at "생성일시"
        datetime updated_at "수정일시"
    }
    
    VENDOR_DOCUMENT {
        int id PK "고유 식별자"
        string vendor_id FK "거래처 참조"
        string document_type "문서 유형"
        string file_path "파일 경로"
        string file_name "파일명"
        datetime upload_date "업로드일"
        text description "문서 설명"
    }
    
    %% 재무 관리 엔티티
    FINANCIAL_RECORD {
        uuid id PK "고유 식별자"
        string contract_id FK "계약 참조"
        date transaction_date "거래일"
        float amount "금액"
        string type "거래 유형 (수입/지출)"
        string category "카테고리"
        text description "거래 설명"
        string payment_method "결제방법"
        string status "거래 상태"
        string vendor_id FK "거래처 참조"
        datetime created_at "생성일시"
        datetime updated_at "수정일시"
    }
    
    FINANCIAL_DOCUMENT {
        uuid id PK "고유 식별자"
        string financial_record_id FK "재무기록 참조"
        string document_type "문서 유형"
        string file_path "파일 경로"
        string file_name "파일명"
        datetime upload_date "업로드일"
        text description "문서 설명"
        datetime created_at "생성일시"
        datetime updated_at "수정일시"
    }
    
    %% 작업 관리 엔티티
    WORK_LOG {
        uuid id PK "고유 식별자"
        string labor_id FK "인력 참조"
        date work_date "작업일"
        datetime start_time "시작시간"
        datetime end_time "종료시간"
        float work_hours "작업시간"
        float daily_wage "일당"
        float total_amount "총액"
        text description "작업 설명"
        string status "작업 상태"
        datetime created_at "생성일시"
        datetime updated_at "수정일시"
    }
    
    %% 관계 정의
    CONTRACT ||--o{ CONTRACT_DOCUMENT : "has"
    CONTRACT ||--o{ FINANCIAL_RECORD : "generates"
    CONTRACT ||--o{ LABOR : "employs"
    CONTRACT ||--o{ WORK_LOG : "tracks"
    
    VENDOR ||--o{ CONTRACT : "supports"
    VENDOR ||--o{ FINANCIAL_RECORD : "involves"
    VENDOR ||--o{ VENDOR_DOCUMENT : "has"
    
    FINANCIAL_RECORD ||--o{ FINANCIAL_DOCUMENT : "supports"
    LABOR ||--o{ WORK_LOG : "creates"
```

### **2. 상세한 관계 흐름도**

```mermaid
graph TB
    subgraph "🏢 핵심 비즈니스 엔티티"
        subgraph "📋 계약 관리"
            A[Contract<br/>계약<br/>• 계약명, 계약번호<br/>• 계약금액, 계약일<br/>• 시작일, 종료일<br/>• 발주처, 상태]
        end
        
        subgraph "🏪 거래처 관리"
            B[Vendor<br/>거래처<br/>• 거래처명, 사업자번호<br/>• 대표자, 주소<br/>• 연락처, 이메일<br/>• 은행정보, 상태]
        end
        
        subgraph "👷 인력 관리"
            C[Labor<br/>인력<br/>• 이름, 전화번호<br/>• 주민번호, 은행정보<br/>• 일당, 재직상태<br/>• 계약 연결]
        end
    end
    
    subgraph "📄 문서 관리 시스템"
        subgraph "계약 문서"
            D[ContractDocument<br/>계약 문서<br/>• 문서 유형<br/>• 파일 경로, 파일명<br/>• 업로드일, 설명]
        end
        
        subgraph "거래처 문서"
            E[VendorDocument<br/>거래처 문서<br/>• 사업자등록증<br/>• 통장사본<br/>• 기타 서류]
        end
        
        subgraph "재무 문서"
            F[FinancialDocument<br/>재무 문서<br/>• 영수증, 세금계산서<br/>• 입금확인서<br/>• 지출증빙]
        end
    end
    
    subgraph "💰 재무 관리 시스템"
        G[FinancialRecord<br/>재무 기록<br/>• 거래일, 금액<br/>• 유형(수입/지출)<br/>• 카테고리, 설명<br/>• 결제방법, 상태]
    end
    
    subgraph "📝 작업 관리 시스템"
        H[WorkLog<br/>작업일지<br/>• 작업일, 시작/종료시간<br/>• 작업시간, 일당<br/>• 총액, 작업설명<br/>• 작업상태]
    end
    
    %% 핵심 관계
    A -->|"1:N<br/>계약당 여러 문서"| D
    A -->|"1:N<br/>계약당 여러 재무기록"| G
    A -->|"1:N<br/>계약당 여러 인력"| C
    A -->|"1:N<br/>계약당 여러 작업일지"| H
    
    B -->|"1:N<br/>거래처당 여러 계약"| A
    B -->|"1:N<br/>거래처당 여러 재무기록"| G
    B -->|"1:N<br/>거래처당 여러 문서"| E
    
    C -->|"1:N<br/>인력당 여러 작업일지"| H
    
    G -->|"1:N<br/>재무기록당 여러 문서"| F
    
    %% 외래키 관계 표시
    A -.->|"vendor_id FK"| B
    C -.->|"contract_id FK"| A
    G -.->|"contract_id FK<br/>vendor_id FK"| A
    G -.->|"vendor_id FK"| B
    H -.->|"labor_id FK"| C
    D -.->|"contract_id FK"| A
    E -.->|"vendor_id FK"| B
    F -.->|"financial_record_id FK"| G
```

### **3. 비즈니스 프로세스별 상세 관계도**

```mermaid
graph TB
    subgraph "🎯 비즈니스 프로세스별 관계"
        subgraph "📋 1. 계약 체결 프로세스"
            A1[거래처 등록<br/>Vendor]
            A2[거래처 문서 업로드<br/>VendorDocument]
            A3[계약 생성<br/>Contract]
            A4[계약 문서 업로드<br/>ContractDocument]
            A5[재무 기록 생성<br/>FinancialRecord]
            A6[재무 문서 업로드<br/>FinancialDocument]
            
            A1 --> A2
            A2 --> A3
            A3 --> A4
            A4 --> A5
            A5 --> A6
        end
        
        subgraph "👷 2. 인력 관리 프로세스"
            B1[계약 확인<br/>Contract]
            B2[인력 등록<br/>Labor]
            B3[작업일지 작성<br/>WorkLog]
            B4[급여 계산<br/>FinancialRecord]
            
            B1 --> B2
            B2 --> B3
            B3 --> B4
        end
        
        subgraph "💰 3. 재무 관리 프로세스"
            C1[수입 기록<br/>FinancialRecord]
            C2[지출 기록<br/>FinancialRecord]
            C3[증빙 문서 첨부<br/>FinancialDocument]
            C4[재무 보고서 생성]
            
            C1 --> C3
            C2 --> C3
            C3 --> C4
        end
    end
    
    subgraph "🔄 데이터 흐름"
        D1[입력 데이터]
        D2[처리 로직]
        D3[저장 데이터]
        D4[출력 결과]
        
        D1 --> D2
        D2 --> D3
        D3 --> D4
    end
```

### **4. 상세한 데이터 접근 패턴 다이어그램**

```mermaid
graph TB
    subgraph "🔍 데이터 접근 패턴"
        subgraph "📊 1. 계약별 종합 조회"
            E1[계약 ID 입력]
            E2[Contract 조회]
            E3[관련 문서 조회<br/>ContractDocument]
            E4[재무 기록 조회<br/>FinancialRecord]
            E5[인력 정보 조회<br/>Labor]
            E6[작업일지 조회<br/>WorkLog]
            E7[거래처 정보 조회<br/>Vendor]
            
            E1 --> E2
            E2 --> E3
            E2 --> E4
            E2 --> E5
            E5 --> E6
            E2 --> E7
        end
        
        subgraph "🏪 2. 거래처별 조회"
            F1[거래처 ID 입력]
            F2[Vendor 조회]
            F3[거래처 문서 조회<br/>VendorDocument]
            F4[관련 계약 조회<br/>Contract]
            F5[재무 기록 조회<br/>FinancialRecord]
            
            F1 --> F2
            F2 --> F3
            F2 --> F4
            F2 --> F5
        end
        
        subgraph "👷 3. 인력별 조회"
            G1[인력 ID 입력]
            G2[Labor 조회]
            G3[소속 계약 조회<br/>Contract]
            G4[작업일지 조회<br/>WorkLog]
            G5[급여 정보 조회<br/>FinancialRecord]
            
            G1 --> G2
            G2 --> G3
            G2 --> G4
            G2 --> G5
        end
    end
```

### **5. 상세한 관계 유형별 분류도**

```mermaid
graph TB
    subgraph "🔗 관계 유형별 상세 분류"
        subgraph "1️⃣ 1:1 관계"
            H1[현재 시스템에서는<br/>1:1 관계 없음]
        end
        
        subgraph "1️⃣:N 1:N 관계"
            H2[Contract → ContractDocument<br/>1개 계약 → 여러 문서]
            H3[Contract → FinancialRecord<br/>1개 계약 → 여러 재무기록]
            H4[Contract → Labor<br/>1개 계약 → 여러 인력]
            H5[Vendor → Contract<br/>1개 거래처 → 여러 계약]
            H6[Vendor → FinancialRecord<br/>1개 거래처 → 여러 재무기록]
            H7[Vendor → VendorDocument<br/>1개 거래처 → 여러 문서]
            H8[FinancialRecord → FinancialDocument<br/>1개 재무기록 → 여러 문서]
            H9[Labor → WorkLog<br/>1명 인력 → 여러 작업일지]
        end
        
        subgraph "N:1 N:1 관계"
            H10[ContractDocument → Contract<br/>여러 문서 → 1개 계약]
            H11[FinancialRecord → Contract<br/>여러 재무기록 → 1개 계약]
            H12[Labor → Contract<br/>여러 인력 → 1개 계약]
            H13[Contract → Vendor<br/>여러 계약 → 1개 거래처]
            H14[FinancialRecord → Vendor<br/>여러 재무기록 → 1개 거래처]
            H15[VendorDocument → Vendor<br/>여러 문서 → 1개 거래처]
            H16[FinancialDocument → FinancialRecord<br/>여러 문서 → 1개 재무기록]
            H17[WorkLog → Labor<br/>여러 작업일지 → 1명 인력]
        end
    end
```

### **6. 상세한 제약조건 및 인덱스 다이어그램**

```mermaid
graph TB
    subgraph "🔒 제약조건 및 인덱스"
        subgraph "🔑 Primary Key"
            I1[Contract.id<br/>UUID, Primary Key]
            I2[Vendor.id<br/>String, Primary Key]
            I3[Labor.id<br/>UUID, Primary Key]
            I4[FinancialRecord.id<br/>UUID, Primary Key]
            I5[WorkLog.id<br/>UUID, Primary Key]
            I6[ContractDocument.id<br/>UUID, Primary Key]
            I7[VendorDocument.id<br/>Integer, Primary Key]
            I8[FinancialDocument.id<br/>UUID, Primary Key]
        end
        
        subgraph "🔗 Foreign Key"
            I9[Contract.vendor_id<br/>→ Vendor.id]
            I10[Labor.contract_id<br/>→ Contract.id]
            I11[FinancialRecord.contract_id<br/>→ Contract.id]
            I12[FinancialRecord.vendor_id<br/>→ Vendor.id]
            I13[WorkLog.labor_id<br/>→ Labor.id]
            I14[ContractDocument.contract_id<br/>→ Contract.id]
            I15[VendorDocument.vendor_id<br/>→ Vendor.id]
            I16[FinancialDocument.financial_record_id<br/>→ FinancialRecord.id]
        end
        
        subgraph "🔍 Unique Key"
            I17[Contract.contract_number<br/>Unique]
            I18[Vendor.business_number<br/>Unique]
            I19[Labor.id_number<br/>Unique]
        end
        
        subgraph "📊 Index"
            I20[Contract.name<br/>Index]
            I21[Contract.contract_number<br/>Unique Index]
            I22[Vendor.name<br/>Index]
            I23[Vendor.business_number<br/>Unique Index]
            I24[FinancialRecord.transaction_date<br/>Index]
            I25[WorkLog.work_date<br/>Index]
        end
    end
```

### **7. 상세한 데이터 무결성 다이어그램**

```mermaid
graph TB
    subgraph "🛡️ 데이터 무결성 보장"
        subgraph "📋 참조 무결성"
            J1[CASCADE DELETE<br/>계약 삭제 시<br/>관련 데이터 모두 삭제]
            J2[CASCADE DELETE<br/>거래처 삭제 시<br/>관련 데이터 모두 삭제]
            J3[CASCADE DELETE<br/>인력 삭제 시<br/>작업일지 삭제]
            J4[CASCADE DELETE<br/>재무기록 삭제 시<br/>재무문서 삭제]
        end
        
        subgraph "✅ 체크 제약조건"
            J5[contract_amount > 0<br/>계약금액은 양수]
            J6[amount > 0<br/>거래금액은 양수]
            J7[daily_wage > 0<br/>일당은 양수]
            J8[work_hours > 0<br/>작업시간은 양수]
            J9[start_date <= end_date<br/>시작일 <= 종료일]
        end
        
        subgraph "🔍 비즈니스 규칙"
            J10[계약번호 중복 불가<br/>Unique Constraint]
            J11[사업자번호 중복 불가<br/>Unique Constraint]
            J12[주민번호 중복 불가<br/>Unique Constraint]
            J13[재무기록은 계약과 연결<br/>Foreign Key Constraint]
            J14[작업일지는 인력과 연결<br/>Foreign Key Constraint]
        end
    end
```

### **8. 상세한 성능 최적화 다이어그램**

```mermaid
graph TB
    subgraph "⚡ 성능 최적화 전략"
        subgraph "📊 인덱스 전략"
            K1[Primary Key Index<br/>자동 생성]
            K2[Foreign Key Index<br/>자동 생성]
            K3[Business Key Index<br/>수동 생성]
            K4[Composite Index<br/>복합 인덱스]
        end
        
        subgraph "🔍 쿼리 최적화"
            K5[계약별 조회<br/>contract_id Index]
            K6[거래처별 조회<br/>vendor_id Index]
            K7[날짜별 조회<br/>transaction_date Index]
            K8[인력별 조회<br/>labor_id Index]
        end
        
        subgraph "💾 데이터 파티셔닝"
            K9[재무기록<br/>월별 파티셔닝]
            K10[작업일지<br/>월별 파티셔닝]
            K11[문서 저장<br/>연도별 파티셔닝]
        end
        
        subgraph "🔄 캐싱 전략"
            K12[계약 정보<br/>Redis 캐싱]
            K13[거래처 정보<br/>Redis 캐싱]
            K14[인력 정보<br/>Redis 캐싱]
            K15[재무 집계<br/>Redis 캐싱]
        end
    end
```

### **9. 상세한 보안 및 권한 다이어그램**

```mermaid
graph TB
    subgraph "🔐 보안 및 권한 관리"
        subgraph "👥 사용자 역할"
            L1[시스템 관리자<br/>전체 권한]
            L2[프로젝트 관리자<br/>프로젝트별 권한]
            L3[현장 관리자<br/>현장별 권한]
            L4[일반 사용자<br/>제한된 권한]
        end
        
        subgraph "📋 데이터 접근 권한"
            L5[계약 정보<br/>읽기/쓰기/삭제]
            L6[거래처 정보<br/>읽기/쓰기/삭제]
            L7[인력 정보<br/>읽기/쓰기/삭제]
            L8[재무 정보<br/>읽기/쓰기/삭제]
            L9[작업일지<br/>읽기/쓰기/삭제]
            L10[문서 파일<br/>읽기/쓰기/삭제]
        end
        
        subgraph "🛡️ 보안 조치"
            L11[데이터 암호화<br/>AES-256]
            L12[접근 로그<br/>감사 추적]
            L13[세션 관리<br/>JWT 토큰]
            L14[파일 업로드<br/>보안 검증]
        end
    end
```

### **10. 상세한 확장성 및 유지보수 다이어그램**

```mermaid
graph TB
    subgraph "🚀 확장성 및 유지보수"
        subgraph "📈 확장 가능한 구조"
            M1[모듈화된 설계<br/>독립적 확장]
            M2[API 기반 구조<br/>서비스 분리]
            M3[마이크로서비스<br/>준비]
            M4[클라우드 네이티브<br/>준비]
        end
        
        subgraph "🔧 유지보수성"
            M5[코드 표준화<br/>일관된 네이밍]
            M6[문서화<br/>API 문서]
            M7[테스트 커버리지<br/>80% 이상]
            M8[버전 관리<br/>Git 기반]
        end
        
        subgraph "📊 모니터링"
            M9[성능 모니터링<br/>응답시간 추적]
            M10[에러 로깅<br/>실시간 알림]
            M11[사용량 통계<br/>트래픽 분석]
            M12[백업 관리<br/>자동 백업]
        end
    end
```

이러한 상세한 다이어그램들을 통해 건설 관리 시스템의 복합적인 스키마 관계를 완전히 이해할 수 있습니다. 각 다이어그램은 특정 관점에서 시스템의 구조와 관계를 보여주며, 전체적으로는 시스템의 완전한 아키텍처를 제공합니다. 