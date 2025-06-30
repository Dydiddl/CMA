"""
ASCR API Endpoints

PDF 처리 및 검증을 위한 API 엔드포인트들입니다.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging

from ....services.ascr import ASCRProcessor
from ....core.auth import get_current_user
from ....models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/extract-toc")
async def extract_toc(
    file: UploadFile = File(...),
    year: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """
    PDF에서 목차 구조를 추출합니다.
    """
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")
        
        processor = ASCRProcessor()
        result = await processor.extract_toc(file.file, year)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "목차 추출이 완료되었습니다.",
                "data": result
            }
        )
    except Exception as e:
        logger.error(f"목차 추출 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"목차 추출 실패: {str(e)}")

@router.post("/extract-text")
async def extract_text(
    file: UploadFile = File(...),
    pages: Optional[List[int]] = None,
    current_user: User = Depends(get_current_user)
):
    """
    PDF에서 텍스트를 추출합니다.
    """
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")
        
        processor = ASCRProcessor()
        result = await processor.extract_text(file.file, pages)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "텍스트 추출이 완료되었습니다.",
                "data": result
            }
        )
    except Exception as e:
        logger.error(f"텍스트 추출 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"텍스트 추출 실패: {str(e)}")

@router.post("/split-pdf")
async def split_pdf(
    file: UploadFile = File(...),
    toc_structure: dict = None,
    current_user: User = Depends(get_current_user)
):
    """
    PDF를 목차 구조에 따라 분할합니다.
    """
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")
        
        processor = ASCRProcessor()
        result = await processor.split_pdf(file.file, toc_structure)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "PDF 분할이 완료되었습니다.",
                "data": result
            }
        )
    except Exception as e:
        logger.error(f"PDF 분할 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF 분할 실패: {str(e)}")

@router.post("/download-standard-price")
async def download_standard_price(
    year: int,
    force_update: bool = False,
    current_user: User = Depends(get_current_user)
):
    """
    표준 가격 목록을 다운로드합니다.
    """
    try:
        processor = ASCRProcessor()
        result = await processor.download_standard_price(year, force_update)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"{year}년 표준 가격 목록 다운로드가 완료되었습니다.",
                "data": result
            }
        )
    except Exception as e:
        logger.error(f"표준 가격 목록 다운로드 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"다운로드 실패: {str(e)}")

@router.post("/validate-price-list")
async def validate_price_list(
    year: int,
    current_user: User = Depends(get_current_user)
):
    """
    표준 가격 목록을 검증합니다.
    """
    try:
        processor = ASCRProcessor()
        result = await processor.validate_price_list(year)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"{year}년 표준 가격 목록 검증이 완료되었습니다.",
                "data": result
            }
        )
    except Exception as e:
        logger.error(f"표준 가격 목록 검증 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"검증 실패: {str(e)}")

@router.post("/analyze-ground-truth")
async def analyze_ground_truth(
    data_file: UploadFile = File(...),
    analysis_type: str = "comprehensive",
    current_user: User = Depends(get_current_user)
):
    """
    지반 진실 데이터를 분석합니다.
    """
    try:
        processor = ASCRProcessor()
        result = await processor.analyze_ground_truth(data_file.file, analysis_type)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "지반 진실 데이터 분석이 완료되었습니다.",
                "data": result
            }
        )
    except Exception as e:
        logger.error(f"지반 진실 데이터 분석 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")

@router.post("/fix-hierarchy")
async def fix_hierarchy(
    structure_file: UploadFile = File(...),
    fix_type: str = "dots_to_commas",
    current_user: User = Depends(get_current_user)
):
    """
    계층 구조를 수정합니다.
    """
    try:
        processor = ASCRProcessor()
        result = await processor.fix_hierarchy(structure_file.file, fix_type)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "계층 구조 수정이 완료되었습니다.",
                "data": result
            }
        )
    except Exception as e:
        logger.error(f"계층 구조 수정 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"수정 실패: {str(e)}")

@router.get("/status")
async def get_ascr_status(current_user: User = Depends(get_current_user)):
    """
    ASCR 모듈의 상태를 확인합니다.
    """
    try:
        processor = ASCRProcessor()
        status = await processor.get_status()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": status
            }
        )
    except Exception as e:
        logger.error(f"ASCR 상태 확인 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"상태 확인 실패: {str(e)}") 