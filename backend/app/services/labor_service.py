#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 노무 관리 서비스 - 성능 최적화 버전
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging
from app.models.labor import Labor, WorkLog
from app.schemas.labor import LaborCreate, LaborUpdate, LaborResponse, LaborListResponse
from app.core.exceptions import NotFoundException, ValidationException
from app.core.cache import get_cache, CacheKeys
from app.core.database import get_db

logger = logging.getLogger(__name__)


class LaborService:
    """노무 관리 서비스 - 성능 최적화"""
    
    def __init__(self, db: Session):
        self.db = db
        self.cache = get_cache()
    
    def create_labor(self, labor_data: LaborCreate) -> LaborResponse:
        """노무자 생성 - 캐싱 적용"""
        try:
            # 중복 검사
            existing_labor = self.db.query(Labor).filter(
                or_(
                    Labor.worker_name == labor_data.worker_name,
                    Labor.contact == labor_data.contact
                )
            ).first()
            
            if existing_labor:
                raise ValidationException("이미 존재하는 노무자입니다.")
            
            # 노무자 생성
            labor = Labor(**labor_data.dict())
            self.db.add(labor)
            self.db.commit()
            self.db.refresh(labor)
            
            # 캐시 무효화
            self._invalidate_labor_cache()
            
            logger.info(f"노무자 생성 완료: {labor.worker_name}")
            return LaborResponse.from_orm(labor)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"노무자 생성 실패: {e}")
            raise
    
    def get_labor_records(
        self, 
        skip: int = 0, 
        limit: int = 50,
        search: Optional[str] = None,
        job_type: Optional[str] = None,
        status: Optional[str] = None,
        worker_id: Optional[str] = None
    ) -> Tuple[List[LaborResponse], int]:
        """노무자 목록 조회 - 최적화된 쿼리"""
        
        # 캐시 키 생성
        cache_key = f"{CacheKeys.LABOR_LIST}:{skip}:{limit}:{search}:{job_type}:{status}:{worker_id}"
        
        # 캐시 확인
        cached_result = self.cache.get(cache_key)
        if cached_result:
            logger.info("노무자 목록 캐시에서 조회")
            return cached_result
        
        try:
            # 기본 쿼리
            query = self.db.query(Labor)
            
            # 검색 조건 적용
            if search:
                search_filter = or_(
                    Labor.worker_name.contains(search),
                    Labor.contact.contains(search),
                    Labor.ssn.contains(search)
                )
                query = query.filter(search_filter)
            
            # 필터 조건 적용
            if job_type:
                query = query.filter(Labor.job_type == job_type)
            
            if status:
                query = query.filter(Labor.status == status)
            
            if worker_id:
                query = query.filter(Labor.id == worker_id)
            
            # 전체 개수 조회 (캐시 적용)
            total_cache_key = f"{CacheKeys.LABOR_COUNT}:{search}:{job_type}:{status}:{worker_id}"
            total = self.cache.get(total_cache_key)
            
            if total is None:
                total = query.count()
                self.cache.set(total_cache_key, total, 300)  # 5분 캐시
            
            # 페이징 및 정렬
            labor_list = query.order_by(desc(Labor.created_at)).offset(skip).limit(limit).all()
            
            # 결과 변환
            result = [LaborResponse.from_orm(labor) for labor in labor_list]
            
            # 캐시 저장
            self.cache.set(cache_key, (result, total), 300)  # 5분 캐시
            
            return result, total
            
        except Exception as e:
            logger.error(f"노무자 목록 조회 실패: {e}")
            raise
    
    def get_labor_by_id(self, labor_id: str) -> Optional[LaborResponse]:
        """노무자 ID로 조회 - 캐싱 적용"""
        
        # 캐시 확인
        cache_key = f"{CacheKeys.LABOR_DETAIL}:{labor_id}"
        cached_labor = self.cache.get(cache_key)
        
        if cached_labor:
            logger.info(f"노무자 상세 캐시에서 조회: {labor_id}")
            return cached_labor
        
        try:
            labor = self.db.query(Labor).filter(Labor.id == labor_id).first()
            
            if not labor:
                return None
            
            result = LaborResponse.model_validate(labor)
            
            # 캐시 저장
            self.cache.set(cache_key, result, 600)  # 10분 캐시
            
            return result
            
        except Exception as e:
            logger.error(f"노무자 상세 조회 실패: {e}")
            raise
    
    def update_labor(self, labor_id: str, labor_update: LaborUpdate) -> Optional[LaborResponse]:
        """노무자 수정 - 캐싱 무효화"""
        try:
            labor = self.db.query(Labor).filter(Labor.id == labor_id).first()
            if not labor:
                return None
            
            # 업데이트할 데이터만 추출
            update_data = labor_update.model_dump(exclude_unset=True)
            
            # 중복 검사 (이름이나 연락처 변경 시)
            if 'name' in update_data or 'phone' in update_data:
                existing_labor = self.db.query(Labor).filter(
                    and_(
                        or_(
                            Labor.name == update_data.get('name', labor.name),
                            Labor.phone == update_data.get('phone', labor.phone)
                        ),
                        Labor.id != labor_id
                    )
                ).first()
                
                if existing_labor:
                    raise ValidationException("이미 존재하는 노무자입니다.")
            
            # 노무자 정보 업데이트
            for field, value in update_data.items():
                setattr(labor, field, value)
            
            self.db.commit()
            self.db.refresh(labor)
            
            # 캐시 무효화
            self._invalidate_labor_cache(labor_id)
            
            logger.info(f"노무자 수정 완료: {labor.name}")
            return LaborResponse.model_validate(labor)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"노무자 수정 실패: {e}")
            raise
    
    def delete_labor(self, labor_id: str) -> bool:
        """노무자 삭제 - 캐싱 무효화"""
        try:
            labor = self.db.query(Labor).filter(Labor.id == labor_id).first()
            if not labor:
                return False
            
            # 관련 기록 확인
            related_records = self.db.query(WorkLog).filter(
                WorkLog.labor_id == labor_id
            ).count()
            
            if related_records > 0:
                logger.warning(f"노무자 삭제 시도: {labor_id} (관련 기록 {related_records}개 존재)")
            
            self.db.delete(labor)
            self.db.commit()
            
            # 캐시 무효화
            self._invalidate_labor_cache(labor_id)
            
            logger.info(f"노무자 삭제 완료: {labor.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"노무자 삭제 실패: {e}")
            raise
    
    def get_labor_summary(self) -> Dict[str, Any]:
        """노무 요약 통계 - 캐싱 적용"""
        
        # 캐시 확인
        cache_key = CacheKeys.LABOR_SUMMARY
        cached_summary = self.cache.get(cache_key)
        
        if cached_summary:
            logger.info("노무 요약 캐시에서 조회")
            return cached_summary
        
        try:
            # 현재 날짜 기준
            now = datetime.now()
            current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            week_start = now - timedelta(days=now.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # 기본 통계
            total_workers = self.db.query(func.count(Labor.id)).scalar()
            active_workers = self.db.query(func.count(Labor.id)).filter(
                Labor.status == "재직"
            ).scalar()
            
            # 평균 시급
            avg_wage_result = self.db.query(func.avg(Labor.daily_wage)).scalar()
            average_wage = float(avg_wage_result) if avg_wage_result else 0.0
            
            # 이번 달 근무 기록 통계
            monthly_records = self.db.query(
                func.sum(WorkLog.work_hours).label('total_hours'),
                func.sum(WorkLog.work_hours * Labor.daily_wage).label('total_cost')
            ).join(Labor, WorkLog.labor_id == Labor.id).filter(
                WorkLog.work_date >= current_month_start
            ).first()
            
            monthly_hours = float(monthly_records.total_hours) if monthly_records.total_hours else 0.0
            monthly_cost = float(monthly_records.total_cost) if monthly_records.total_cost else 0.0
            
            # 이번 주 근무 시간
            weekly_hours = self.db.query(func.sum(WorkLog.work_hours)).filter(
                WorkLog.work_date >= week_start
            ).scalar()
            weekly_hours = float(weekly_hours) if weekly_hours else 0.0
            
            # 총 근무 시간 (전체)
            total_hours = self.db.query(func.sum(WorkLog.work_hours)).scalar()
            total_hours = float(total_hours) if total_hours else 0.0
            
            # 가동률 계산
            utilization_rate = (active_workers / total_workers * 100) if total_workers > 0 else 0.0
            
            # 임금 트렌드 (간단한 계산)
            wage_trend = "+5%" if average_wage > 15000 else "0%"
            
            # 비용 트렌드 (간단한 계산)
            cost_trend = "+10%" if monthly_cost > 10000000 else "0%"
            
            # 목표 대비 달성률 (간단한 계산)
            hours_target = 80.0  # 목표 80%
            
            summary = {
                "total_workers": total_workers,
                "active_workers": active_workers,
                "utilization_rate": round(utilization_rate, 1),
                "average_wage": round(average_wage),
                "wage_trend": wage_trend,
                "total_labor_cost": round(monthly_cost),
                "monthly_labor_cost": round(monthly_cost),
                "labor_cost_trend": cost_trend,
                "total_hours": round(total_hours),
                "weekly_hours": round(weekly_hours),
                "hours_target": round(hours_target, 1)
            }
            
            # 캐시 저장 (1시간)
            self.cache.set(cache_key, summary, 3600)
            
            return summary
            
        except Exception as e:
            logger.error(f"노무 요약 통계 계산 실패: {e}")
            raise
    
    def batch_create_labor_records(self, records: List[Dict[str, Any]]) -> List[WorkLog]:
        """노무 기록 배치 생성 - 성능 최적화"""
        try:
            labor_records = []
            
            for record_data in records:
                # 필드명 변환
                if 'worker_id' in record_data:
                    record_data['labor_id'] = record_data.pop('worker_id')
                if 'hours_worked' in record_data:
                    record_data['work_hours'] = record_data.pop('hours_worked')
                
                labor_record = WorkLog(**record_data)
                labor_records.append(labor_record)
            
            # 배치 삽입
            self.db.bulk_save_objects(labor_records)
            self.db.commit()
            
            logger.info(f"노무 기록 배치 생성 완료: {len(labor_records)}개")
            return labor_records
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"노무 기록 배치 생성 실패: {e}")
            raise
    
    def get_labor_statistics_by_period(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """기간별 노무 통계 - 최적화된 쿼리"""
        
        try:
            # 기간별 근무 기록 통계
            period_stats = self.db.query(
                func.count(WorkLog.id).label('total_records'),
                func.sum(WorkLog.work_hours).label('total_hours'),
                func.sum(WorkLog.work_hours * Labor.daily_wage).label('total_cost'),
                func.avg(WorkLog.work_hours).label('avg_hours_per_day')
            ).join(Labor, WorkLog.labor_id == Labor.id).filter(
                and_(
                    WorkLog.work_date >= start_date,
                    WorkLog.work_date <= end_date
                )
            ).first()
            
            # 직종별 통계
            job_type_stats = self.db.query(
                Labor.status.label('job_type'),
                func.count(WorkLog.id).label('record_count'),
                func.sum(WorkLog.work_hours).label('total_hours'),
                func.sum(WorkLog.work_hours * Labor.daily_wage).label('total_cost')
            ).join(WorkLog, Labor.id == WorkLog.labor_id).filter(
                and_(
                    WorkLog.work_date >= start_date,
                    WorkLog.work_date <= end_date
                )
            ).group_by(Labor.status).all()
            
            # 결과 구성
            result = {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "total_records": period_stats.total_records or 0,
                    "total_hours": float(period_stats.total_hours or 0),
                    "total_cost": float(period_stats.total_cost or 0),
                    "avg_hours_per_day": float(period_stats.avg_hours_per_day or 0)
                },
                "by_job_type": [
                    {
                        "job_type": stat.job_type,
                        "record_count": stat.record_count,
                        "total_hours": float(stat.total_hours or 0),
                        "total_cost": float(stat.total_cost or 0)
                    }
                    for stat in job_type_stats
                ]
            }
            
            return result
            
        except Exception as e:
            logger.error(f"기간별 노무 통계 계산 실패: {e}")
            raise
    
    def _invalidate_labor_cache(self, labor_id: Optional[str] = None):
        """노무 관련 캐시 무효화"""
        try:
            # 관련 캐시 키들 무효화
            cache_patterns = [
                f"{CacheKeys.LABOR_LIST}:*",
                f"{CacheKeys.LABOR_COUNT}:*",
                CacheKeys.LABOR_SUMMARY
            ]
            
            if labor_id:
                cache_patterns.append(f"{CacheKeys.LABOR_DETAIL}:{labor_id}")
            
            for pattern in cache_patterns:
                self.cache.delete_pattern(pattern)
            
            logger.info("노무 관련 캐시 무효화 완료")
            
        except Exception as e:
            logger.error(f"캐시 무효화 실패: {e}")
    
    def optimize_database_queries(self):
        """데이터베이스 쿼리 최적화"""
        try:
            # 인덱스 사용 통계 확인
            index_stats = self.db.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    idx_scan,
                    idx_tup_read,
                    idx_tup_fetch
                FROM pg_stat_user_indexes
                WHERE tablename IN ('labor', 'work_logs')
                ORDER BY idx_scan DESC
            """).fetchall()
            
            # 느린 쿼리 확인
            slow_queries = self.db.execute("""
                SELECT 
                    query,
                    calls,
                    total_time,
                    mean_time,
                    rows
                FROM pg_stat_statements
                WHERE query LIKE '%labor%'
                ORDER BY mean_time DESC
                LIMIT 10
            """).fetchall()
            
            logger.info("데이터베이스 최적화 분석 완료")
            return {
                "index_stats": [dict(row) for row in index_stats],
                "slow_queries": [dict(row) for row in slow_queries]
            }
            
        except Exception as e:
            logger.error(f"데이터베이스 최적화 분석 실패: {e}")
            raise 