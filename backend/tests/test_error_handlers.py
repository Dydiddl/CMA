import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from app.core.error_handlers import (
    validation_exception_handler,
    integrity_error_handler,
    permission_error_handler,
    not_found_error_handler,
    general_exception_handler
)
from app.schemas.error import (
    ErrorResponse,
    ValidationErrorResponse,
    PermissionErrorResponse,
    NotFoundErrorResponse
)

app = FastAPI()

class TestModel(BaseModel):
    name: str = Field(..., min_length=3)
    age: int = Field(..., gt=0)

@app.post("/test-validation")
async def test_validation(model: TestModel):
    return model

@app.get("/test-integrity")
async def test_integrity():
    raise IntegrityError(None, None, "unique constraint violation")

@app.get("/test-permission")
async def test_permission():
    raise PermissionErrorResponse(
        code="PERMISSION_DENIED",
        message="권한이 없습니다",
        required_permissions=["admin"]
    )

@app.get("/test-not-found")
async def test_not_found():
    raise NotFoundErrorResponse(
        code="NOT_FOUND",
        message="리소스를 찾을 수 없습니다",
        resource_type="user",
        resource_id=1
    )

@app.get("/test-general")
async def test_general():
    raise Exception("일반적인 오류")

# 에러 핸들러 등록
app.add_exception_handler(ValidationErrorResponse, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(PermissionErrorResponse, permission_error_handler)
app.add_exception_handler(NotFoundErrorResponse, not_found_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

client = TestClient(app)

def test_validation_error():
    response = client.post("/test-validation", json={"name": "a", "age": -1})
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "VALIDATION_ERROR"
    assert "field_errors" in data

def test_integrity_error():
    response = client.get("/test-integrity")
    assert response.status_code == 409
    data = response.json()
    assert data["code"] == "DUPLICATE_ENTRY"
    assert "이미 존재하는 데이터입니다" in data["message"]

def test_permission_error():
    response = client.get("/test-permission")
    assert response.status_code == 403
    data = response.json()
    assert data["code"] == "PERMISSION_DENIED"
    assert "권한이 없습니다" in data["message"]
    assert "admin" in data["required_permissions"]

def test_not_found_error():
    response = client.get("/test-not-found")
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "NOT_FOUND"
    assert "리소스를 찾을 수 없습니다" in data["message"]
    assert data["resource_type"] == "user"
    assert data["resource_id"] == 1

def test_general_error():
    response = client.get("/test-general")
    assert response.status_code == 500
    data = response.json()
    assert data["code"] == "INTERNAL_SERVER_ERROR"
    assert "서버 내부 오류가 발생했습니다" in data["message"] 