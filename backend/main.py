"""
건설 관리 시스템 API 서버
이 파일은 FastAPI를 사용하여 건설 관리 시스템의 백엔드 API를 구현합니다.
주요 기능:
- 프로젝트 관리 (CRUD 작업)
- 태스크 관리 (CRUD 작업)
- 사용자 인증 및 권한 관리
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import json
from sqlalchemy.sql import func
import asyncio
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from .config import settings
from .middleware import PrometheusMiddleware, LoggingMiddleware, get_metrics
from .logger import app_logger

from backend.database import SessionLocal, engine
from backend import models, schemas, crud
from backend.auth import get_current_user

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    건설 관리 시스템 API
    
    ## 주요 기능
    * 사용자 관리
    * 프로젝트 관리
    * 작업 관리
    * 알림 시스템
    
    ## API 문서
    이 API는 RESTful 원칙을 따르며, 모든 엔드포인트는 JSON 형식으로 데이터를 주고받습니다.
    인증이 필요한 엔드포인트의 경우 JWT 토큰을 Authorization 헤더에 포함해야 합니다.
    
    ## 응답 코드
    * 200: 성공
    * 201: 생성 성공
    * 400: 잘못된 요청
    * 401: 인증 실패
    * 403: 권한 없음
    * 404: 리소스를 찾을 수 없음
    * 500: 서버 오류
    """,
    version="1.0.0",
    docs_url=None,  # 기본 Swagger UI 비활성화
    redoc_url=None  # 기본 ReDoc 비활성화
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

# WebSocket 연결 관리를 위한 클래스
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_notification(self, user_id: int, notification: dict):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(notification)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # 클라이언트로부터의 메시지 처리 (필요한 경우)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

@app.post("/notifications/", response_model=schemas.Notification)
async def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db)
):
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    # WebSocket을 통해 실시간 알림 전송
    await manager.send_notification(
        notification.user_id,
        {
            "id": db_notification.id,
            "title": db_notification.title,
            "message": db_notification.message,
            "type": db_notification.type,
            "created_at": db_notification.created_at.isoformat()
        }
    )
    
    return db_notification

@app.get("/notifications/{user_id}", response_model=List[schemas.Notification])
async def get_user_notifications(
    user_id: int,
    filter: schemas.NotificationFilter = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Notification).filter(models.Notification.user_id == user_id)
    
    # 필터 적용
    if filter.type:
        query = query.filter(models.Notification.type == filter.type)
    if filter.priority is not None:
        query = query.filter(models.Notification.priority == filter.priority)
    if filter.group:
        query = query.filter(models.Notification.group == filter.group)
    if filter.category:
        query = query.filter(models.Notification.category == filter.category)
    if filter.is_read is not None:
        query = query.filter(models.Notification.is_read == filter.is_read)
    if filter.start_date:
        query = query.filter(models.Notification.created_at >= filter.start_date)
    if filter.end_date:
        query = query.filter(models.Notification.created_at <= filter.end_date)
    
    # 만료된 알림 제외
    query = query.filter(
        (models.Notification.expires_at == None) |
        (models.Notification.expires_at > datetime.utcnow())
    )
    
    notifications = query.order_by(
        models.Notification.priority.desc(),
        models.Notification.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return notifications

@app.get("/notifications/{user_id}/groups", response_model=List[str])
async def get_notification_groups(
    user_id: int,
    db: Session = Depends(get_db)
):
    groups = db.query(models.Notification.group)\
        .filter(models.Notification.user_id == user_id)\
        .filter(models.Notification.group != None)\
        .distinct()\
        .all()
    return [group[0] for group in groups]

@app.get("/notifications/{user_id}/categories", response_model=List[str])
async def get_notification_categories(
    user_id: int,
    db: Session = Depends(get_db)
):
    categories = db.query(models.Notification.category)\
        .filter(models.Notification.user_id == user_id)\
        .filter(models.Notification.category != None)\
        .distinct()\
        .all()
    return [category[0] for category in categories]

@app.get("/notifications/{user_id}/summary", response_model=dict)
async def get_notification_summary(
    user_id: int,
    db: Session = Depends(get_db)
):
    total = db.query(models.Notification)\
        .filter(models.Notification.user_id == user_id)\
        .count()
    
    unread = db.query(models.Notification)\
        .filter(models.Notification.user_id == user_id)\
        .filter(models.Notification.is_read == False)\
        .count()
    
    by_priority = db.query(
        models.Notification.priority,
        func.count(models.Notification.id)
    ).filter(models.Notification.user_id == user_id)\
        .group_by(models.Notification.priority)\
        .all()
    
    by_type = db.query(
        models.Notification.type,
        func.count(models.Notification.id)
    ).filter(models.Notification.user_id == user_id)\
        .group_by(models.Notification.type)\
        .all()
    
    return {
        "total": total,
        "unread": unread,
        "by_priority": dict(by_priority),
        "by_type": dict(by_type)
    }

@app.put("/notifications/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification = db.query(models.Notification)\
        .filter(models.Notification.id == notification_id)\
        .first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    return {"status": "success"}

# 알림 템플릿 관련 API
@app.post("/notification-templates/", response_model=schemas.NotificationTemplate)
async def create_notification_template(
    template: schemas.NotificationTemplateCreate,
    db: Session = Depends(get_db)
):
    db_template = models.NotificationTemplate(**template.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@app.get("/notification-templates/", response_model=List[schemas.NotificationTemplate])
async def get_notification_templates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    templates = db.query(models.NotificationTemplate)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return templates

@app.get("/notification-templates/{template_id}", response_model=schemas.NotificationTemplate)
async def get_notification_template(
    template_id: int,
    db: Session = Depends(get_db)
):
    template = db.query(models.NotificationTemplate)\
        .filter(models.NotificationTemplate.id == template_id)\
        .first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

# 알림 일괄 처리 API
@app.put("/notifications/bulk-update")
async def bulk_update_notifications(
    update: schemas.BulkNotificationUpdate,
    db: Session = Depends(get_db)
):
    db.query(models.Notification)\
        .filter(models.Notification.id.in_(update.notification_ids))\
        .update({"is_read": update.is_read}, synchronize_session=False)
    db.commit()
    return {"status": "success", "updated_count": len(update.notification_ids)}

# 알림 통계 API
@app.get("/notifications/{user_id}/stats", response_model=List[schemas.NotificationStats])
async def get_notification_stats(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.NotificationStats)\
        .filter(models.NotificationStats.user_id == user_id)
    
    if start_date:
        query = query.filter(models.NotificationStats.date >= start_date)
    if end_date:
        query = query.filter(models.NotificationStats.date <= end_date)
    
    stats = query.order_by(models.NotificationStats.date.desc()).all()
    return stats

# 알림 자동 정리 API
@app.post("/notifications/cleanup")
async def cleanup_notifications(
    config: schemas.NotificationCleanupConfig,
    db: Session = Depends(get_db)
):
    cutoff_date = datetime.utcnow() - timedelta(days=config.days_to_keep)
    query = db.query(models.Notification)\
        .filter(models.Notification.created_at < cutoff_date)
    
    if config.keep_unread:
        query = query.filter(models.Notification.is_read == True)
    if config.keep_high_priority:
        query = query.filter(models.Notification.priority < 2)
    
    deleted_count = query.delete()
    db.commit()
    return {"status": "success", "deleted_count": deleted_count}

# 알림 생성 헬퍼 함수
async def create_notification_from_template(
    template_id: int,
    user_id: int,
    variables: dict,
    db: Session
) -> models.Notification:
    template = db.query(models.NotificationTemplate)\
        .filter(models.NotificationTemplate.id == template_id)\
        .first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # 템플릿 변수 검증
    if template.variables:
        missing_vars = set(template.variables.keys()) - set(variables.keys())
        if missing_vars:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required variables: {', '.join(missing_vars)}"
            )
    
    # 템플릿 적용
    title = template.title_template.format(**variables)
    message = template.message_template.format(**variables)
    
    notification = models.Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=template.type,
        group=template.group,
        category=template.category,
        priority=template.priority,
        metadata=variables
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    # WebSocket을 통해 실시간 알림 전송
    await manager.send_notification(
        user_id,
        {
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "type": notification.type,
            "created_at": notification.created_at.isoformat()
        }
    )
    
    return notification

# 템플릿을 사용한 알림 생성 API
@app.post("/notifications/from-template/{template_id}")
async def create_notification_from_template_endpoint(
    template_id: int,
    user_id: int,
    variables: dict,
    db: Session = Depends(get_db)
):
    notification = await create_notification_from_template(template_id, user_id, variables, db)
    return notification

# 일일 통계 업데이트 스케줄러
async def update_daily_stats():
    while True:
        try:
            db = SessionLocal()
            today = datetime.utcnow().date()
            
            # 모든 사용자에 대해 통계 업데이트
            users = db.query(models.User).all()
            for user in users:
                # 기존 통계 확인
                existing_stats = db.query(models.NotificationStats)\
                    .filter(models.NotificationStats.user_id == user.id)\
                    .filter(models.NotificationStats.date == today)\
                    .first()
                
                if not existing_stats:
                    # 새로운 통계 생성
                    stats = models.NotificationStats(
                        user_id=user.id,
                        date=today
                    )
                    db.add(stats)
                else:
                    stats = existing_stats
                
                # 통계 업데이트
                notifications = db.query(models.Notification)\
                    .filter(models.Notification.user_id == user.id)\
                    .filter(models.Notification.created_at >= today)\
                    .all()
                
                stats.total_count = len(notifications)
                stats.read_count = sum(1 for n in notifications if n.is_read)
                stats.unread_count = stats.total_count - stats.read_count
                
                # 타입별 통계
                by_type = {}
                for n in notifications:
                    by_type[n.type] = by_type.get(n.type, 0) + 1
                stats.by_type = by_type
                
                # 우선순위별 통계
                by_priority = {}
                for n in notifications:
                    by_priority[n.priority] = by_priority.get(n.priority, 0) + 1
                stats.by_priority = by_priority
                
                # 그룹별 통계
                by_group = {}
                for n in notifications:
                    if n.group:
                        by_group[n.group] = by_group.get(n.group, 0) + 1
                stats.by_group = by_group
            
            db.commit()
        except Exception as e:
            print(f"Error updating daily stats: {e}")
        finally:
            db.close()
        
        # 24시간 대기
        await asyncio.sleep(24 * 60 * 60)

# 알림 템플릿 카테고리 API
@app.post("/notification-template-categories/", response_model=schemas.NotificationTemplateCategory)
async def create_template_category(
    category: schemas.NotificationTemplateCategoryCreate,
    db: Session = Depends(get_db)
):
    db_category = models.NotificationTemplateCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/notification-template-categories/", response_model=List[schemas.NotificationTemplateCategory])
async def get_template_categories(
    db: Session = Depends(get_db)
):
    categories = db.query(models.NotificationTemplateCategory)\
        .filter(models.NotificationTemplateCategory.parent_id == None)\
        .all()
    return categories

# 알림 템플릿 버전 관리 API
@app.post("/notification-templates/{template_id}/versions", response_model=schemas.NotificationTemplateVersion)
async def create_template_version(
    template_id: int,
    version: schemas.NotificationTemplateVersionCreate,
    db: Session = Depends(get_db)
):
    # 기존 활성 버전 비활성화
    db.query(models.NotificationTemplateVersion)\
        .filter(models.NotificationTemplateVersion.template_id == template_id)\
        .filter(models.NotificationTemplateVersion.is_active == True)\
        .update({"is_active": False})
    
    db_version = models.NotificationTemplateVersion(**version.dict())
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version

@app.get("/notification-templates/{template_id}/versions", response_model=List[schemas.NotificationTemplateVersion])
async def get_template_versions(
    template_id: int,
    db: Session = Depends(get_db)
):
    versions = db.query(models.NotificationTemplateVersion)\
        .filter(models.NotificationTemplateVersion.template_id == template_id)\
        .order_by(models.NotificationTemplateVersion.created_at.desc())\
        .all()
    return versions

# 알림 정리 스케줄링 API
@app.post("/notification-cleanup-schedules/", response_model=schemas.NotificationCleanupSchedule)
async def create_cleanup_schedule(
    schedule: schemas.NotificationCleanupScheduleCreate,
    db: Session = Depends(get_db)
):
    db_schedule = models.NotificationCleanupSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.get("/notification-cleanup-schedules/", response_model=List[schemas.NotificationCleanupSchedule])
async def get_cleanup_schedules(
    db: Session = Depends(get_db)
):
    schedules = db.query(models.NotificationCleanupSchedule).all()
    return schedules

# 알림 리포트 생성 API
@app.post("/notification-reports/generate", response_model=schemas.NotificationReport)
async def generate_notification_report(
    request: schemas.ReportGenerationRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    # 리포트 데이터 수집
    stats = db.query(models.NotificationStats)\
        .filter(models.NotificationStats.user_id == user_id)\
        .filter(models.NotificationStats.date >= request.start_date)\
        .filter(models.NotificationStats.date <= request.end_date)\
        .all()
    
    # 리포트 데이터 구성
    report_data = {
        "summary": {
            "total_notifications": sum(stat.total_count for stat in stats),
            "read_notifications": sum(stat.read_count for stat in stats),
            "unread_notifications": sum(stat.unread_count for stat in stats),
        },
        "daily_stats": [
            {
                "date": stat.date.isoformat(),
                "total": stat.total_count,
                "read": stat.read_count,
                "unread": stat.unread_count,
                "by_type": stat.by_type,
                "by_priority": stat.by_priority,
                "by_group": stat.by_group
            }
            for stat in stats
        ]
    }
    
    # 리포트 저장
    report = models.NotificationReport(
        user_id=user_id,
        report_type=request.report_type,
        start_date=request.start_date,
        end_date=request.end_date,
        report_data=report_data
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    # 리포트 파일 생성 (PDF, Excel, CSV 등)
    if request.format == "pdf":
        report.file_path = await generate_pdf_report(report_data, request)
    elif request.format == "excel":
        report.file_path = await generate_excel_report(report_data, request)
    elif request.format == "csv":
        report.file_path = await generate_csv_report(report_data, request)
    
    db.commit()
    return report

@app.get("/notification-reports/{report_id}", response_model=schemas.NotificationReport)
async def get_notification_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    report = db.query(models.NotificationReport)\
        .filter(models.NotificationReport.id == report_id)\
        .first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

# 정리 스케줄러 실행 함수
async def run_cleanup_schedules():
    while True:
        try:
            db = SessionLocal()
            now = datetime.utcnow()
            
            # 실행할 스케줄 찾기
            schedules = db.query(models.NotificationCleanupSchedule)\
                .filter(models.NotificationCleanupSchedule.is_active == True)\
                .all()
            
            for schedule in schedules:
                if should_run_schedule(schedule, now):
                    # 정리 작업 실행
                    cutoff_date = now - timedelta(days=schedule.days_to_keep)
                    query = db.query(models.Notification)\
                        .filter(models.Notification.created_at < cutoff_date)
                    
                    if schedule.keep_unread:
                        query = query.filter(models.Notification.is_read == True)
                    if schedule.keep_high_priority:
                        query = query.filter(models.Notification.priority < 2)
                    
                    deleted_count = query.delete()
                    
                    # 마지막 실행 시간 업데이트
                    schedule.last_run = now
                    db.commit()
                    
                    print(f"Cleaned up {deleted_count} notifications for schedule {schedule.name}")
        
        except Exception as e:
            print(f"Error running cleanup schedules: {e}")
        finally:
            db.close()
        
        # 1시간마다 체크
        await asyncio.sleep(3600)

def should_run_schedule(schedule: models.NotificationCleanupSchedule, now: datetime) -> bool:
    if not schedule.last_run:
        return True
    
    if schedule.schedule_type == "daily":
        return (now - schedule.last_run).days >= 1
    elif schedule.schedule_type == "weekly":
        return (now - schedule.last_run).days >= 7
    elif schedule.schedule_type == "monthly":
        return (now - schedule.last_run).days >= 30
    
    return False

# 서버 시작 시 스케줄러 시작
@app.on_event("startup")
async def startup_event():
    app_logger.info("서버가 시작되었습니다.")
    asyncio.create_task(update_daily_stats())
    asyncio.create_task(run_cleanup_schedules())

# 서버 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("서버가 종료되었습니다.")

# 커스텀 Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{settings.PROJECT_NAME} - API 문서",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

# OpenAPI 스키마
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="건설 관리 시스템 API 문서",
        routes=app.routes,
    )

# 메트릭 엔드포인트
@app.get("/metrics")
async def metrics():
    return get_metrics()

# 헬스 체크 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    # 개발 서버 실행 (호스트: 0.0.0.0, 포트: 8000)
    uvicorn.run(app, host="0.0.0.0", port=8000) 