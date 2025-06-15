from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from datetime import datetime

from app.api import deps
from app.core.permissions import check_permissions
from app.core.config import settings
from app.models.user import User
from app.schemas.file import FileCreate, FileResponse, FileList
from app.crud import file as file_crud
from app.services.file_service import FileService

router = APIRouter()
file_service = FileService()

@router.post("/upload", response_model=FileResponse)
async def upload_file(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user)
) -> FileResponse:
    """
    파일을 업로드합니다.
    """
    if not check_permissions(current_user, ["create:file"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="파일 업로드 권한이 없습니다"
        )
    
    # 파일 형식 검증
    if not file_service.validate_file_type(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="지원하지 않는 파일 형식입니다"
        )
    
    # 파일 크기 검증
    if not file_service.validate_file_size(file.size):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="파일 크기가 제한을 초과했습니다"
        )
    
    # 파일 저장
    file_path = await file_service.save_file(file)
    
    # 파일 정보 저장
    file_in = FileCreate(
        filename=file.filename,
        file_path=file_path,
        file_size=file.size,
        file_type=file.content_type,
        uploaded_by=current_user.id
    )
    
    file_record = file_crud.create_file(db=db, file=file_in)
    return file_record

@router.get("/files", response_model=FileList)
def list_files(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> FileList:
    """
    파일 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:file"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="파일 조회 권한이 없습니다"
        )
    
    files = file_crud.get_files(
        db=db,
        skip=skip,
        limit=limit,
        user_id=current_user.id
    )
    total = file_crud.get_files_count(db=db, user_id=current_user.id)
    
    return FileList(
        items=files,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/files/{file_id}", response_model=FileResponse)
def get_file(
    *,
    db: Session = Depends(deps.get_db),
    file_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> FileResponse:
    """
    특정 파일의 정보를 조회합니다.
    """
    if not check_permissions(current_user, ["read:file"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="파일 조회 권한이 없습니다"
        )
    
    file = file_crud.get_file(db=db, file_id=file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="파일을 찾을 수 없습니다"
        )
    
    return file

@router.get("/files/{file_id}/download")
async def download_file(
    *,
    db: Session = Depends(deps.get_db),
    file_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    파일을 다운로드합니다.
    """
    if not check_permissions(current_user, ["read:file"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="파일 다운로드 권한이 없습니다"
        )
    
    file = file_crud.get_file(db=db, file_id=file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="파일을 찾을 수 없습니다"
        )
    
    if not os.path.exists(file.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="파일이 서버에 존재하지 않습니다"
        )
    
    return FileResponse(
        path=file.file_path,
        filename=file.filename,
        media_type=file.file_type
    )

@router.delete("/files/{file_id}")
def delete_file(
    *,
    db: Session = Depends(deps.get_db),
    file_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    파일을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:file"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="파일 삭제 권한이 없습니다"
        )
    
    file = file_crud.get_file(db=db, file_id=file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="파일을 찾을 수 없습니다"
        )
    
    # 파일 시스템에서 삭제
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    # 데이터베이스에서 삭제
    file_crud.delete_file(db=db, file_id=file_id)
    
    return {"message": "파일이 삭제되었습니다"} 