from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from app.services.excel.processor import ExcelProcessor
from app.services.excel.validator import ExcelValidator
from app.schemas.excel import ExcelResponse, ExcelValidationResponse

router = APIRouter()

@router.post("/upload", response_model=ExcelResponse)
async def upload_excel(
    file: UploadFile = File(...),
    processor: ExcelProcessor = Depends(),
    validator: ExcelValidator = Depends()
):
    """
    Excel 파일을 업로드하고 처리합니다.
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .xlsx and .xls files are allowed.")
    
    # 파일 검증
    validation_result = await validator.validate(file)
    if not validation_result.is_valid:
        raise HTTPException(status_code=400, detail=validation_result.errors)
    
    # 파일 처리
    result = await processor.process(file)
    return result

@router.post("/generate", response_model=ExcelResponse)
async def generate_excel(
    data: dict,
    processor: ExcelProcessor = Depends()
):
    """
    데이터를 기반으로 Excel 파일을 생성합니다.
    """
    try:
        result = await processor.generate(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate", response_model=ExcelValidationResponse)
async def validate_excel(
    file: UploadFile = File(...),
    validator: ExcelValidator = Depends()
):
    """
    Excel 파일의 유효성을 검사합니다.
    """
    result = await validator.validate(file)
    return result
