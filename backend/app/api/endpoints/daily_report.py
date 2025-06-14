from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.crud import daily_report as crud
from app.schemas.daily_report import (
    DailyReport,
    DailyReportCreate,
    DailyReportUpdate,
    WorkEntry,
    WorkEntryCreate,
    WorkEntryUpdate,
    SafetyCheck,
    SafetyCheckCreate,
    SafetyCheckUpdate,
    QualityCheck,
    QualityCheckCreate,
    QualityCheckUpdate,
    DailyReportAttachment,
    DailyReportAttachmentCreate,
    DailyReportFilter,
    DailyReportStatistics
)

router = APIRouter()

# 일일 작업 일지 기본 CRUD
@router.post("/", response_model=DailyReport)
def create_daily_report(
    *,
    db: Session = Depends(deps.get_db),
    report_in: DailyReportCreate,
    current_user = Depends(deps.get_current_user)
) -> DailyReport:
    """
    새로운 일일 작업 일지를 생성합니다.
    """
    report = crud.create_daily_report(db, report_in, current_user.id)
    return report

@router.get("/{report_id}", response_model=DailyReport)
def get_daily_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    current_user = Depends(deps.get_current_user)
) -> DailyReport:
    """
    특정 일일 작업 일지를 조회합니다.
    """
    report = crud.get_daily_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="일일 작업 일지를 찾을 수 없습니다.")
    return report

@router.get("/", response_model=List[DailyReport])
def get_daily_reports(
    *,
    db: Session = Depends(deps.get_db),
    project_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    weather_condition: Optional[str] = None,
    work_status: Optional[str] = None,
    created_by: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
) -> List[DailyReport]:
    """
    일일 작업 일지 목록을 조회합니다.
    """
    filter_params = DailyReportFilter(
        project_id=project_id,
        start_date=start_date,
        end_date=end_date,
        weather_condition=weather_condition,
        work_status=work_status,
        created_by=created_by,
        skip=skip,
        limit=limit
    )
    reports = crud.get_daily_reports(db, filter_params)
    return reports

@router.put("/{report_id}", response_model=DailyReport)
def update_daily_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    report_in: DailyReportUpdate,
    current_user = Depends(deps.get_current_user)
) -> DailyReport:
    """
    일일 작업 일지를 업데이트합니다.
    """
    report = crud.update_daily_report(db, report_id, report_in)
    if not report:
        raise HTTPException(status_code=404, detail="일일 작업 일지를 찾을 수 없습니다.")
    return report

@router.delete("/{report_id}")
def delete_daily_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    current_user = Depends(deps.get_current_user)
) -> dict:
    """
    일일 작업 일지를 삭제합니다.
    """
    success = crud.delete_daily_report(db, report_id)
    if not success:
        raise HTTPException(status_code=404, detail="일일 작업 일지를 찾을 수 없습니다.")
    return {"message": "일일 작업 일지가 삭제되었습니다."}

# 작업 항목 CRUD
@router.post("/{report_id}/work-entries", response_model=WorkEntry)
def create_work_entry(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    work_entry_in: WorkEntryCreate,
    current_user = Depends(deps.get_current_user)
) -> WorkEntry:
    """
    일일 작업 일지에 새로운 작업 항목을 추가합니다.
    """
    work_entry = crud.create_work_entry(db, report_id, work_entry_in)
    return work_entry

@router.get("/{report_id}/work-entries", response_model=List[WorkEntry])
def get_work_entries(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    current_user = Depends(deps.get_current_user)
) -> List[WorkEntry]:
    """
    일일 작업 일지의 작업 항목 목록을 조회합니다.
    """
    report = crud.get_daily_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="일일 작업 일지를 찾을 수 없습니다.")
    return report.work_entries

@router.put("/work-entries/{entry_id}", response_model=WorkEntry)
def update_work_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_id: int,
    work_entry_in: WorkEntryUpdate,
    current_user = Depends(deps.get_current_user)
) -> WorkEntry:
    """
    작업 항목을 업데이트합니다.
    """
    work_entry = crud.update_work_entry(db, entry_id, work_entry_in)
    if not work_entry:
        raise HTTPException(status_code=404, detail="작업 항목을 찾을 수 없습니다.")
    return work_entry

@router.delete("/work-entries/{entry_id}")
def delete_work_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_id: int,
    current_user = Depends(deps.get_current_user)
) -> dict:
    """
    작업 항목을 삭제합니다.
    """
    success = crud.delete_work_entry(db, entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="작업 항목을 찾을 수 없습니다.")
    return {"message": "작업 항목이 삭제되었습니다."}

# 안전 점검 CRUD
@router.post("/{report_id}/safety-checks", response_model=SafetyCheck)
def create_safety_check(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    safety_check_in: SafetyCheckCreate,
    current_user = Depends(deps.get_current_user)
) -> SafetyCheck:
    """
    일일 작업 일지에 새로운 안전 점검을 추가합니다.
    """
    safety_check = crud.create_safety_check(db, report_id, safety_check_in, current_user.id)
    return safety_check

@router.get("/{report_id}/safety-checks", response_model=List[SafetyCheck])
def get_safety_checks(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    current_user = Depends(deps.get_current_user)
) -> List[SafetyCheck]:
    """
    일일 작업 일지의 안전 점검 목록을 조회합니다.
    """
    report = crud.get_daily_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="일일 작업 일지를 찾을 수 없습니다.")
    return report.safety_checks

@router.put("/safety-checks/{check_id}", response_model=SafetyCheck)
def update_safety_check(
    *,
    db: Session = Depends(deps.get_db),
    check_id: int,
    safety_check_in: SafetyCheckUpdate,
    current_user = Depends(deps.get_current_user)
) -> SafetyCheck:
    """
    안전 점검을 업데이트합니다.
    """
    safety_check = crud.update_safety_check(db, check_id, safety_check_in)
    if not safety_check:
        raise HTTPException(status_code=404, detail="안전 점검을 찾을 수 없습니다.")
    return safety_check

@router.delete("/safety-checks/{check_id}")
def delete_safety_check(
    *,
    db: Session = Depends(deps.get_db),
    check_id: int,
    current_user = Depends(deps.get_current_user)
) -> dict:
    """
    안전 점검을 삭제합니다.
    """
    success = crud.delete_safety_check(db, check_id)
    if not success:
        raise HTTPException(status_code=404, detail="안전 점검을 찾을 수 없습니다.")
    return {"message": "안전 점검이 삭제되었습니다."}

# 품질 점검 CRUD
@router.post("/{report_id}/quality-checks", response_model=QualityCheck)
def create_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    quality_check_in: QualityCheckCreate,
    current_user = Depends(deps.get_current_user)
) -> QualityCheck:
    """
    일일 작업 일지에 새로운 품질 점검을 추가합니다.
    """
    quality_check = crud.create_quality_check(db, report_id, quality_check_in, current_user.id)
    return quality_check

@router.get("/{report_id}/quality-checks", response_model=List[QualityCheck])
def get_quality_checks(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    current_user = Depends(deps.get_current_user)
) -> List[QualityCheck]:
    """
    일일 작업 일지의 품질 점검 목록을 조회합니다.
    """
    report = crud.get_daily_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="일일 작업 일지를 찾을 수 없습니다.")
    return report.quality_checks

@router.put("/quality-checks/{check_id}", response_model=QualityCheck)
def update_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    check_id: int,
    quality_check_in: QualityCheckUpdate,
    current_user = Depends(deps.get_current_user)
) -> QualityCheck:
    """
    품질 점검을 업데이트합니다.
    """
    quality_check = crud.update_quality_check(db, check_id, quality_check_in)
    if not quality_check:
        raise HTTPException(status_code=404, detail="품질 점검을 찾을 수 없습니다.")
    return quality_check

@router.delete("/quality-checks/{check_id}")
def delete_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    check_id: int,
    current_user = Depends(deps.get_current_user)
) -> dict:
    """
    품질 점검을 삭제합니다.
    """
    success = crud.delete_quality_check(db, check_id)
    if not success:
        raise HTTPException(status_code=404, detail="품질 점검을 찾을 수 없습니다.")
    return {"message": "품질 점검이 삭제되었습니다."}

# 첨부파일 관리
@router.post("/{report_id}/attachments", response_model=DailyReportAttachment)
async def create_attachment(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = None,
    current_user = Depends(deps.get_current_user)
) -> DailyReportAttachment:
    """
    일일 작업 일지에 새로운 첨부파일을 추가합니다.
    """
    # TODO: 파일 업로드 처리 로직 구현
    attachment_in = DailyReportAttachmentCreate(
        file_name=file.filename,
        file_path="",  # TODO: 실제 파일 경로 설정
        file_type=file.content_type,
        file_size=0,  # TODO: 실제 파일 크기 설정
        description=description
    )
    attachment = crud.create_attachment(db, report_id, attachment_in, current_user.id)
    return attachment

@router.get("/{report_id}/attachments", response_model=List[DailyReportAttachment])
def get_attachments(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    current_user = Depends(deps.get_current_user)
) -> List[DailyReportAttachment]:
    """
    일일 작업 일지의 첨부파일 목록을 조회합니다.
    """
    report = crud.get_daily_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="일일 작업 일지를 찾을 수 없습니다.")
    return report.attachments

@router.delete("/attachments/{attachment_id}")
def delete_attachment(
    *,
    db: Session = Depends(deps.get_db),
    attachment_id: int,
    current_user = Depends(deps.get_current_user)
) -> dict:
    """
    첨부파일을 삭제합니다.
    """
    success = crud.delete_attachment(db, attachment_id)
    if not success:
        raise HTTPException(status_code=404, detail="첨부파일을 찾을 수 없습니다.")
    return {"message": "첨부파일이 삭제되었습니다."}

# 통계 조회
@router.get("/statistics/{project_id}", response_model=DailyReportStatistics)
def get_statistics(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user = Depends(deps.get_current_user)
) -> DailyReportStatistics:
    """
    프로젝트의 일일 작업 일지 통계를 조회합니다.
    """
    statistics = crud.get_daily_report_statistics(db, project_id, start_date, end_date)
    return statistics 