"""
계약 관련 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db, get_current_user
from app.schemas.contract import (
    ContractCreate, 
    ContractUpdate, 
    ContractResponse, 
    ContractListResponse,
    ContractDetailResponse,
    StandardResponse
)
from app.services.contract import ContractService
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    새로운 계약을 생성합니다.
    
    Args:
        contract: 계약 생성 데이터
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        ContractResponse: 생성된 계약 정보
        
    Raises:
        HTTPException: 400 - 유효하지 않은 데이터
        HTTPException: 500 - 서버 오류
    """
    try:
        contract_service = ContractService(db)
        result = contract_service.create_contract(contract, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="계약 생성 중 오류가 발생했습니다."
        )


@router.get("/", response_model=ContractListResponse)
async def get_contracts(
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 레코드 수"),
    search: Optional[str] = Query(None, description="검색어"),
    status_filter: Optional[str] = Query(None, alias="status", description="상태 필터"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    계약 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 레코드 수
        limit: 가져올 레코드 수
        search: 검색어
        status_filter: 상태 필터
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        ContractListResponse: 계약 목록 및 페이징 정보
    """
    try:
        contract_service = ContractService(db)
        contracts, total = contract_service.get_contracts(
            skip=skip, limit=limit, search=search, status=status_filter
        )
        return ContractListResponse(
            data=contracts,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="계약 목록 조회 중 오류가 발생했습니다."
        )


@router.get("/{contract_id}", response_model=ContractDetailResponse)
async def get_contract(
    contract_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    특정 계약의 상세 정보를 조회합니다.
    
    Args:
        contract_id: 계약 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        ContractDetailResponse: 계약 상세 정보 및 관련 문서
        
    Raises:
        HTTPException: 404 - 계약을 찾을 수 없음
    """
    try:
        contract_service = ContractService(db)
        contract_detail = contract_service.get_contract_detail(contract_id)
        if not contract_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="계약을 찾을 수 없습니다."
            )
        return contract_detail
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="계약 조회 중 오류가 발생했습니다."
        )


@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: str,
    contract_update: ContractUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    계약 정보를 수정합니다.
    
    Args:
        contract_id: 계약 ID
        contract_update: 수정할 계약 데이터
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        ContractResponse: 수정된 계약 정보
        
    Raises:
        HTTPException: 400 - 유효하지 않은 데이터
        HTTPException: 404 - 계약을 찾을 수 없음
    """
    try:
        contract_service = ContractService(db)
        contract = contract_service.update_contract(contract_id, contract_update)
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="계약을 찾을 수 없습니다."
            )
        return contract
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="계약 수정 중 오류가 발생했습니다."
        )


@router.delete("/{contract_id}", response_model=StandardResponse)
async def delete_contract(
    contract_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    계약을 삭제합니다.
    
    Args:
        contract_id: 계약 ID
        db: 데이터베이스 세션
        current_user: 현재 사용자
        
    Returns:
        StandardResponse: 삭제 결과
        
    Raises:
        HTTPException: 404 - 계약을 찾을 수 없음
    """
    try:
        contract_service = ContractService(db)
        success = contract_service.delete_contract(contract_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="계약을 찾을 수 없습니다."
            )
        return StandardResponse(
            status="success",
            message="계약이 성공적으로 삭제되었습니다."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="계약 삭제 중 오류가 발생했습니다."
        ) 