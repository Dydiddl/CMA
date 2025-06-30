from fastapi import APIRouter
from .endpoints import (
    auth,
    users,
    contracts,
    labor,
    vendors,
    finance,
    dashboard
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["인증"])
api_router.include_router(users.router, prefix="/users", tags=["사용자"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["계약 관리"])
api_router.include_router(labor.router, prefix="/labor", tags=["인력 관리"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["거래처 관리"])
api_router.include_router(finance.router, prefix="/finance", tags=["재무 관리"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["대시보드"]) 