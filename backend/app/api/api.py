from fastapi import APIRouter

from backend.app.api.endpoints import (
    auth,
    users,
    projects,
    construction_sites,
    contracts,
    departments,
    daily_reports,
    costs,
    budgets,
    documents,
    api_doc
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(construction_sites.router, prefix="/construction-sites", tags=["construction-sites"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(daily_reports.router, prefix="/daily-reports", tags=["daily-reports"])
api_router.include_router(costs.router, prefix="/costs", tags=["costs"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(api_doc.router, prefix="/api-docs", tags=["api-docs"]) 