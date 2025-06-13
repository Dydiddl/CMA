-- UUID 확장 활성화
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 사용자 관리 테이블
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'admin': 관리자, 'manager': 매니저, 'employee': 일반직원
    department VARCHAR(50), -- 부서명
    phone VARCHAR(20), -- 연락처
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true -- 계정 활성화 상태
);

COMMENT ON TABLE users IS '시스템 사용자 정보를 관리하는 테이블';
COMMENT ON COLUMN users.email IS '사용자 이메일 (로그인 ID로 사용)';
COMMENT ON COLUMN users.role IS '사용자 권한 레벨';
COMMENT ON COLUMN users.department IS '소속 부서';

-- 거래처 관리 테이블
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255) NOT NULL,
    business_number VARCHAR(20) UNIQUE, -- 사업자등록번호
    representative_name VARCHAR(100), -- 대표자명
    contact_person VARCHAR(100), -- 담당자명
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE clients IS '거래처(발주처) 정보를 관리하는 테이블';
COMMENT ON COLUMN clients.business_number IS '사업자등록번호 (고유식별)';
COMMENT ON COLUMN clients.representative_name IS '회사 대표자명';

-- 계약 관리 테이블
CREATE TABLE contracts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_number VARCHAR(50) UNIQUE NOT NULL, -- 계약번호
    client_id UUID REFERENCES clients(id),
    project_name VARCHAR(255) NOT NULL, -- 프로젝트명
    contract_amount DECIMAL(15,2) NOT NULL, -- 계약금액
    start_date DATE NOT NULL, -- 착수일
    end_date DATE, -- 준공일
    status VARCHAR(20) NOT NULL, -- 'pending': 대기, 'active': 진행중, 'completed': 완료, 'cancelled': 취소
    contract_type VARCHAR(50) NOT NULL, -- 'construction': 시공, 'maintenance': 유지보수, 'consulting': 컨설팅
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE contracts IS '계약 정보를 관리하는 테이블';
COMMENT ON COLUMN contracts.contract_number IS '계약번호 (고유식별)';
COMMENT ON COLUMN contracts.status IS '계약 진행 상태';
COMMENT ON COLUMN contracts.contract_type IS '계약 유형';

-- 작업자 관리 테이블
CREATE TABLE workers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    id_number VARCHAR(20) UNIQUE, -- 주민등록번호
    bank_account VARCHAR(50), -- 계좌번호
    bank_name VARCHAR(50), -- 은행명
    hourly_rate DECIMAL(10,2) NOT NULL, -- 시급
    is_active BOOLEAN DEFAULT true, -- 재직상태
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE workers IS '작업자(인력) 정보를 관리하는 테이블';
COMMENT ON COLUMN workers.id_number IS '주민등록번호 (고유식별)';
COMMENT ON COLUMN workers.hourly_rate IS '시급 (원/시간)';

-- 인건비 관리 테이블
CREATE TABLE labor_costs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id UUID REFERENCES contracts(id),
    worker_id UUID REFERENCES workers(id),
    work_date DATE NOT NULL, -- 작업일
    hours_worked DECIMAL(5,2) NOT NULL, -- 작업시간
    hourly_rate DECIMAL(10,2) NOT NULL, -- 시급
    total_amount DECIMAL(15,2) NOT NULL, -- 총액
    payment_status VARCHAR(20) DEFAULT 'pending', -- 'pending': 미지급, 'paid': 지급완료
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE labor_costs IS '인건비 지급 내역을 관리하는 테이블';
COMMENT ON COLUMN labor_costs.hours_worked IS '작업시간 (시간)';
COMMENT ON COLUMN labor_costs.total_amount IS '총 지급액 (시간 * 시급)';

-- 수입 관리 테이블
CREATE TABLE revenues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id UUID REFERENCES contracts(id),
    amount DECIMAL(15,2) NOT NULL, -- 수입금액
    payment_date DATE NOT NULL, -- 수입일
    payment_type VARCHAR(20) NOT NULL, -- 'cash': 현금, 'transfer': 계좌이체, 'check': 수표
    status VARCHAR(20) DEFAULT 'pending', -- 'pending': 미수금, 'received': 수금완료
    description TEXT, -- 비고
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE revenues IS '수입 내역을 관리하는 테이블';
COMMENT ON COLUMN revenues.payment_type IS '지급 수단';
COMMENT ON COLUMN revenues.status IS '수금 상태';

-- 문서 관리 테이블
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id UUID REFERENCES contracts(id),
    document_type VARCHAR(50) NOT NULL, -- 'contract': 계약서, 'invoice': 청구서, 'receipt': 영수증, 'report': 보고서
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL, -- 파일 크기 (bytes)
    mime_type VARCHAR(100) NOT NULL, -- 파일 형식
    uploaded_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE documents IS '계약 관련 문서를 관리하는 테이블';
COMMENT ON COLUMN documents.document_type IS '문서 유형';
COMMENT ON COLUMN documents.mime_type IS '파일 MIME 타입';

-- 비용 관리 테이블
CREATE TABLE expenses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id UUID REFERENCES contracts(id),
    category VARCHAR(50) NOT NULL, -- 'material': 자재비, 'equipment': 장비비, 'subcontract': 하도급비, 'other': 기타
    amount DECIMAL(15,2) NOT NULL, -- 비용금액
    expense_date DATE NOT NULL, -- 지출일
    description TEXT, -- 비고
    payment_status VARCHAR(20) DEFAULT 'pending', -- 'pending': 미지급, 'paid': 지급완료
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE expenses IS '비용 지출 내역을 관리하는 테이블';
COMMENT ON COLUMN expenses.category IS '비용 유형';
COMMENT ON COLUMN expenses.payment_status IS '지급 상태'; 