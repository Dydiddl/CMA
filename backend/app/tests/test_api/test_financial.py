from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ....main import app
from ....db.base import get_db
from ....schemas.financial import FinancialRecordCreate, FinancialDocumentCreate

client = TestClient(app)

def test_create_financial_record():
    response = client.post("/financial/", json={"project_name": "Test Project", "status": "PENDING"})
    assert response.status_code == 200
    data = response.json()
    assert data["project_name"] == "Test Project"
    assert data["status"] == "PENDING"

def test_read_financial_records():
    response = client.get("/financial/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_financial_record():
    response = client.get("/financial/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_financial_record():
    response = client.put("/financial/1", json={"project_name": "Updated Project", "status": "COMPLETED"})
    assert response.status_code == 200
    data = response.json()
    assert data["project_name"] == "Updated Project"
    assert data["status"] == "COMPLETED"

def test_delete_financial_record():
    response = client.delete("/financial/1")
    assert response.status_code == 200
    assert response.json()["message"] == "재무 기록이 삭제되었습니다"

def test_create_financial_document():
    response = client.post("/financial/1/documents", json={"document_name": "Test Document"})
    assert response.status_code == 200
    data = response.json()
    assert data["document_name"] == "Test Document"

def test_read_financial_documents():
    response = client.get("/financial/1/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 