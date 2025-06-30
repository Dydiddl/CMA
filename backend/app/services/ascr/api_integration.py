#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR CMA 시스템 통합 API
고도화된 ASCR 모듈을 CMA 시스템과 통합
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
import aiofiles

# ASCR 모듈 임포트
from .async_processor import AsyncASCRProcessor
from .memory_optimizer import OptimizedASCRProcessor
from .advanced_logger import AdvancedLogger

logger = logging.getLogger(__name__)

# API 라우터 생성
router = APIRouter(prefix="/api/v1/ascr", tags=["ASCR"])

# Pydantic 모델
class ASCRProcessingRequest(BaseModel):
    """ASCR 처리 요청 모델"""
    file_path: str
    output_dir: str
    processing_type: str = "standard"  # standard, optimized, ml_enhanced
    options: Dict[str, Any] = {}

class ASCRProcessingResponse(BaseModel):
    """ASCR 처리 응답 모델"""
    task_id: str
    status: str
    message: str
    created_at: datetime

class ASCRStatusResponse(BaseModel):
    """ASCR 상태 응답 모델"""
    task_id: str
    status: str
    progress: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ASCRBatchRequest(BaseModel):
    """ASCR 배치 처리 요청 모델"""
    files: List[str]
    output_dir: str
    processing_type: str = "standard"
    options: Dict[str, Any] = {}

# 전역 변수
processing_tasks: Dict[str, Dict[str, Any]] = {}
task_counter = 0

class ASCRService:
    """ASCR 서비스 클래스"""
    
    def __init__(self):
        self.async_processor = AsyncASCRProcessor()
        self.optimized_processor = OptimizedASCRProcessor()
        self.logger = AdvancedLogger("ASCR_Service")
    
    async def process_pdf_standard(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """표준 PDF 처리"""
        with self.logger.operation_context("표준_PDF_처리", str(pdf_path)) as context:
            try:
                result = await self.async_processor.process_pdf_async(pdf_path, output_dir)
                return result
            except Exception as e:
                self.logger.log_error_with_context(e, "표준_PDF_처리", {"file_path": str(pdf_path)})
                raise
    
    def process_pdf_optimized(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """최적화된 PDF 처리"""
        with self.logger.operation_context("최적화_PDF_처리", str(pdf_path)) as context:
            try:
                result = self.optimized_processor.process_pdf_optimized(pdf_path, output_dir)
                return result
            except Exception as e:
                self.logger.log_error_with_context(e, "최적화_PDF_처리", {"file_path": str(pdf_path)})
                raise
    
    async def process_pdf_ml_enhanced(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """ML 강화 PDF 처리"""
        with self.logger.operation_context("ML_강화_PDF_처리", str(pdf_path)) as context:
            try:
                # 기본 처리
                basic_result = await self.async_processor.process_pdf_async(pdf_path, output_dir)
                
                # ML 분석 추가 (향후 구현)
                ml_analysis = {
                    "ml_enhanced": True,
                    "confidence_score": 0.95,
                    "suggested_improvements": []
                }
                
                basic_result["ml_analysis"] = ml_analysis
                return basic_result
                
            except Exception as e:
                self.logger.log_error_with_context(e, "ML_강화_PDF_처리", {"file_path": str(pdf_path)})
                raise

# ASCR 서비스 인스턴스
ascr_service = ASCRService()

def generate_task_id() -> str:
    """작업 ID 생성"""
    global task_counter
    task_counter += 1
    return f"ascr_task_{task_counter}_{int(datetime.now().timestamp())}"

async def process_pdf_background(task_id: str, pdf_path: str, output_dir: str, processing_type: str):
    """백그라운드 PDF 처리"""
    try:
        # 작업 상태 업데이트
        processing_tasks[task_id]["status"] = "processing"
        processing_tasks[task_id]["progress"] = 0.1
        
        pdf_path_obj = Path(pdf_path)
        output_dir_obj = Path(output_dir)
        
        # 출력 디렉토리 생성
        output_dir_obj.mkdir(parents=True, exist_ok=True)
        
        # 처리 타입에 따른 실행
        if processing_type == "standard":
            result = await ascr_service.process_pdf_standard(pdf_path_obj, output_dir_obj)
        elif processing_type == "optimized":
            result = ascr_service.process_pdf_optimized(pdf_path_obj, output_dir_obj)
        elif processing_type == "ml_enhanced":
            result = await ascr_service.process_pdf_ml_enhanced(pdf_path_obj, output_dir_obj)
        else:
            raise ValueError(f"지원하지 않는 처리 타입: {processing_type}")
        
        # 작업 완료 상태 업데이트
        processing_tasks[task_id]["status"] = "completed"
        processing_tasks[task_id]["progress"] = 1.0
        processing_tasks[task_id]["result"] = result
        processing_tasks[task_id]["updated_at"] = datetime.now()
        
        logger.info(f"작업 완료: {task_id}")
        
    except Exception as e:
        # 오류 상태 업데이트
        processing_tasks[task_id]["status"] = "error"
        processing_tasks[task_id]["error"] = str(e)
        processing_tasks[task_id]["updated_at"] = datetime.now()
        
        logger.error(f"작업 실패: {task_id} - {e}")

@router.post("/process", response_model=ASCRProcessingResponse)
async def process_pdf(request: ASCRProcessingRequest, background_tasks: BackgroundTasks):
    """PDF 처리 API 엔드포인트"""
    try:
        # 작업 ID 생성
        task_id = generate_task_id()
        
        # 작업 정보 저장
        processing_tasks[task_id] = {
            "status": "pending",
            "progress": 0.0,
            "file_path": request.file_path,
            "output_dir": request.output_dir,
            "processing_type": request.processing_type,
            "options": request.options,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # 백그라운드 작업 시작
        background_tasks.add_task(
            process_pdf_background,
            task_id,
            request.file_path,
            request.output_dir,
            request.processing_type
        )
        
        return ASCRProcessingResponse(
            task_id=task_id,
            status="pending",
            message="PDF 처리 작업이 시작되었습니다.",
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"PDF 처리 요청 실패: {e}")
        raise HTTPException(status_code=500, detail=f"PDF 처리 요청 실패: {e}")

@router.get("/status/{task_id}", response_model=ASCRStatusResponse)
async def get_processing_status(task_id: str):
    """처리 상태 조회 API 엔드포인트"""
    if task_id not in processing_tasks:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")
    
    task = processing_tasks[task_id]
    
    return ASCRStatusResponse(
        task_id=task_id,
        status=task["status"],
        progress=task["progress"],
        result=task.get("result"),
        error=task.get("error"),
        created_at=task["created_at"],
        updated_at=task["updated_at"]
    )

@router.post("/batch", response_model=ASCRProcessingResponse)
async def process_pdf_batch(request: ASCRBatchRequest, background_tasks: BackgroundTasks):
    """배치 PDF 처리 API 엔드포인트"""
    try:
        # 작업 ID 생성
        task_id = generate_task_id()
        
        # 작업 정보 저장
        processing_tasks[task_id] = {
            "status": "pending",
            "progress": 0.0,
            "files": request.files,
            "output_dir": request.output_dir,
            "processing_type": request.processing_type,
            "options": request.options,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # 배치 처리 백그라운드 작업
        async def batch_process():
            try:
                total_files = len(request.files)
                results = []
                
                for i, file_path in enumerate(request.files):
                    # 진행률 업데이트
                    progress = (i / total_files) * 0.9  # 90%까지
                    processing_tasks[task_id]["progress"] = progress
                    processing_tasks[task_id]["updated_at"] = datetime.now()
                    
                    # 개별 파일 처리
                    pdf_path_obj = Path(file_path)
                    output_dir_obj = Path(request.output_dir)
                    
                    if request.processing_type == "standard":
                        result = await ascr_service.process_pdf_standard(pdf_path_obj, output_dir_obj)
                    elif request.processing_type == "optimized":
                        result = ascr_service.process_pdf_optimized(pdf_path_obj, output_dir_obj)
                    elif request.processing_type == "ml_enhanced":
                        result = await ascr_service.process_pdf_ml_enhanced(pdf_path_obj, output_dir_obj)
                    
                    results.append({
                        "file_path": file_path,
                        "result": result
                    })
                
                # 배치 처리 완료
                processing_tasks[task_id]["status"] = "completed"
                processing_tasks[task_id]["progress"] = 1.0
                processing_tasks[task_id]["result"] = {
                    "batch_results": results,
                    "total_files": total_files,
                    "successful_files": len([r for r in results if r["result"].get("status") == "success"])
                }
                processing_tasks[task_id]["updated_at"] = datetime.now()
                
            except Exception as e:
                processing_tasks[task_id]["status"] = "error"
                processing_tasks[task_id]["error"] = str(e)
                processing_tasks[task_id]["updated_at"] = datetime.now()
        
        # 백그라운드 작업 시작
        background_tasks.add_task(batch_process)
        
        return ASCRProcessingResponse(
            task_id=task_id,
            status="pending",
            message=f"배치 PDF 처리 작업이 시작되었습니다. (파일 수: {len(request.files)})",
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"배치 PDF 처리 요청 실패: {e}")
        raise HTTPException(status_code=500, detail=f"배치 PDF 처리 요청 실패: {e}")

@router.get("/tasks", response_model=List[ASCRStatusResponse])
async def list_processing_tasks():
    """처리 작업 목록 조회 API 엔드포인트"""
    tasks = []
    for task_id, task in processing_tasks.items():
        tasks.append(ASCRStatusResponse(
            task_id=task_id,
            status=task["status"],
            progress=task["progress"],
            result=task.get("result"),
            error=task.get("error"),
            created_at=task["created_at"],
            updated_at=task["updated_at"]
        ))
    
    return tasks

@router.delete("/tasks/{task_id}")
async def cancel_processing_task(task_id: str):
    """처리 작업 취소 API 엔드포인트"""
    if task_id not in processing_tasks:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")
    
    task = processing_tasks[task_id]
    if task["status"] in ["completed", "error"]:
        raise HTTPException(status_code=400, detail="이미 완료된 작업입니다.")
    
    # 작업 취소
    task["status"] = "cancelled"
    task["updated_at"] = datetime.now()
    
    return {"message": "작업이 취소되었습니다."}

@router.get("/performance-report")
async def get_performance_report():
    """성능 보고서 조회 API 엔드포인트"""
    try:
        report = ascr_service.logger.get_performance_report()
        return report
    except Exception as e:
        logger.error(f"성능 보고서 생성 실패: {e}")
        raise HTTPException(status_code=500, detail=f"성능 보고서 생성 실패: {e}")

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """PDF 파일 업로드 API 엔드포인트"""
    try:
        # 업로드 디렉토리 생성
        upload_dir = Path("uploads/ascr")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # 파일 저장
        file_path = upload_dir / file.filename
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return {
            "message": "파일 업로드 성공",
            "file_path": str(file_path),
            "file_size": len(content)
        }
        
    except Exception as e:
        logger.error(f"파일 업로드 실패: {e}")
        raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {e}")

# 헬스체크 엔드포인트
@router.get("/health")
async def health_check():
    """ASCR 모듈 헬스체크"""
    return {
        "status": "healthy",
        "module": "ASCR",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

# 통계 엔드포인트
@router.get("/stats")
async def get_processing_stats():
    """처리 통계 조회"""
    total_tasks = len(processing_tasks)
    completed_tasks = len([t for t in processing_tasks.values() if t["status"] == "completed"])
    error_tasks = len([t for t in processing_tasks.values() if t["status"] == "error"])
    pending_tasks = len([t for t in processing_tasks.values() if t["status"] == "pending"])
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "error_tasks": error_tasks,
        "pending_tasks": pending_tasks,
        "success_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    } 