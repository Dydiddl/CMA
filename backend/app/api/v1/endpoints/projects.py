#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
프로젝트 관리 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse,
    ProjectDocumentCreate, ProjectDocumentUpdate, ProjectDocumentResponse, 
    ProjectDocumentListResponse, ProjectStatistics, ProjectStatus, ProjectType
)
from app.services.project import ProjectService
from app.models.user import User
from app.api.deps import get_db, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 생성"""
    try:
        project_service = ProjectService(db)
        result = project_service.create_project(project)
        return ProjectResponse.from_orm(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"프로젝트 생성 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 생성 중 오류가 발생했습니다.")

@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 레코드 수"),
    search: Optional[str] = Query(None, description="검색어"),
    status: Optional[ProjectStatus] = Query(None, description="프로젝트 상태"),
    project_type: Optional[ProjectType] = Query(None, description="프로젝트 유형"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 목록 조회"""
    try:
        project_service = ProjectService(db)
        projects, total = project_service.get_projects(
            skip=skip, limit=limit, search=search, status=status, project_type=project_type
        )
        
        project_responses = []
        for project in projects:
            # 진행률 및 예산 사용률 계산
            progress_percentage = project.calculate_progress()
            budget_usage_percentage = project.calculate_budget_usage()
            
            project_dict = {
                **project.__dict__,
                'progress_percentage': progress_percentage,
                'budget_usage_percentage': budget_usage_percentage
            }
            project_responses.append(ProjectResponse.from_orm(project))
        
        return ProjectListResponse(
            data=project_responses,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
    except Exception as e:
        logger.error(f"프로젝트 목록 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 목록 조회 중 오류가 발생했습니다.")

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 상세 조회"""
    try:
        project_service = ProjectService(db)
        project = project_service.get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")
        
        # 진행률 및 예산 사용률 계산
        progress_percentage = project.calculate_progress()
        budget_usage_percentage = project.calculate_budget_usage()
        
        project_dict = {
            **project.__dict__,
            'progress_percentage': progress_percentage,
            'budget_usage_percentage': budget_usage_percentage
        }
        
        return ProjectResponse.from_orm(project)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"프로젝트 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 조회 중 오류가 발생했습니다.")

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 수정"""
    try:
        project_service = ProjectService(db)
        project = project_service.update_project(project_id, project_update)
        if not project:
            raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")
        
        # 진행률 및 예산 사용률 계산
        progress_percentage = project.calculate_progress()
        budget_usage_percentage = project.calculate_budget_usage()
        
        project_dict = {
            **project.__dict__,
            'progress_percentage': progress_percentage,
            'budget_usage_percentage': budget_usage_percentage
        }
        
        return ProjectResponse.from_orm(project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"프로젝트 수정 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 수정 중 오류가 발생했습니다.")

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 삭제"""
    try:
        project_service = ProjectService(db)
        success = project_service.delete_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")
        return {"status": "success", "message": "프로젝트가 성공적으로 삭제되었습니다."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"프로젝트 삭제 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 삭제 중 오류가 발생했습니다.")

@router.get("/statistics/overview", response_model=ProjectStatistics)
async def get_project_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 통계 조회"""
    try:
        project_service = ProjectService(db)
        statistics = project_service.get_project_statistics()
        return ProjectStatistics(**statistics)
    except Exception as e:
        logger.error(f"프로젝트 통계 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 통계 조회 중 오류가 발생했습니다.")

# 프로젝트 문서 관련 엔드포인트

@router.post("/{project_id}/documents", response_model=ProjectDocumentResponse, status_code=201)
async def create_project_document(
    project_id: str,
    document: ProjectDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 문서 생성"""
    try:
        document.project_id = project_id
        project_service = ProjectService(db)
        result = project_service.create_project_document(document)
        return ProjectDocumentResponse.from_orm(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"프로젝트 문서 생성 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 문서 생성 중 오류가 발생했습니다.")

@router.get("/{project_id}/documents", response_model=ProjectDocumentListResponse)
async def get_project_documents(
    project_id: str,
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 레코드 수"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 문서 목록 조회"""
    try:
        project_service = ProjectService(db)
        documents, total = project_service.get_project_documents(project_id, skip=skip, limit=limit)
        
        document_responses = [ProjectDocumentResponse.from_orm(doc) for doc in documents]
        
        return ProjectDocumentListResponse(
            data=document_responses,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
    except Exception as e:
        logger.error(f"프로젝트 문서 목록 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 문서 목록 조회 중 오류가 발생했습니다.")

@router.get("/documents/{document_id}", response_model=ProjectDocumentResponse)
async def get_project_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 문서 상세 조회"""
    try:
        project_service = ProjectService(db)
        document = project_service.get_project_document_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="프로젝트 문서를 찾을 수 없습니다.")
        return ProjectDocumentResponse.from_orm(document)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"프로젝트 문서 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 문서 조회 중 오류가 발생했습니다.")

@router.put("/documents/{document_id}", response_model=ProjectDocumentResponse)
async def update_project_document(
    document_id: str,
    document_update: ProjectDocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 문서 수정"""
    try:
        project_service = ProjectService(db)
        document = project_service.update_project_document(document_id, document_update)
        if not document:
            raise HTTPException(status_code=404, detail="프로젝트 문서를 찾을 수 없습니다.")
        return ProjectDocumentResponse.from_orm(document)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"프로젝트 문서 수정 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 문서 수정 중 오류가 발생했습니다.")

@router.delete("/documents/{document_id}")
async def delete_project_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """프로젝트 문서 삭제"""
    try:
        project_service = ProjectService(db)
        success = project_service.delete_project_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="프로젝트 문서를 찾을 수 없습니다.")
        return {"status": "success", "message": "프로젝트 문서가 성공적으로 삭제되었습니다."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"프로젝트 문서 삭제 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="프로젝트 문서 삭제 중 오류가 발생했습니다.")
