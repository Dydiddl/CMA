#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트 설정 및 공통 픽스처
"""

import pytest
from typing import Generator
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.vendor import Vendor
from app.models.contract import Contract
from app.models.financial import FinancialRecord
from app.models.labor import Labor
from app.models.project import Project
from datetime import datetime, date
import uuid


@pytest.fixture
def db() -> Generator[Session, None, None]:
    """데이터베이스 세션 픽스처"""
    for session in get_db():
        yield session
        break


# API 테스트용 실제 모델 생성 함수들
def create_test_user_model(db: Session, email: str = "test@example.com", full_name: str = "테스트 사용자", role: str = "user", department: str = "개발팀", phone: str = "010-1234-5678", is_active: bool = True) -> User:
    """API 테스트용 실제 User 모델 생성"""
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        password_hash=get_password_hash("testpassword123"),
        full_name=full_name,
        role=role,
        department=department,
        phone=phone,
        is_active=is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_vendor_model(db: Session, name: str = "테스트 거래처", business_number: str = "1234567890", representative: str = "홍길동", address: str = "서울시 강남구 테스트로 123", phone: str = "02-1234-5678", email: str = "test@vendor.com", bank_name: str = "신한은행", bank_account: str = "110-123-456789", status: str = "활성", description: str = "테스트용 거래처입니다.") -> Vendor:
    """API 테스트용 실제 Vendor 모델 생성"""
    vendor = Vendor(
        id=str(uuid.uuid4()),
        name=name,
        business_number=business_number,
        representative=representative,
        address=address,
        phone=phone,
        email=email,
        bank_name=bank_name,
        bank_account=bank_account,
        status=status,
        description=description,
        bank_info={"bank_name": bank_name, "account_number": bank_account},
        documents={}
    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


def create_test_contract_model(db: Session, vendor_id: str = None, name: str = "테스트 계약", contract_number: str = "CON-2024-001", contract_amount: float = 1000000, status: str = "진행중", contract_date: date = None, start_date: date = None, end_date: date = None, client_name: str = "테스트 발주처", client_contact: str = "02-1234-5678", description: str = "테스트 계약입니다.") -> Contract:
    """API 테스트용 실제 Contract 모델 생성"""
    if vendor_id is None:
        vendor = create_test_vendor_model(db)
        vendor_id = vendor.id
    
    if contract_date is None:
        contract_date = date.today()
    if start_date is None:
        start_date = date.today()
    if end_date is None:
        end_date = date.today()
    
    contract = Contract(
        id=str(uuid.uuid4()),
        name=name,
        contract_number=contract_number,
        contract_amount=contract_amount,
        contract_date=contract_date,
        start_date=start_date,
        end_date=end_date,
        client_name=client_name,
        client_contact=client_contact,
        status=status,
        description=description,
        vendor_id=vendor_id
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def create_test_labor_model(db: Session, contract_id: str = None, name: str = "홍길동", phone: str = "010-1234-5678", id_number: str = "900101-1234567", bank_name: str = "신한은행", bank_account: str = "110-123-456789", daily_wage: float = 20000, status: str = "재직", project_id: str = None, user_id: str = None) -> Labor:
    """API 테스트용 실제 Labor 모델 생성"""
    if contract_id is None:
        contract = create_test_contract_model(db)
        contract_id = contract.id
    
    labor = Labor(
        id=str(uuid.uuid4()),
        name=name,
        phone=phone,
        id_number=id_number,
        bank_name=bank_name,
        bank_account=bank_account,
        daily_wage=daily_wage,
        status=status,
        contract_id=contract_id,
        project_id=project_id,
        user_id=user_id,
        deleted_at=None,
        is_deleted=False
    )
    db.add(labor)
    db.commit()
    db.refresh(labor)
    return labor


def create_test_financial_record_model(db: Session, contract_id: str = None, amount: float = 1000000, type: str = "수입", category: str = "계약금", description: str = "테스트 계약금", payment_method: str = "계좌이체", status: str = "지급완료", vendor_id: str = None, user_id: str = None, transaction_date: date = None) -> FinancialRecord:
    """API 테스트용 실제 FinancialRecord 모델 생성"""
    if contract_id is None:
        contract = create_test_contract_model(db)
        contract_id = contract.id
    
    if transaction_date is None:
        transaction_date = date.today()
    
    record = FinancialRecord(
        id=str(uuid.uuid4()),
        contract_id=contract_id,
        project_id=None,
        transaction_date=transaction_date,
        date=transaction_date,
        amount=amount,
        type=type,
        category=category,
        description=description,
        payment_method=payment_method,
        status=status,
        vendor_id=vendor_id,
        user_id=user_id,
        deleted_at=None,
        is_deleted=False
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def create_test_project_model(db: Session, vendor_id: str = None, name: str = "테스트 프로젝트", project_number: str = "PRJ-2024-001", description: str = "테스트 프로젝트입니다.", start_date: date = None, end_date: date = None, budget: float = 10000000, status: str = "in_progress") -> Project:
    """API 테스트용 실제 Project 모델 생성"""
    if vendor_id is None:
        vendor = create_test_vendor_model(db)
        vendor_id = vendor.id
    
    if start_date is None:
        start_date = date.today()
    if end_date is None:
        end_date = date.today()
    
    project = Project(
        id=str(uuid.uuid4()),
        name=name,
        project_number=project_number,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        status=status,
        vendor_id=vendor_id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


# 기존 fixture들 (단위 테스트용)
@pytest.fixture
def create_test_user():
    """테스트용 사용자 생성"""
    return {
        "id": "user-test-123",
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "full_name": "테스트 사용자",
        "role": "user",
        "department": "개발팀",
        "phone": "010-1234-5678",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def create_test_vendor():
    """테스트용 거래처 생성"""
    return {
        "id": "vendor-test-123",
        "name": "테스트 거래처",
        "business_number": "1234567890",
        "representative": "홍길동",
        "address": "서울시 강남구 테스트로 123",
        "phone": "02-1234-5678",
        "email": "test@vendor.com",
        "bank_name": "신한은행",
        "bank_account": "110-123-456789",
        "status": "활성",
        "description": "테스트용 거래처입니다.",
        "bank_info": {"bank_name": "신한은행", "account_number": "110-123-456789"},
        "documents": {},
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def create_test_contract():
    """테스트용 계약 생성"""
    return {
        "id": "contract-test-123",
        "name": "테스트 계약",
        "contract_number": "CON-2024-001",
        "contract_amount": 1000000.0,
        "contract_date": "2024-01-01",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "client_name": "테스트 발주처",
        "client_contact": "02-1234-5678",
        "status": "진행중",
        "description": "테스트 계약입니다.",
        "vendor_id": "vendor-test-123",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def create_test_financial_record():
    """테스트용 재무 기록 생성"""
    return {
        "id": "financial-test-123",
        "contract_id": "contract-test-123",
        "project_id": "project-test-123",
        "transaction_date": "2024-01-01",
        "date": "2024-01-01",
        "amount": 1000000.0,
        "type": "수입",
        "category": "계약금",
        "description": "테스트 계약금",
        "payment_method": "계좌이체",
        "status": "지급완료",
        "vendor_id": "vendor-test-123",
        "user_id": "user-test-123",
        "deleted_at": None,
        "is_deleted": False,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def create_test_labor():
    """테스트용 노무자 생성"""
    return {
        "id": "labor-test-123",
        "name": "홍길동",
        "phone": "010-1234-5678",
        "id_number": "900101-1234567",
        "bank_name": "신한은행",
        "bank_account": "110-123-456789",
        "daily_wage": 20000.0,
        "status": "재직",
        "contract_id": "contract-test-123",
        "project_id": "project-test-123",
        "user_id": "user-test-123",
        "deleted_at": None,
        "is_deleted": False,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def create_test_project():
    """테스트용 프로젝트 생성"""
    return {
        "id": "project-test-123",
        "name": "테스트 프로젝트",
        "project_number": "PRJ-2024-001",
        "description": "테스트 프로젝트입니다.",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "budget": 10000000.0,
        "status": "in_progress",
        "vendor_id": "vendor-test-123",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def create_test_vendor_document():
    """테스트용 거래처 문서 생성"""
    return {
        "id": "vendor-doc-test-123",
        "vendor_id": "vendor-test-123",
        "name": "사업자등록증",
        "document_type": "사업자등록증",
        "file_path": "/path/to/business_license.pdf",
        "file_name": "business_license.pdf",
        "upload_date": "2024-01-01T00:00:00",
        "description": "사업자등록증 문서"
    }


@pytest.fixture
def create_test_financial_document():
    """테스트용 재무 문서 생성"""
    return {
        "id": "financial-doc-test-123",
        "financial_record_id": "financial-test-123",
        "document_type": "계약서",
        "file_path": "/path/to/contract.pdf",
        "file_name": "contract.pdf",
        "upload_date": "2024-01-01T00:00:00",
        "description": "계약서 문서"
    }


@pytest.fixture
def sample_contract_data():
    """샘플 계약 데이터 픽스처"""
    return {
        "name": "테스트 계약",
        "contract_number": "CON-2024-001",
        "contract_amount": 1000000,
        "contract_date": "2024-01-15T00:00:00",
        "client_name": "테스트 발주처",
        "vendor_id": "test-vendor-id",
        "status": "진행중"
    }


@pytest.fixture
def sample_labor_data():
    """샘플 노무 데이터 픽스처"""
    return {
        "name": "테스트 노무",
        "position": "기술자",
        "hourly_rate": 25000,
        "contract_id": "test-contract-id"
    }


@pytest.fixture
def sample_financial_data():
    """샘플 재무 데이터 픽스처"""
    return {
        "transaction_type": "수입",
        "amount": 500000,
        "description": "테스트 거래",
        "contract_id": "test-contract-id"
    }


# 성능 테스트용 픽스처
@pytest.fixture
def large_dataset():
    """대용량 데이터셋 픽스처"""
    return [
        {
            "name": f"계약 {i}",
            "contract_number": f"CON-2024-{i:03d}",
            "contract_amount": 1000000 + (i * 100000),
            "contract_date": "2024-01-15T00:00:00",
            "client_name": f"발주처 {i}",
            "vendor_id": f"vendor-{i}",
            "status": "진행중"
        }
        for i in range(1, 101)  # 100개의 테스트 데이터
    ]


# ASCR 테스트용 픽스처
@pytest.fixture
def sample_pdf_data():
    """샘플 PDF 데이터 픽스처"""
    return {
        "file_path": "tests/fixtures/sample.pdf",
        "year": 2025,
        "expected_sections": ["공통부문", "토목부문", "건축부문"]
    }


# Excel 테스트용 픽스처
@pytest.fixture
def sample_excel_data():
    """샘플 Excel 데이터 픽스처"""
    return {
        "file_path": "tests/fixtures/sample.xlsx",
        "sheet_name": "Sheet1",
        "expected_columns": ["A", "B", "C"]
    } 