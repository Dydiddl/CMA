#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
재무 서비스 모듈 - 하이브리드 아키텍처 최적화
"""
import asyncio
import logging
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, date
import json
from functools import lru_cache

from app.models.financial import FinancialRecord, FinancialDocument
from app.schemas.financial import (
    FinancialRecordCreate, 
    FinancialRecordUpdate, 
    FinancialDocumentCreate
)
from app.core.exceptions import (
    FinancialRecordNotFoundException, 
    ValidationException, 
    DatabaseException
)
from app.core.cache import CacheManager

logger = logging.getLogger(__name__)


class FinancialService:
    """재무 서비스 클래스 - 성능 최적화 버전"""
    
    def __init__(self, db: Session, cache: Optional[CacheManager] = None):
        self.db = db
        self.cache = cache or CacheManager()
        self.cache_prefix = "financial"
        self.cache_ttl = 3600  # 1시간
    
    async def create_financial_record(
        self, 
        record_data: FinancialRecordCreate, 
        user_id: str
    ) -> FinancialRecord:
        """
        새로운 재무 기록을 생성합니다 - 비동기 처리 및 캐싱
        
        Args:
            record_data: 재무 기록 생성 데이터
            user_id: 생성자 사용자 ID
            
        Returns:
            FinancialRecord: 생성된 재무 기록 정보
            
        Raises:
            ValidationException: 데이터 검증 실패 시
            DatabaseException: 데이터베이스 오류 시
        """
        try:
            # 데이터 검증
            if record_data.amount <= 0:
                raise ValidationException("금액은 0보다 커야 합니다.")
            
            # 재무 기록 생성
            record = FinancialRecord(
                **record_data.dict(),
                user_id=user_id
            )
            self.db.add(record)
            await self._commit_with_retry()
            self.db.refresh(record)
            
            # 캐시 무효화
            await self._invalidate_financial_cache()
            
            logger.info(f"재무 기록 생성 완료: {record.id} - {record.amount}")
            return record
            
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"재무 기록 생성 실패: {e}")
            raise DatabaseException(f"재무 기록 생성 중 오류 발생: {e}")
    
    async def get_financial_records(
        self,
        skip: int = 0,
        limit: int = 10,
        type_filter: Optional[str] = None,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        contract_id: Optional[str] = None,
        vendor_id: Optional[str] = None
    ) -> Tuple[List[FinancialRecord], int]:
        """
        재무 기록 목록을 조회합니다 - 캐싱 및 필터링 최적화
        
        Args:
            skip: 건너뛸 레코드 수
            limit: 가져올 레코드 수
            type_filter: 거래 유형 필터
            category: 카테고리 필터
            start_date: 시작일
            end_date: 종료일
            contract_id: 계약 ID 필터
            vendor_id: 거래처 ID 필터
            
        Returns:
            Tuple[List[FinancialRecord], int]: 재무 기록 목록과 전체 개수
        """
        try:
            # 캐시 키 생성
            cache_key = f"{self.cache_prefix}:list:{skip}:{limit}:{type_filter}:{category}:{start_date}:{end_date}:{contract_id}:{vendor_id}"
            
            # 캐시에서 조회 시도
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # 데이터베이스 쿼리 최적화 (삭제되지 않은 기록만)
            query = self.db.query(FinancialRecord).filter(FinancialRecord.is_deleted.is_(False))
            
            # 필터 조건 적용
            if type_filter:
                query = query.filter(FinancialRecord.type == type_filter)
            
            if category:
                query = query.filter(FinancialRecord.category == category)
            
            if start_date:
                query = query.filter(FinancialRecord.transaction_date >= start_date)
            
            if end_date:
                query = query.filter(FinancialRecord.transaction_date <= end_date)
            
            if contract_id:
                query = query.filter(FinancialRecord.contract_id == contract_id)
            
            if vendor_id:
                query = query.filter(FinancialRecord.vendor_id == vendor_id)
            
            # 전체 개수 조회 (캐시 활용)
            total_cache_key = f"{self.cache_prefix}:total:{type_filter}:{category}:{start_date}:{end_date}:{contract_id}:{vendor_id}"
            total = await self.cache.get_or_set(
                total_cache_key,
                lambda: query.count(),
                ttl=1800  # 30분
            )
            
            # 정렬 및 페이징 적용
            records = query.order_by(desc(FinancialRecord.transaction_date)).offset(skip).limit(limit).all()
            
            # 결과 캐싱
            result = (records, total)
            await self.cache.setex(cache_key, self.cache_ttl, json.dumps(result))
            
            return result
            
        except Exception as e:
            logger.error(f"재무 기록 목록 조회 실패: {e}")
            raise DatabaseException(f"재무 기록 목록 조회 중 오류 발생: {e}")
    
    async def get_financial_record_by_id(self, record_id: str) -> Optional[FinancialRecord]:
        """
        재무 기록 ID로 조회 - 캐싱 적용
        
        Args:
            record_id: 재무 기록 ID
            
        Returns:
            FinancialRecord: 재무 기록 정보
        """
        try:
            # 캐시에서 조회 시도
            cache_key = f"{self.cache_prefix}:{record_id}"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return FinancialRecord.parse_raw(cached_result)
            
            # 데이터베이스 조회 (삭제되지 않은 기록만)
            record = self.db.query(FinancialRecord).filter(
                FinancialRecord.id == record_id,
                FinancialRecord.is_deleted.is_(False)
            ).first()
            
            if record:
                # 캐싱
                await self.cache.setex(cache_key, self.cache_ttl, record.json())
            
            return record
            
        except Exception as e:
            logger.error(f"재무 기록 조회 실패: {e}")
            raise DatabaseException(f"재무 기록 조회 중 오류 발생: {e}")
    
    async def update_financial_record(
        self, 
        record_id: str, 
        record_update: FinancialRecordUpdate
    ) -> Optional[FinancialRecord]:
        """
        재무 기록 정보를 수정합니다 - 검증 및 캐싱 무효화
        
        Args:
            record_id: 재무 기록 ID
            record_update: 수정할 재무 기록 데이터
            
        Returns:
            FinancialRecord: 수정된 재무 기록 정보
        """
        try:
            # 재무 기록 존재 확인
            record = await self.get_financial_record_by_id(record_id)
            if not record:
                return None
            
            # 데이터 검증
            if record_update.amount and record_update.amount <= 0:
                raise ValidationException("금액은 0보다 커야 합니다.")
            
            # 업데이트할 데이터만 추출
            update_data = record_update.dict(exclude_unset=True)
            
            # 재무 기록 정보 업데이트
            for field, value in update_data.items():
                setattr(record, field, value)
            
            await self._commit_with_retry()
            self.db.refresh(record)
            
            # 캐시 무효화
            await self._invalidate_financial_cache(record_id)
            
            logger.info(f"재무 기록 수정 완료: {record_id}")
            return record
            
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"재무 기록 수정 실패: {e}")
            raise DatabaseException(f"재무 기록 수정 중 오류 발생: {e}")
    
    async def delete_financial_record(self, record_id: str) -> bool:
        """
        재무 기록을 삭제합니다 - 소프트 삭제 적용
        
        Args:
            record_id: 재무 기록 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            record = await self.get_financial_record_by_id(record_id)
            if not record:
                return False
            
            # 소프트 삭제 (실제 삭제 대신 상태 변경)
            record.status = "삭제됨"
            record.deleted_at = datetime.utcnow()
            record.is_deleted = True
            
            await self._commit_with_retry()
            
            # 캐시 무효화
            await self._invalidate_financial_cache(record_id)
            
            logger.info(f"재무 기록 삭제 완료: {record_id}")
            return True
            
        except Exception as e:
            logger.error(f"재무 기록 삭제 실패: {e}")
            raise DatabaseException(f"재무 기록 삭제 중 오류 발생: {e}")
    
    async def create_financial_document(
        self, 
        record_id: str, 
        document_data: FinancialDocumentCreate
    ) -> FinancialDocument:
        """
        재무 문서를 생성합니다
        
        Args:
            record_id: 재무 기록 ID
            document_data: 문서 생성 데이터
            
        Returns:
            FinancialDocument: 생성된 문서 정보
        """
        try:
            # 재무 기록 존재 확인
            record = await self.get_financial_record_by_id(record_id)
            if not record:
                raise FinancialRecordNotFoundException("재무 기록을 찾을 수 없습니다.")
            
            # 문서 생성
            document = FinancialDocument(
                **document_data.dict(),
                financial_record_id=record_id
            )
            self.db.add(document)
            await self._commit_with_retry()
            self.db.refresh(document)
            
            # 캐시 무효화
            await self._invalidate_financial_cache(record_id)
            
            logger.info(f"재무 문서 생성 완료: {document.id}")
            return document
            
        except FinancialRecordNotFoundException:
            raise
        except Exception as e:
            logger.error(f"재무 문서 생성 실패: {e}")
            raise DatabaseException(f"재무 문서 생성 중 오류 발생: {e}")
    
    async def get_financial_documents(self, record_id: str) -> List[FinancialDocument]:
        """
        재무 기록의 모든 문서를 조회합니다
        
        Args:
            record_id: 재무 기록 ID
            
        Returns:
            List[FinancialDocument]: 문서 목록
        """
        try:
            # 캐시에서 조회 시도
            cache_key = f"{self.cache_prefix}:documents:{record_id}"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return [FinancialDocument.parse_raw(doc) for doc in json.loads(cached_result)]
            
            # 데이터베이스 조회
            documents = self.db.query(FinancialDocument).filter(
                FinancialDocument.financial_record_id == record_id
            ).all()
            
            # 캐싱
            await self.cache.setex(cache_key, self.cache_ttl, json.dumps([doc.json() for doc in documents]))
            
            return documents
            
        except Exception as e:
            logger.error(f"재무 문서 조회 실패: {e}")
            raise DatabaseException(f"재무 문서 조회 중 오류 발생: {e}")
    
    # 성능 최적화를 위한 헬퍼 메서드들
    
    async def _commit_with_retry(self, max_retries: int = 3):
        """데이터베이스 커밋 재시도 로직"""
        for attempt in range(max_retries):
            try:
                self.db.commit()
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"커밋 재시도 {attempt + 1}/{max_retries}: {e}")
                await asyncio.sleep(0.1 * (attempt + 1))
    
    async def _invalidate_financial_cache(self, record_id: Optional[str] = None):
        """재무 관련 캐시 무효화"""
        try:
            if record_id:
                # 특정 재무 기록 캐시 무효화
                patterns = [
                    f"{self.cache_prefix}:{record_id}",
                    f"{self.cache_prefix}:documents:{record_id}"
                ]
            else:
                # 모든 재무 캐시 무효화
                patterns = [f"{self.cache_prefix}:*"]
            
            for pattern in patterns:
                await self.cache.delete_pattern(pattern)
                
        except Exception as e:
            logger.warning(f"캐시 무효화 실패: {e}")
    
    @lru_cache(maxsize=1000)
    def _get_financial_categories(self) -> List[str]:
        """재무 카테고리 옵션 조회 - 캐시된 함수"""
        return ["자재비", "노무비", "경비", "계약금", "중도금", "잔금", "기타"]
    
    @lru_cache(maxsize=1000)
    def _get_payment_methods(self) -> List[str]:
        """결제 방법 옵션 조회 - 캐시된 함수"""
        return ["현금", "계좌이체", "카드", "어음", "기타"]
    
    async def get_financial_statistics(self) -> Dict[str, Any]:
        """재무 통계 정보 조회 - 대시보드용"""
        try:
            cache_key = f"{self.cache_prefix}:statistics"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # 통계 쿼리 최적화 (삭제되지 않은 기록만)
            income_stats = self.db.query(
                func.sum(FinancialRecord.amount).label('total_income')
            ).filter(
                FinancialRecord.type == "수입",
                FinancialRecord.is_deleted.is_(False)
            ).scalar() or 0
            
            expense_stats = self.db.query(
                func.sum(FinancialRecord.amount).label('total_expense')
            ).filter(
                FinancialRecord.type == "지출",
                FinancialRecord.is_deleted.is_(False)
            ).scalar() or 0
            
            category_stats = self.db.query(
                FinancialRecord.category,
                func.sum(FinancialRecord.amount).label('total_amount')
            ).filter(FinancialRecord.is_deleted.is_(False)).group_by(FinancialRecord.category).all()
            
            result = {
                "total_income": income_stats,
                "total_expense": expense_stats,
                "net_profit": income_stats - expense_stats,
                "by_category": {s.category: s.total_amount for s in category_stats}
            }
            
            # 캐싱 (짧은 TTL)
            await self.cache.setex(cache_key, 1800, json.dumps(result))
            
            return result
            
        except Exception as e:
            logger.error(f"재무 통계 조회 실패: {e}")
            return {"total_income": 0, "total_expense": 0, "net_profit": 0, "by_category": {}}
    
    async def get_monthly_summary(self, year: int, month: int) -> Dict[str, Any]:
        """월별 재무 요약 조회"""
        try:
            cache_key = f"{self.cache_prefix}:monthly:{year}:{month}"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # 월별 통계 쿼리 (삭제되지 않은 기록만)
            monthly_stats = self.db.query(
                FinancialRecord.type,
                func.sum(FinancialRecord.amount).label('total_amount'),
                func.count(FinancialRecord.id).label('count')
            ).filter(
                func.extract('year', FinancialRecord.transaction_date) == year,
                func.extract('month', FinancialRecord.transaction_date) == month,
                FinancialRecord.is_deleted.is_(False)
            ).group_by(FinancialRecord.type).all()
            
            result = {
                "year": year,
                "month": month,
                "income": next((s.total_amount for s in monthly_stats if s.type == "수입"), 0),
                "expense": next((s.total_amount for s in monthly_stats if s.type == "지출"), 0),
                "transaction_count": sum(s.count for s in monthly_stats)
            }
            result["net_profit"] = result["income"] - result["expense"]
            
            # 캐싱
            await self.cache.setex(cache_key, 3600, json.dumps(result))
            
            return result
            
        except Exception as e:
            logger.error(f"월별 요약 조회 실패: {e}")
            return {"year": year, "month": month, "income": 0, "expense": 0, "net_profit": 0, "transaction_count": 0}


# 기존 함수들도 유지 (호환성)
def create_financial_record(db: Session, record: FinancialRecordCreate) -> FinancialRecord:
    """재무 기록을 생성합니다."""
    # TODO: 실제 DB 저장 로직 구현
    pass


def get_financial_records(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    contract_id: Optional[int] = None,
    vendor_id: Optional[int] = None
) -> List[FinancialRecord]:
    """재무 기록 목록을 조회합니다."""
    # TODO: 실제 DB 조회 로직 구현
    return []


def get_financial_record(db: Session, record_id: int) -> Optional[FinancialRecord]:
    """특정 재무 기록을 조회합니다."""
    # TODO: 실제 DB 조회 로직 구현
    return None


def update_financial_record(
    db: Session, 
    record_id: int, 
    record: FinancialRecordUpdate
) -> Optional[FinancialRecord]:
    """재무 기록을 업데이트합니다."""
    # TODO: 실제 DB 업데이트 로직 구현
    return None


def delete_financial_record(db: Session, record_id: int) -> bool:
    """재무 기록을 삭제합니다."""
    # TODO: 실제 DB 삭제 로직 구현
    return False


def create_financial_document(
    db: Session, 
    record_id: int, 
    document: FinancialDocumentCreate
) -> FinancialDocument:
    """재무 문서를 생성합니다."""
    # TODO: 실제 DB 저장 로직 구현
    pass


def get_financial_documents(db: Session, record_id: int) -> List[FinancialDocument]:
    """재무 문서 목록을 조회합니다."""
    # TODO: 실제 DB 조회 로직 구현
    return [] 