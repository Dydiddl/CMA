from fastapi import APIRouter
from .endpoints import users, projects, tasks, ascr, performance

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(ascr.router, prefix="/ascr", tags=["ASCR"])
api_router.include_router(performance.router, prefix="/performance", tags=["Performance"]) 