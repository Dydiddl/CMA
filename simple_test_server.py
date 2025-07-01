#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 테스트 서버
실시간 연동 테스트용
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import uuid
from datetime import datetime

app = FastAPI(title="CMA Simple Test Server", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델
class ContractCreate(BaseModel):
    name: str
    contract_number: str
    contract_amount: float
    client_name: str
    status: str = "진행중"
    description: Optional[str] = None

class ContractUpdate(BaseModel):
    name: Optional[str] = None
    contract_number: Optional[str] = None
    contract_amount: Optional[float] = None
    client_name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

# 인메모리 데이터 저장소
contracts_db = [
    {
        "id": "1",
        "name": "테스트 계약 1",
        "contract_number": "CON-2024-001",
        "contract_amount": 1000000,
        "client_name": "테스트 발주처",
        "status": "진행중",
        "description": "테스트용 계약",
        "created_at": "2024-01-15T00:00:00"
    },
    {
        "id": "2",
        "name": "테스트 계약 2",
        "contract_number": "CON-2024-002",
        "contract_amount": 2000000,
        "client_name": "테스트 발주처 2",
        "status": "완료",
        "description": "완료된 테스트 계약",
        "created_at": "2024-01-20T00:00:00"
    }
]

financial_db = [
    {
        "id": "1",
        "type": "수입",
        "amount": 5000000,
        "description": "계약금 수입",
        "date": "2024-01-15",
        "created_at": "2024-01-15T00:00:00"
    },
    {
        "id": "2",
        "type": "지출",
        "amount": 3000000,
        "description": "자재비 지출",
        "date": "2024-01-20",
        "created_at": "2024-01-20T00:00:00"
    }
]

labor_db = [
    {
        "id": "1",
        "worker_name": "홍길동",
        "position": "현장소장",
        "salary": 5000000,
        "work_hours": 160,
        "created_at": "2024-01-15T00:00:00"
    },
    {
        "id": "2",
        "worker_name": "김철수",
        "position": "기술자",
        "salary": 3500000,
        "work_hours": 160,
        "created_at": "2024-01-15T00:00:00"
    }
]

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "CMA Simple Test Server", "status": "running"}

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

# 계약 관련 API
@app.get("/api/v1/contracts")
async def get_contracts(skip: int = 0, limit: int = 10, search: Optional[str] = None, status: Optional[str] = None):
    """계약 목록 조회"""
    filtered_contracts = contracts_db
    
    if search:
        filtered_contracts = [c for c in filtered_contracts if search.lower() in c["name"].lower() or search.lower() in c["contract_number"].lower()]
    
    if status:
        filtered_contracts = [c for c in filtered_contracts if c["status"] == status]
    
    total = len(filtered_contracts)
    paginated_contracts = filtered_contracts[skip:skip + limit]
    
    return {
        "status": "success",
        "data": paginated_contracts,
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@app.get("/api/v1/contracts/{contract_id}")
async def get_contract(contract_id: str):
    """계약 상세 조회"""
    contract = next((c for c in contracts_db if c["id"] == contract_id), None)
    if not contract:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    
    return {"status": "success", "data": contract}

@app.post("/api/v1/contracts")
async def create_contract(contract: ContractCreate):
    """계약 생성"""
    # 계약번호 중복 검사
    if any(c["contract_number"] == contract.contract_number for c in contracts_db):
        raise HTTPException(status_code=400, detail="이미 존재하는 계약번호입니다")
    
    new_contract = {
        "id": str(uuid.uuid4()),
        **contract.dict(),
        "created_at": datetime.now().isoformat()
    }
    
    contracts_db.append(new_contract)
    return {"status": "success", "data": new_contract}

@app.put("/api/v1/contracts/{contract_id}")
async def update_contract(contract_id: str, contract_update: ContractUpdate):
    """계약 수정"""
    contract = next((c for c in contracts_db if c["id"] == contract_id), None)
    if not contract:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    
    # 업데이트할 데이터만 적용
    update_data = contract_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        contract[key] = value
    
    return {"status": "success", "data": contract}

@app.delete("/api/v1/contracts/{contract_id}")
async def delete_contract(contract_id: str):
    """계약 삭제"""
    contract = next((c for c in contracts_db if c["id"] == contract_id), None)
    if not contract:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    
    contracts_db.remove(contract)
    return {"status": "success", "message": "계약이 성공적으로 삭제되었습니다"}

# 재무 관련 API
@app.get("/api/v1/financial")
async def get_financial():
    """재무 정보 조회 (요약)"""
    total_revenue = sum(f["amount"] for f in financial_db if f["type"] == "수입")
    total_expenses = sum(f["amount"] for f in financial_db if f["type"] == "지출")
    profit = total_revenue - total_expenses
    
    return {
        "status": "success",
        "data": {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "profit": profit
        }
    }

@app.get("/api/v1/finance")
async def get_financial_records(skip: int = 0, limit: int = 10, type: Optional[str] = None):
    """재무 기록 조회"""
    filtered_records = financial_db
    
    if type:
        filtered_records = [f for f in filtered_records if f["type"] == type]
    
    total = len(filtered_records)
    paginated_records = filtered_records[skip:skip + limit]
    
    return {
        "status": "success",
        "data": paginated_records,
        "total": total
    }

# 노무 관련 API
@app.get("/api/v1/labor")
async def get_labor():
    """노무 정보 조회 (요약)"""
    return {
        "status": "success",
        "data": labor_db
    }

@app.get("/api/v1/labor/workers")
async def get_workers(skip: int = 0, limit: int = 10, search: Optional[str] = None):
    """근로자 목록 조회"""
    filtered_workers = labor_db
    
    if search:
        filtered_workers = [w for w in labor_db if search.lower() in w["worker_name"].lower()]
    
    total = len(filtered_workers)
    paginated_workers = filtered_workers[skip:skip + limit]
    
    return {
        "status": "success",
        "data": paginated_workers,
        "total": total
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 