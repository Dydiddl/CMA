from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models.daily_report import (
    DailyReport,
    WorkEntry,
    SafetyCheck,
    QualityCheck,
    DailyReportAttachment,
    WeatherCondition,
    WorkStatus
)
from app.schemas.daily_report import (
    DailyReportCreate,
    DailyReportUpdate,
    WorkEntryCreate,
    WorkEntryUpdate,
    SafetyCheckCreate,
    SafetyCheckUpdate,
    QualityCheckCreate,
    QualityCheckUpdate,
    DailyReportAttachmentCreate,
    DailyReportFilter
)

def create_daily_report(db: Session, report: DailyReportCreate, user_id: int) -> DailyReport:
    db_report = DailyReport(
        **report.dict(),
        created_by=user_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_daily_report(db: Session, report_id: int) -> Optional[DailyReport]:
    return db.query(DailyReport).filter(DailyReport.id == report_id).first()

def get_daily_reports(
    db: Session,
    filter_params: DailyReportFilter
) -> List[DailyReport]:
    query = db.query(DailyReport)
    
    if filter_params.project_id:
        query = query.filter(DailyReport.project_id == filter_params.project_id)
    if filter_params.start_date:
        query = query.filter(DailyReport.report_date >= filter_params.start_date)
    if filter_params.end_date:
        query = query.filter(DailyReport.report_date <= filter_params.end_date)
    if filter_params.weather_condition:
        query = query.filter(DailyReport.weather_condition == filter_params.weather_condition)
    if filter_params.work_status:
        query = query.filter(DailyReport.work_status == filter_params.work_status)
    if filter_params.created_by:
        query = query.filter(DailyReport.created_by == filter_params.created_by)
    
    return query.offset(filter_params.skip).limit(filter_params.limit).all()

def update_daily_report(
    db: Session,
    report_id: int,
    report_update: DailyReportUpdate
) -> Optional[DailyReport]:
    db_report = get_daily_report(db, report_id)
    if not db_report:
        return None
    
    update_data = report_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_report, field, value)
    
    db_report.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_report)
    return db_report

def delete_daily_report(db: Session, report_id: int) -> bool:
    db_report = get_daily_report(db, report_id)
    if not db_report:
        return False
    
    db.delete(db_report)
    db.commit()
    return True

# 작업 항목 CRUD
def create_work_entry(
    db: Session,
    report_id: int,
    work_entry: WorkEntryCreate
) -> WorkEntry:
    db_work_entry = WorkEntry(
        **work_entry.dict(),
        daily_report_id=report_id
    )
    db.add(db_work_entry)
    db.commit()
    db.refresh(db_work_entry)
    return db_work_entry

def get_work_entry(db: Session, entry_id: int) -> Optional[WorkEntry]:
    return db.query(WorkEntry).filter(WorkEntry.id == entry_id).first()

def update_work_entry(
    db: Session,
    entry_id: int,
    work_entry_update: WorkEntryUpdate
) -> Optional[WorkEntry]:
    db_work_entry = get_work_entry(db, entry_id)
    if not db_work_entry:
        return None
    
    update_data = work_entry_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_work_entry, field, value)
    
    db_work_entry.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_work_entry)
    return db_work_entry

def delete_work_entry(db: Session, entry_id: int) -> bool:
    db_work_entry = get_work_entry(db, entry_id)
    if not db_work_entry:
        return False
    
    db.delete(db_work_entry)
    db.commit()
    return True

# 안전 점검 CRUD
def create_safety_check(
    db: Session,
    report_id: int,
    safety_check: SafetyCheckCreate,
    user_id: int
) -> SafetyCheck:
    db_safety_check = SafetyCheck(
        **safety_check.dict(),
        daily_report_id=report_id,
        checked_by=user_id
    )
    db.add(db_safety_check)
    db.commit()
    db.refresh(db_safety_check)
    return db_safety_check

def get_safety_check(db: Session, check_id: int) -> Optional[SafetyCheck]:
    return db.query(SafetyCheck).filter(SafetyCheck.id == check_id).first()

def update_safety_check(
    db: Session,
    check_id: int,
    safety_check_update: SafetyCheckUpdate
) -> Optional[SafetyCheck]:
    db_safety_check = get_safety_check(db, check_id)
    if not db_safety_check:
        return None
    
    update_data = safety_check_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_safety_check, field, value)
    
    db_safety_check.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_safety_check)
    return db_safety_check

def delete_safety_check(db: Session, check_id: int) -> bool:
    db_safety_check = get_safety_check(db, check_id)
    if not db_safety_check:
        return False
    
    db.delete(db_safety_check)
    db.commit()
    return True

# 품질 점검 CRUD
def create_quality_check(
    db: Session,
    report_id: int,
    quality_check: QualityCheckCreate,
    user_id: int
) -> QualityCheck:
    db_quality_check = QualityCheck(
        **quality_check.dict(),
        daily_report_id=report_id,
        checked_by=user_id
    )
    db.add(db_quality_check)
    db.commit()
    db.refresh(db_quality_check)
    return db_quality_check

def get_quality_check(db: Session, check_id: int) -> Optional[QualityCheck]:
    return db.query(QualityCheck).filter(QualityCheck.id == check_id).first()

def update_quality_check(
    db: Session,
    check_id: int,
    quality_check_update: QualityCheckUpdate
) -> Optional[QualityCheck]:
    db_quality_check = get_quality_check(db, check_id)
    if not db_quality_check:
        return None
    
    update_data = quality_check_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_quality_check, field, value)
    
    db_quality_check.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_quality_check)
    return db_quality_check

def delete_quality_check(db: Session, check_id: int) -> bool:
    db_quality_check = get_quality_check(db, check_id)
    if not db_quality_check:
        return False
    
    db.delete(db_quality_check)
    db.commit()
    return True

# 첨부파일 CRUD
def create_attachment(
    db: Session,
    report_id: int,
    attachment: DailyReportAttachmentCreate,
    user_id: int
) -> DailyReportAttachment:
    db_attachment = DailyReportAttachment(
        **attachment.dict(),
        daily_report_id=report_id,
        uploaded_by=user_id
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

def get_attachment(db: Session, attachment_id: int) -> Optional[DailyReportAttachment]:
    return db.query(DailyReportAttachment).filter(DailyReportAttachment.id == attachment_id).first()

def delete_attachment(db: Session, attachment_id: int) -> bool:
    db_attachment = get_attachment(db, attachment_id)
    if not db_attachment:
        return False
    
    db.delete(db_attachment)
    db.commit()
    return True

# 통계 조회
def get_daily_report_statistics(
    db: Session,
    project_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, Any]:
    query = db.query(DailyReport).filter(DailyReport.project_id == project_id)
    
    if start_date:
        query = query.filter(DailyReport.report_date >= start_date)
    if end_date:
        query = query.filter(DailyReport.report_date <= end_date)
    
    reports = query.all()
    
    # 기본 통계
    total_reports = len(reports)
    total_work_entries = sum(len(report.work_entries) for report in reports)
    total_safety_checks = sum(len(report.safety_checks) for report in reports)
    total_quality_checks = sum(len(report.quality_checks) for report in reports)
    
    # 작업 상태 분포
    work_status_distribution = {}
    for status in WorkStatus:
        count = sum(1 for report in reports if report.work_status == status)
        work_status_distribution[status.value] = count
    
    # 날씨 분포
    weather_distribution = {}
    for condition in WeatherCondition:
        count = sum(1 for report in reports if report.weather_condition == condition)
        weather_distribution[condition.value] = count
    
    # 평균 진행률
    progress_values = [report.work_progress for report in reports if report.work_progress is not None]
    average_progress = sum(progress_values) / len(progress_values) if progress_values else 0
    
    # 안전 점검 합격률
    safety_checks = [check for report in reports for check in report.safety_checks]
    safety_check_pass_rate = sum(1 for check in safety_checks if check.status) / len(safety_checks) if safety_checks else 0
    
    # 품질 점검 합격률
    quality_checks = [check for report in reports for check in report.quality_checks]
    quality_check_pass_rate = sum(1 for check in quality_checks if check.status) / len(quality_checks) if quality_checks else 0
    
    # 월별 추이
    monthly_trend = {}
    for report in reports:
        month_key = report.report_date.strftime("%Y-%m")
        monthly_trend[month_key] = monthly_trend.get(month_key, 0) + 1
    
    return {
        "total_reports": total_reports,
        "total_work_entries": total_work_entries,
        "total_safety_checks": total_safety_checks,
        "total_quality_checks": total_quality_checks,
        "work_status_distribution": work_status_distribution,
        "weather_distribution": weather_distribution,
        "average_progress": average_progress,
        "safety_check_pass_rate": safety_check_pass_rate,
        "quality_check_pass_rate": quality_check_pass_rate,
        "monthly_trend": monthly_trend
    } 