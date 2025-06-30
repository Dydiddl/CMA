from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from typing import List, Optional
from app.services.estimator import EstimatorParser, EstimatorGenerator, EstimatorUpdater
from app.schemas.estimator import (
    EstimateResponse,
    EstimateGenerateRequest,
    EstimateUpdateRequest,
    WorkItemResponse
)
from pathlib import Path
import tempfile
import os

router = APIRouter()

@router.post("/upload", response_model=List[WorkItemResponse])
async def upload_estimate(
    file: UploadFile = File(...),
    parser: EstimatorParser = Depends()
):
    """
    품셈 파일을 업로드하고 파싱합니다.
    """
    if not file.filename.endswith(('.hwp', '.pdf')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. HWP 또는 PDF 파일만 업로드 가능합니다."
        )
    
    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # 파일 파싱
        parsed_data = parser.parse_file(temp_path)
        
        # 공사 항목 추출
        work_items = parser.extract_work_items(parsed_data)
        
        # 데이터 검증
        if not parser.validate_data(parsed_data):
            raise HTTPException(
                status_code=400,
                detail="파싱된 데이터가 유효하지 않습니다."
            )
        
        return work_items
    
    finally:
        # 임시 파일 삭제
        os.unlink(temp_path)

@router.post("/generate", response_model=EstimateResponse)
async def generate_estimate(
    request: EstimateGenerateRequest,
    generator: EstimatorGenerator = Depends(),
    updater: EstimatorUpdater = Depends()
):
    """
    공사내역서를 생성합니다.
    """
    try:
        # 연도별 변경사항 적용
        updated_items = updater.apply_updates(
            request.work_items,
            request.year
        )
        
        # 내역서 생성
        output_path = generator.generate_estimate(
            work_items=updated_items,
            output_path=request.output_path,
            template_path=request.template_path
        )
        
        return {
            "success": True,
            "file_path": output_path,
            "message": "공사내역서가 성공적으로 생성되었습니다."
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"내역서 생성 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/updates", response_model=EstimateResponse)
async def add_estimate_update(
    request: EstimateUpdateRequest,
    updater: EstimatorUpdater = Depends()
):
    """
    연도별 변경사항을 추가합니다.
    """
    try:
        updater.add_update(
            year=request.year,
            updates=request.updates
        )
        
        return {
            "success": True,
            "message": f"{request.year}년도 변경사항이 추가되었습니다."
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"변경사항 추가 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/updates/{year}", response_model=EstimateResponse)
async def get_estimate_updates(
    year: int,
    updater: EstimatorUpdater = Depends()
):
    """
    특정 연도의 변경사항을 조회합니다.
    """
    updates = updater.get_updates(year)
    if not updates:
        raise HTTPException(
            status_code=404,
            detail=f"{year}년도의 변경사항을 찾을 수 없습니다."
        )
    
    return {
        "success": True,
        "data": updates
    }

@router.get("/templates", response_model=EstimateResponse)
async def list_templates(
    generator: EstimatorGenerator = Depends()
):
    """
    사용 가능한 템플릿 목록을 조회합니다.
    """
    template_dir = Path(generator.template_dir)
    templates = [
        f.name for f in template_dir.glob("*.xlsx")
        if f.is_file() and not f.name.startswith(".")
    ]
    
    return {
        "success": True,
        "data": templates
    } 