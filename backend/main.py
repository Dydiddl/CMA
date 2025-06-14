"""
건설 관리 시스템 API 서버
이 파일은 FastAPI를 사용하여 건설 관리 시스템의 백엔드 API를 구현합니다.
주요 기능:
- 프로젝트 관리 (CRUD 작업)
- 태스크 관리 (CRUD 작업)
- 사용자 인증 및 권한 관리
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from backend.database import SessionLocal, engine
from backend import models, schemas, crud
from backend.auth import get_current_user

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Construction Management API",
    description="건설 프로젝트 관리를 위한 RESTful API",
    version="1.0.0"
)

# CORS(Cross-Origin Resource Sharing) 설정
# 개발 환경에서는 모든 도메인에서의 접근을 허용
# 프로덕션 환경에서는 특정 도메인만 허용하도록 수정 필요
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서만 사용. 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 세션 의존성
# 각 API 요청마다 새로운 데이터베이스 세션을 생성하고 요청 완료 후 세션을 종료
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 프로젝트 관련 엔드포인트
@app.get("/api/projects", response_model=List[schemas.Project])
def get_projects(
    skip: int = 0,  # 페이지네이션을 위한 건너뛸 항목 수
    limit: int = 100,  # 한 페이지에 표시할 최대 항목 수
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 인증된 사용자만 접근 가능
):
    """
    모든 프로젝트 목록을 조회합니다.
    페이지네이션을 지원하며, 인증된 사용자만 접근 가능합니다.
    """
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@app.post("/api/projects", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreate,  # 프로젝트 생성에 필요한 데이터
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    새로운 프로젝트를 생성합니다.
    인증된 사용자만 접근 가능합니다.
    """
    return crud.create_project(db=db, project=project)

@app.get("/api/projects/{project_id}", response_model=schemas.Project)
def get_project(
    project_id: int,  # 조회할 프로젝트의 ID
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    특정 프로젝트의 상세 정보를 조회합니다.
    프로젝트가 존재하지 않는 경우 404 에러를 반환합니다.
    """
    project = crud.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/api/projects/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,  # 수정할 프로젝트의 ID
    project: schemas.ProjectUpdate,  # 프로젝트 수정에 필요한 데이터
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    특정 프로젝트의 정보를 수정합니다.
    프로젝트가 존재하지 않는 경우 404 에러를 반환합니다.
    """
    updated_project = crud.update_project(db, project_id=project_id, project=project)
    if updated_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@app.delete("/api/projects/{project_id}")
def delete_project(
    project_id: int,  # 삭제할 프로젝트의 ID
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    특정 프로젝트를 삭제합니다.
    프로젝트가 존재하지 않는 경우 404 에러를 반환합니다.
    """
    success = crud.delete_project(db, project_id=project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

# 태스크 관련 엔드포인트
@app.get("/api/tasks", response_model=List[schemas.Task])
def get_tasks(
    project_id: int,  # 태스크를 조회할 프로젝트의 ID
    skip: int = 0,  # 페이지네이션을 위한 건너뛸 항목 수
    limit: int = 100,  # 한 페이지에 표시할 최대 항목 수
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    특정 프로젝트의 모든 태스크 목록을 조회합니다.
    페이지네이션을 지원하며, 인증된 사용자만 접근 가능합니다.
    """
    tasks = crud.get_tasks(db, project_id=project_id, skip=skip, limit=limit)
    return tasks

@app.post("/api/tasks", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,  # 태스크 생성에 필요한 데이터
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    새로운 태스크를 생성합니다.
    인증된 사용자만 접근 가능합니다.
    """
    return crud.create_task(db=db, task=task)

@app.get("/api/tasks/{task_id}", response_model=schemas.Task)
def get_task(
    task_id: int,  # 조회할 태스크의 ID
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    특정 태스크의 상세 정보를 조회합니다.
    태스크가 존재하지 않는 경우 404 에러를 반환합니다.
    """
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,  # 수정할 태스크의 ID
    task: schemas.TaskUpdate,  # 태스크 수정에 필요한 데이터
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    특정 태스크의 정보를 수정합니다.
    태스크가 존재하지 않는 경우 404 에러를 반환합니다.
    """
    updated_task = crud.update_task(db, task_id=task_id, task=task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/api/tasks/{task_id}")
def delete_task(
    task_id: int,  # 삭제할 태스크의 ID
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    특정 태스크를 삭제합니다.
    태스크가 존재하지 않는 경우 404 에러를 반환합니다.
    """
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    # 개발 서버 실행 (호스트: 0.0.0.0, 포트: 8000)
    uvicorn.run(app, host="0.0.0.0", port=8000) 