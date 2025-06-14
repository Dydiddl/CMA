import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from backend.app.models.base import Base
from backend.app.models.project import Project
from backend.app.models.contract import Contract
from backend.app.models.progress import Progress
from backend.app.models.financial_record import FinancialRecord
from backend.app.models.document import Document
from backend.app.models.user import User
from backend.app.models.department import Department

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

def test_project_validation(db_session):
    """프로젝트 모델 유효성 검사 테스트"""
    # 필수 필드 누락 테스트
    with pytest.raises(IntegrityError):
        project = Project()
        db_session.add(project)
        db_session.commit()

    # 코드 중복 테스트
    project1 = Project(
        name="테스트 프로젝트 1",
        code="TEST-001",
        status="active"
    )
    db_session.add(project1)
    db_session.commit()

    with pytest.raises(IntegrityError):
        project2 = Project(
            name="테스트 프로젝트 2",
            code="TEST-001",  # 중복된 코드
            status="active"
        )
        db_session.add(project2)
        db_session.commit()

def test_project_relationships(db_session):
    """프로젝트 관계 테스트"""
    # 사용자 생성
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()

    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active",
        owner_id=user.id
    )
    db_session.add(project)
    db_session.commit()

    # 계약 생성
    contract = Contract(
        project_id=project.id,
        contract_number="CONT-001",
        client_id="test-client-id",
        contract_amount=1000000,
        start_date=datetime.now(),
        status="active"
    )
    db_session.add(contract)
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

    # 관계 검증
    saved_project = db_session.query(Project).first()
    assert saved_project.owner == user
    assert len(saved_project.contracts) == 1
    assert len(saved_project.progress_records) == 1
    assert saved_project.contracts[0].contract_number == "CONT-001"
    assert saved_project.progress_records[0].progress_percentage == 50

def test_contract_constraints(db_session):
    """계약 모델 제약 조건 테스트"""
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()

    # 음수 금액 테스트
    with pytest.raises(ValueError):
        contract = Contract(
            project_id=project.id,
            contract_number="CONT-001",
            client_id="test-client-id",
            contract_amount=-1000000,  # 음수 금액
            start_date=datetime.now(),
            status="active"
        )
        db_session.add(contract)
        db_session.commit()

    # 잘못된 상태값 테스트
    with pytest.raises(ValueError):
        contract = Contract(
            project_id=project.id,
            contract_number="CONT-001",
            client_id="test-client-id",
            contract_amount=1000000,
            start_date=datetime.now(),
            status="invalid_status"  # 잘못된 상태값
        )
        db_session.add(contract)
        db_session.commit()

def test_progress_constraints(db_session):
    """진행상황 모델 제약 조건 테스트"""
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()

    # 잘못된 진행률 테스트
    with pytest.raises(ValueError):
        progress = Progress(
            project_id=project.id,
            progress_percentage=150,  # 100% 초과
            stage="construction",
            description="공사 진행 중"
        )
        db_session.add(progress)
        db_session.commit()

    # 음수 진행률 테스트
    with pytest.raises(ValueError):
        progress = Progress(
            project_id=project.id,
            progress_percentage=-10,  # 음수 진행률
            stage="construction",
            description="공사 진행 중"
        )
        db_session.add(progress)
        db_session.commit()

def test_financial_record_constraints(db_session):
    """금액 기록 모델 제약 조건 테스트"""
    # 프로젝트 생성
    project = Project(
        name="테스트 프로젝트",
        code="TEST-001",
        status="active"
    )
    db_session.add(project)
    db_session.commit()

    # 잘못된 거래 유형 테스트
    with pytest.raises(ValueError):
        record = FinancialRecord(
            project_id=project.id,
            transaction_type="invalid_type",  # 잘못된 거래 유형
            amount=1000000,
            transaction_date=datetime.now(),
            description="테스트 거래"
        )
        db_session.add(record)
        db_session.commit()

    # 음수 금액 테스트
    with pytest.raises(ValueError):
        record = FinancialRecord(
            project_id=project.id,
            transaction_type="income",
            amount=-1000000,  # 음수 금액
            transaction_date=datetime.now(),
            description="테스트 거래"
        )
        db_session.add(record)
        db_session.commit() 