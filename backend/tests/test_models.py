import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.project import Project
from app.models.contract import Contract
from app.models.progress import Progress
from app.models.financial_record import FinancialRecord
from app.models.document import Document

# 테스트용 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_create_project(db_session):
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        description="테스트용 프로젝트입니다.",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    saved_project = db_session.query(Project).first()
    assert saved_project.name == "테스트 프로젝트"
    assert saved_project.code == "TEST-001"

def test_create_contract(db_session):
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    # 계약 생성
    contract = Contract(
        project_id=project.id,
        contract_number="CONT-001",
        client_id="test-client-id",
        contract_amount=1000000,
        start_date="2024-01-01",
        status="active",
        contract_type="construction",
        created_by="test-user-id"
    )
    db_session.add(contract)
    db_session.commit()
    
    saved_contract = db_session.query(Contract).first()
    assert saved_contract.contract_number == "CONT-001"
    assert saved_contract.project_id == project.id

def test_create_progress(db_session):
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    # 진행상황 생성
    progress = Progress(
        project_id=project.id,
        progress_percentage=50,
        stage="construction",
        description="공사 진행 중"
    )
    db_session.add(progress)
    db_session.commit()
    
    saved_progress = db_session.query(Progress).first()
    assert saved_progress.progress_percentage == 50
    assert saved_progress.project_id == project.id

def test_create_financial_record(db_session):
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    # 금액 기록 생성
    financial_record = FinancialRecord(
        project_id=project.id,
        transaction_type="income",
        amount=1000000,
        transaction_date="2024-01-01",
        description="계약금 수입"
    )
    db_session.add(financial_record)
    db_session.commit()
    
    saved_record = db_session.query(FinancialRecord).first()
    assert saved_record.transaction_type == "income"
    assert saved_record.amount == 1000000
    assert saved_record.project_id == project.id

def test_create_document(db_session):
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()
    
    # 문서 생성
    document = Document(
        project_id=project.id,
        document_type="contract",
        file_name="test.pdf",
        file_path="/path/to/test.pdf",
        file_size=1024,
        mime_type="application/pdf",
        uploaded_by="test-user-id"
    )
    db_session.add(document)
    db_session.commit()
    
    saved_document = db_session.query(Document).first()
    assert saved_document.document_type == "contract"
    assert saved_document.project_id == project.id 