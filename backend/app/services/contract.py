"""
계약 서비스 모듈 - 하이브리드 아키텍처 최적화
"""
import asyncio
import logging
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
import json
from functools import lru_cache

from app.models.contract import Contract, ContractDocument
from app.schemas.contract import (
    ContractCreate, 
    ContractUpdate, 
    ContractDocumentCreate,
    ContractDetailResponse
)
from app.core.exceptions import (
    ContractNotFoundException, 
    ValidationException, 
    DatabaseException
)
from app.core.cache import CacheManager

logger = logging.getLogger(__name__)


class ContractService:
    """계약 서비스 클래스 - 성능 최적화 버전"""
    
    def __init__(self, db: Session, cache: Optional[CacheManager] = None):
        self.db = db
        self.cache = cache or CacheManager()
        self.cache_prefix = "contract"
        self.cache_ttl = 3600  # 1시간
    
    async def create_contract(self, contract_data: ContractCreate, user_id: str) -> Contract:
        """
        새로운 계약을 생성합니다 - 비동기 처리 및 캐싱
        
        Args:
            contract_data: 계약 생성 데이터
            user_id: 생성자 사용자 ID
            
        Returns:
            Contract: 생성된 계약 정보
            
        Raises:
            ValidationException: 계약번호 중복 시
            DatabaseException: 데이터베이스 오류 시
        """
        try:
            # 계약번호 중복 검사
            existing_contract = await self._check_contract_number_exists(contract_data.contract_number)
            if existing_contract:
                raise ValidationException("이미 존재하는 계약번호입니다.")
            
            # 계약 생성
            contract = Contract(**contract_data.dict(), user_id=user_id)
            self.db.add(contract)
            await self._commit_with_retry()
            self.db.refresh(contract)
            
            # 캐시 무효화
            await self._invalidate_contract_cache()
            
            logger.info(f"계약 생성 완료: {contract.id} - {contract.name}")
            return contract
            
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"계약 생성 실패: {e}")
            raise DatabaseException(f"계약 생성 중 오류 발생: {e}")
    
    async def get_contracts(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        search: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Contract], int]:
        """
        계약 목록을 조회합니다 - 캐싱 및 검색 최적화
        
        Args:
            skip: 건너뛸 레코드 수
            limit: 가져올 레코드 수
            search: 검색어
            status: 상태 필터
            
        Returns:
            Tuple[List[Contract], int]: 계약 목록과 전체 개수
        """
        try:
            # 캐시 키 생성
            cache_key = f"{self.cache_prefix}:list:{skip}:{limit}:{search}:{status}"
            
            # 캐시에서 조회 시도
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # 데이터베이스 쿼리 최적화 (삭제되지 않은 계약만)
            query = self.db.query(Contract).filter(Contract.is_deleted.is_(False))
            
            # 검색 조건 적용
            if search:
                search_filter = or_(
                    Contract.name.contains(search),
                    Contract.contract_number.contains(search),
                    Contract.client_name.contains(search)
                )
                query = query.filter(search_filter)
            
            # 상태 필터 적용
            if status:
                query = query.filter(Contract.status == status)
            
            # 전체 개수 조회 (캐시 활용)
            total_cache_key = f"{self.cache_prefix}:total:{search}:{status}"
            total = await self.cache.get_or_set(
                total_cache_key,
                lambda: query.count(),
                ttl=1800  # 30분
            )
            
            # 페이징 적용
            contracts = query.offset(skip).limit(limit).all()
            
            # 결과 캐싱
            result = (contracts, total)
            await self.cache.setex(cache_key, self.cache_ttl, json.dumps(result))
            
            return result
            
        except Exception as e:
            logger.error(f"계약 목록 조회 실패: {e}")
            raise DatabaseException(f"계약 목록 조회 중 오류 발생: {e}")
    
    async def get_contract_detail(self, contract_id: str) -> Optional[ContractDetailResponse]:
        """
        계약 상세 정보를 조회합니다 - 캐싱 및 관계 데이터 포함
        
        Args:
            contract_id: 계약 ID
            
        Returns:
            ContractDetailResponse: 계약 상세 정보 및 관련 문서
        """
        try:
            # 캐시에서 조회 시도
            cache_key = f"{self.cache_prefix}:detail:{contract_id}"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return ContractDetailResponse.parse_raw(cached_result)
            
            # 계약 정보 조회
            contract = await self.get_contract_by_id(contract_id)
            if not contract:
                return None
            
            # 관련 문서 조회
            documents = await self.get_contract_documents(contract_id)
            
            # 응답 구성
            response = ContractDetailResponse(
                status="success",
                data=contract,
                documents=documents,
                message=None
            )
            
            # 캐싱
            await self.cache.setex(cache_key, self.cache_ttl, response.json())
            
            return response
            
        except Exception as e:
            logger.error(f"계약 상세 조회 실패: {e}")
            raise DatabaseException(f"계약 상세 조회 중 오류 발생: {e}")
    
    async def get_contract_by_id(self, contract_id: str) -> Optional[Contract]:
        """
        계약 ID로 조회 - 캐싱 적용
        
        Args:
            contract_id: 계약 ID
            
        Returns:
            Contract: 계약 정보
        """
        try:
            # 캐시에서 조회 시도
            cache_key = f"{self.cache_prefix}:{contract_id}"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return Contract.parse_raw(cached_result)
            
            # 데이터베이스 조회 (삭제되지 않은 계약만)
            contract = self.db.query(Contract).filter(
                Contract.id == contract_id,
                Contract.is_deleted.is_(False)
            ).first()
            
            if contract:
                # 캐싱
                await self.cache.setex(cache_key, self.cache_ttl, contract.json())
            
            return contract
            
        except Exception as e:
            logger.error(f"계약 조회 실패: {e}")
            raise DatabaseException(f"계약 조회 중 오류 발생: {e}")
    
    async def update_contract(
        self, 
        contract_id: str, 
        contract_update: ContractUpdate
    ) -> Optional[Contract]:
        """
        계약 정보를 수정합니다 - 검증 및 캐싱 무효화
        
        Args:
            contract_id: 계약 ID
            contract_update: 수정할 계약 데이터
            
        Returns:
            Contract: 수정된 계약 정보
        """
        try:
            # 계약 존재 확인
            contract = await self.get_contract_by_id(contract_id)
            if not contract:
                return None
            
            # 계약번호 변경 시 중복 검사
            if contract_update.contract_number:
                existing_contract = await self._check_contract_number_exists(
                    contract_update.contract_number, 
                    exclude_id=contract_id
                )
                if existing_contract:
                    raise ValidationException("이미 존재하는 계약번호입니다.")
            
            # 업데이트할 데이터만 추출
            update_data = contract_update.dict(exclude_unset=True)
            
            # 계약 정보 업데이트
            for field, value in update_data.items():
                setattr(contract, field, value)
            
            await self._commit_with_retry()
            self.db.refresh(contract)
            
            # 캐시 무효화
            await self._invalidate_contract_cache(contract_id)
            
            logger.info(f"계약 수정 완료: {contract_id}")
            return contract
            
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"계약 수정 실패: {e}")
            raise DatabaseException(f"계약 수정 중 오류 발생: {e}")
    
    async def delete_contract(self, contract_id: str) -> bool:
        """
        계약을 삭제합니다 - 소프트 삭제 적용
        
        Args:
            contract_id: 계약 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            contract = await self.get_contract_by_id(contract_id)
            if not contract:
                return False
            
            # 소프트 삭제 (실제 삭제 대신 상태 변경)
            contract.status = "삭제됨"
            contract.deleted_at = datetime.utcnow()
            contract.is_deleted = True
            
            await self._commit_with_retry()
            
            # 캐시 무효화
            await self._invalidate_contract_cache(contract_id)
            
            logger.info(f"계약 삭제 완료: {contract_id}")
            return True
            
        except Exception as e:
            logger.error(f"계약 삭제 실패: {e}")
            raise DatabaseException(f"계약 삭제 중 오류 발생: {e}")
    
    async def create_contract_document(
        self, 
        contract_id: str, 
        document_data: ContractDocumentCreate
    ) -> ContractDocument:
        """
        계약 문서를 생성합니다
        
        Args:
            contract_id: 계약 ID
            document_data: 문서 생성 데이터
            
        Returns:
            ContractDocument: 생성된 문서 정보
        """
        try:
            # 계약 존재 확인
            contract = await self.get_contract_by_id(contract_id)
            if not contract:
                raise ContractNotFoundException("계약을 찾을 수 없습니다.")
            
            # 문서 생성
            document = ContractDocument(
                **document_data.dict(),
                contract_id=contract_id
            )
            self.db.add(document)
            await self._commit_with_retry()
            self.db.refresh(document)
            
            # 캐시 무효화
            await self._invalidate_contract_cache(contract_id)
            
            logger.info(f"계약 문서 생성 완료: {document.id}")
            return document
            
        except ContractNotFoundException:
            raise
        except Exception as e:
            logger.error(f"계약 문서 생성 실패: {e}")
            raise DatabaseException(f"계약 문서 생성 중 오류 발생: {e}")
    
    async def get_contract_documents(self, contract_id: str) -> List[ContractDocument]:
        """
        계약의 모든 문서를 조회합니다
        
        Args:
            contract_id: 계약 ID
            
        Returns:
            List[ContractDocument]: 문서 목록
        """
        try:
            # 캐시에서 조회 시도
            cache_key = f"{self.cache_prefix}:documents:{contract_id}"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return [ContractDocument.parse_raw(doc) for doc in json.loads(cached_result)]
            
            # 데이터베이스 조회
            documents = self.db.query(ContractDocument).filter(
                ContractDocument.contract_id == contract_id
            ).all()
            
            # 캐싱
            await self.cache.setex(cache_key, self.cache_ttl, json.dumps([doc.json() for doc in documents]))
            
            return documents
            
        except Exception as e:
            logger.error(f"계약 문서 조회 실패: {e}")
            raise DatabaseException(f"계약 문서 조회 중 오류 발생: {e}")
    
    # 성능 최적화를 위한 헬퍼 메서드들
    
    async def _check_contract_number_exists(
        self, 
        contract_number: str, 
        exclude_id: Optional[str] = None
    ) -> Optional[Contract]:
        """계약번호 중복 검사 - 캐싱 적용"""
        try:
            cache_key = f"{self.cache_prefix}:number:{contract_number}"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                contract = Contract.parse_raw(cached_result)
                if exclude_id and contract.id == exclude_id:
                    return None
                return contract
            
            query = self.db.query(Contract).filter(
                Contract.contract_number == contract_number,
                Contract.is_deleted.is_(False)
            )
            if exclude_id:
                query = query.filter(Contract.id != exclude_id)
            
            contract = query.first()
            
            if contract:
                await self.cache.setex(cache_key, self.cache_ttl, contract.json())
            
            return contract
            
        except Exception as e:
            logger.error(f"계약번호 중복 검사 실패: {e}")
            return None
    
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
    
    async def _invalidate_contract_cache(self, contract_id: Optional[str] = None):
        """계약 관련 캐시 무효화"""
        try:
            if contract_id:
                # 특정 계약 캐시 무효화
                patterns = [
                    f"{self.cache_prefix}:{contract_id}",
                    f"{self.cache_prefix}:detail:{contract_id}",
                    f"{self.cache_prefix}:documents:{contract_id}"
                ]
            else:
                # 모든 계약 캐시 무효화
                patterns = [f"{self.cache_prefix}:*"]
            
            for pattern in patterns:
                await self.cache.delete_pattern(pattern)
                
        except Exception as e:
            logger.warning(f"캐시 무효화 실패: {e}")
    
    @lru_cache(maxsize=1000)
    def _get_contract_status_options(self) -> List[str]:
        """계약 상태 옵션 조회 - 캐시된 함수"""
        return ["진행중", "완료", "중단", "취소", "삭제됨"]
    
    async def get_contract_statistics(self) -> Dict[str, Any]:
        """계약 통계 정보 조회 - 대시보드용"""
        try:
            cache_key = f"{self.cache_prefix}:statistics"
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # 통계 쿼리 최적화 (삭제되지 않은 계약만)
            stats = self.db.query(
                Contract.status,
                func.count(Contract.id).label('count'),
                func.sum(Contract.contract_amount).label('total_amount')
            ).filter(Contract.is_deleted.is_(False)).group_by(Contract.status).all()
            
            result = {
                "total_contracts": sum(s.count for s in stats),
                "total_amount": sum(s.total_amount or 0 for s in stats),
                "by_status": {s.status: {"count": s.count, "amount": s.total_amount or 0} for s in stats}
            }
            
            # 캐싱 (짧은 TTL)
            await self.cache.setex(cache_key, 1800, json.dumps(result))
            
            return result
            
        except Exception as e:
            logger.error(f"계약 통계 조회 실패: {e}")
            return {"total_contracts": 0, "total_amount": 0, "by_status": {}}

# 기존 함수도 유지 (호환성)
def create_contract(db: Session, contract: ContractCreate) -> Contract:
    return ContractService(db).create_contract(contract)
def get_contracts(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Contract]:
    return ContractService(db).get_contracts(skip, limit, status)
def get_contract(db: Session, contract_id: int) -> Optional[Contract]:
    return ContractService(db).get_contract(contract_id)
def update_contract(db: Session, contract_id: int, contract: ContractUpdate) -> Optional[Contract]:
    return ContractService(db).update_contract(contract_id, contract)
def delete_contract(db: Session, contract_id: int) -> bool:
    return ContractService(db).delete_contract(contract_id)
def create_contract_document(db: Session, contract_id: int, document: ContractDocumentCreate) -> ContractDocument:
    return ContractService(db).create_contract_document(contract_id, document)
def get_contract_documents(db: Session, contract_id: int) -> List[ContractDocument]:
    return ContractService(db).get_contract_documents(contract_id) 