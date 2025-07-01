from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ....main import app
from app.api.deps import get_db
from ....schemas.contracts import ContractCreate, ContractDocumentCreate

client = TestClient(app)

def test_create_contract():
    response = client.post("/contracts/", json={"contract_name": "Test Contract", "status": "PENDING"})
    assert response.status_code == 200
    data = response.json()
    assert data["contract_name"] == "Test Contract"
    assert data["status"] == "PENDING"

def test_read_contracts():
    response = client.get("/contracts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_contract():
    response = client.get("/contracts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_contract():
    response = client.put("/contracts/1", json={"contract_name": "Updated Contract", "status": "COMPLETED"})
    assert response.status_code == 200
    data = response.json()
    assert data["contract_name"] == "Updated Contract"
    assert data["status"] == "COMPLETED"

def test_delete_contract():
    response = client.delete("/contracts/1")
    assert response.status_code == 200
    assert response.json()["message"] == "계약이 삭제되었습니다"

def test_create_contract_document():
    response = client.post("/contracts/1/documents", json={"document_name": "Test Document"})
    assert response.status_code == 200
    data = response.json()
    assert data["document_name"] == "Test Document"

def test_read_contract_documents():
    response = client.get("/contracts/1/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 