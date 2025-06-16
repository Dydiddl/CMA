from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class WorkItemResponse(BaseModel):
    """공사 항목 응답 스키마"""
    code: str = Field(..., description="공사 항목 코드")
    name: str = Field(..., description="공사 항목명")
    unit: str = Field(..., description="단위")
    quantity: float = Field(..., description="수량")
    unit_price: float = Field(..., description="단가")
    amount: float = Field(..., description="금액")
    remarks: Optional[str] = Field(None, description="비고")

class EstimateGenerateRequest(BaseModel):
    """내역서 생성 요청 스키마"""
    work_items: List[WorkItemResponse] = Field(..., description="공사 항목 목록")
    year: int = Field(..., description="적용할 연도")
    output_path: str = Field(..., description="출력 파일 경로")
    template_path: Optional[str] = Field(None, description="템플릿 파일 경로")

class EstimateUpdateRequest(BaseModel):
    """변경사항 추가 요청 스키마"""
    year: int = Field(..., description="변경 연도")
    updates: Dict[str, Any] = Field(..., description="변경사항 데이터")

class EstimateResponse(BaseModel):
    """일반 응답 스키마"""
    success: bool = Field(..., description="성공 여부")
    message: Optional[str] = Field(None, description="응답 메시지")
    data: Optional[Any] = Field(None, description="응답 데이터")
    file_path: Optional[str] = Field(None, description="생성된 파일 경로")
    created_at: Optional[datetime] = Field(None, description="생성 일시") 