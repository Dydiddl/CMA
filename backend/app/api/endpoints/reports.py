from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.project import project
from app.crud.task import task
from app.services.report_generator import ReportGenerator
from datetime import datetime, timedelta
import os

router = APIRouter()

@router.get("/project/{project_id}")
def generate_project_report(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    report_type: str = "pdf",
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    프로젝트 보고서 생성
    """
    # 프로젝트 정보 조회
    project_obj = project.get(db=db, id=project_id)
    if not project_obj:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다")
    
    # 프로젝트 작업 목록 조회
    tasks = task.get_multi_by_project(db=db, project_id=project_id)
    
    # 보고서 생성
    report_generator = ReportGenerator()
    report_path = report_generator.generate_project_report(
        project=project_obj,
        tasks=tasks,
        report_type=report_type
    )
    
    return FileResponse(
        path=report_path,
        filename=f"project_report_{project_id}_{datetime.now().strftime('%Y%m%d')}.{report_type}",
        media_type=f"application/{report_type}"
    )

@router.get("/tasks")
def generate_tasks_report(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime = None,
    end_date: datetime = None,
    status: str = None,
    report_type: str = "pdf",
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    작업 보고서 생성
    """
    # 작업 목록 조회
    tasks = task.get_multi_with_filters(
        db=db,
        start_date=start_date,
        end_date=end_date,
        status=status
    )
    
    # 보고서 생성
    report_generator = ReportGenerator()
    report_path = report_generator.generate_tasks_report(
        tasks=tasks,
        report_type=report_type
    )
    
    return FileResponse(
        path=report_path,
        filename=f"tasks_report_{datetime.now().strftime('%Y%m%d')}.{report_type}",
        media_type=f"application/{report_type}"
    )

@router.get("/summary")
def generate_summary_report(
    *,
    db: Session = Depends(deps.get_db),
    period: str = "month",  # week, month, quarter, year
    report_type: str = "pdf",
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    요약 보고서 생성
    """
    # 기간 설정
    end_date = datetime.now()
    if period == "week":
        start_date = end_date - timedelta(days=7)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    elif period == "quarter":
        start_date = end_date - timedelta(days=90)
    else:  # year
        start_date = end_date - timedelta(days=365)
    
    # 프로젝트 통계
    projects = project.get_multi_with_filters(
        db=db,
        start_date=start_date,
        end_date=end_date
    )
    
    # 작업 통계
    tasks = task.get_multi_with_filters(
        db=db,
        start_date=start_date,
        end_date=end_date
    )
    
    # 보고서 생성
    report_generator = ReportGenerator()
    report_path = report_generator.generate_summary_report(
        projects=projects,
        tasks=tasks,
        period=period,
        report_type=report_type
    )
    
    return FileResponse(
        path=report_path,
        filename=f"summary_report_{period}_{datetime.now().strftime('%Y%m%d')}.{report_type}",
        media_type=f"application/{report_type}"
    ) 