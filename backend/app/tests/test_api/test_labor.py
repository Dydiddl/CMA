from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ....main import app
from app.api.deps import get_db
from ....schemas.labor import LaborCreate, WorkLogCreate

client = TestClient(app)

def test_create_labor():
    response = client.post("/labor/", json={"name": "Test Worker", "status": "ACTIVE"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Worker"
    assert data["status"] == "ACTIVE"

def test_read_labor_list():
    response = client.get("/labor/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_labor():
    response = client.get("/labor/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_labor():
    response = client.put("/labor/1", json={"name": "Updated Worker", "status": "INACTIVE"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Worker"
    assert data["status"] == "INACTIVE"

def test_delete_labor():
    response = client.delete("/labor/1")
    assert response.status_code == 200
    assert response.json()["message"] == "노동자가 삭제되었습니다"

def test_create_work_log():
    response = client.post("/labor/1/work-logs", json={"work_date": "2023-10-01", "hours_worked": 8})
    assert response.status_code == 200
    data = response.json()
    assert data["work_date"] == "2023-10-01"
    assert data["hours_worked"] == 8

def test_read_work_logs():
    response = client.get("/labor/1/work-logs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_work_log():
    response = client.put("/labor/1/work-logs/1", json={"work_date": "2023-10-02", "hours_worked": 6})
    assert response.status_code == 200
    data = response.json()
    assert data["work_date"] == "2023-10-02"
    assert data["hours_worked"] == 6 