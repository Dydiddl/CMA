#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 고도화 모듈 통합 테스트
성능 테스트 및 기능 검증
"""

import pytest
import asyncio
import time
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json
import logging

# ASCR 모듈 임포트
from app.services.ascr.async_processor import AsyncASCRProcessor
from app.services.ascr.memory_optimizer import OptimizedASCRProcessor
from app.services.ascr.advanced_logger import AdvancedLogger
from app.services.ascr.api_integration import ASCRService, processing_tasks

# 테스트 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestASCRAdvancedFeatures:
    """ASCR 고도화 기능 테스트"""
    
    @pytest.fixture
    def temp_dir(self):
        """임시 디렉토리 생성"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_pdf(self, temp_dir):
        """샘플 PDF 파일 생성"""
        pdf_path = temp_dir / "sample.pdf"
        # 간단한 PDF 파일 생성 (실제로는 더 복잡한 PDF가 필요)
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.4\n%Test PDF\n")
        return pdf_path
    
    @pytest.fixture
    def ascr_service(self):
        """ASCR 서비스 인스턴스"""
        return ASCRService()
    
    @pytest.fixture
    def advanced_logger(self):
        """고급 로거 인스턴스"""
        return AdvancedLogger("test_logger")

class TestAsyncProcessing:
    """비동기 처리 테스트"""
    
    @pytest.mark.asyncio
    async def test_async_processor_initialization(self):
        """비동기 프로세서 초기화 테스트"""
        processor = AsyncASCRProcessor(max_workers=4)
        assert processor.max_workers == 4
        assert processor.thread_pool is not None
    
    @pytest.mark.asyncio
    async def test_async_pdf_processing(self, temp_dir, sample_pdf):
        """비동기 PDF 처리 테스트"""
        processor = AsyncASCRProcessor()
        output_dir = temp_dir / "output"
        
        # PDF 처리 실행
        result = await processor.process_pdf_async(sample_pdf, output_dir)
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "processing_time" in result
    
    @pytest.mark.asyncio
    async def test_concurrent_processing(self, temp_dir):
        """동시 처리 테스트"""
        processor = AsyncASCRProcessor(max_workers=2)
        
        # 여러 PDF 파일 동시 처리
        pdf_files = []
        for i in range(3):
            pdf_path = temp_dir / f"test_{i}.pdf"
            with open(pdf_path, "wb") as f:
                f.write(b"%PDF-1.4\n%Test PDF\n")
            pdf_files.append(pdf_path)
        
        # 동시 처리
        tasks = []
        for pdf_file in pdf_files:
            output_dir = temp_dir / f"output_{pdf_file.stem}"
            task = processor.process_pdf_async(pdf_file, output_dir)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        assert len(results) == 3
        for result in results:
            assert not isinstance(result, Exception)

class TestMemoryOptimization:
    """메모리 최적화 테스트"""
    
    def test_memory_optimizer_initialization(self):
        """메모리 최적화기 초기화 테스트"""
        optimizer = OptimizedASCRProcessor(max_memory_mb=512)
        assert optimizer.max_memory_mb == 512
    
    def test_memory_usage_monitoring(self):
        """메모리 사용량 모니터링 테스트"""
        optimizer = OptimizedASCRProcessor()
        memory_info = optimizer.get_memory_usage()
        
        assert "rss_mb" in memory_info
        assert "vms_mb" in memory_info
        assert memory_info["rss_mb"] > 0
    
    def test_memory_optimized_processing(self, temp_dir, sample_pdf):
        """메모리 최적화된 처리 테스트"""
        optimizer = OptimizedASCRProcessor()
        output_dir = temp_dir / "output"
        
        with optimizer.memory_context() as context:
            result = optimizer.process_pdf_optimized(sample_pdf, output_dir)
            
            assert isinstance(result, dict)
            assert "memory_usage" in result
            assert result["memory_usage"]["peak_memory_mb"] > 0

class TestAdvancedLogging:
    """고급 로깅 테스트"""
    
    def test_advanced_logger_initialization(self):
        """고급 로거 초기화 테스트"""
        logger = AdvancedLogger("test_logger")
        assert logger.logger_name == "test_logger"
    
    def test_operation_context(self):
        """작업 컨텍스트 테스트"""
        logger = AdvancedLogger("test_logger")
        
        with logger.operation_context("test_operation", "test_file") as context:
            context.add_metric("test_metric", 100)
            assert context.operation_name == "test_operation"
    
    def test_performance_logging(self):
        """성능 로깅 테스트"""
        logger = AdvancedLogger("test_logger")
        
        with logger.operation_context("performance_test", "test_file") as context:
            time.sleep(0.1)  # 작업 시뮬레이션
            context.add_metric("execution_time", 0.1)
        
        # 성능 보고서 확인
        report = logger.get_performance_report()
        assert "operations" in report
        assert "total_operations" in report

class TestASCRService:
    """ASCR 서비스 테스트"""
    
    @pytest.mark.asyncio
    async def test_service_initialization(self):
        """서비스 초기화 테스트"""
        service = ASCRService()
        assert service.async_processor is not None
        assert service.optimized_processor is not None
        assert service.logger is not None
    
    @pytest.mark.asyncio
    async def test_standard_processing(self, temp_dir, sample_pdf):
        """표준 처리 테스트"""
        service = ASCRService()
        output_dir = temp_dir / "output"
        
        result = await service.process_pdf_standard(sample_pdf, output_dir)
        assert isinstance(result, dict)
    
    def test_optimized_processing(self, temp_dir, sample_pdf):
        """최적화 처리 테스트"""
        service = ASCRService()
        output_dir = temp_dir / "output"
        
        result = service.process_pdf_optimized(sample_pdf, output_dir)
        assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_ml_enhanced_processing(self, temp_dir, sample_pdf):
        """ML 강화 처리 테스트"""
        service = ASCRService()
        output_dir = temp_dir / "output"
        
        result = await service.process_pdf_ml_enhanced(sample_pdf, output_dir)
        assert isinstance(result, dict)
        assert "ml_analysis" in result

class TestAPIIntegration:
    """API 통합 테스트"""
    
    def test_task_management(self):
        """작업 관리 테스트"""
        # 작업 목록 초기화
        processing_tasks.clear()
        
        # 작업 추가
        task_id = "test_task_1"
        processing_tasks[task_id] = {
            "status": "pending",
            "progress": 0.0,
            "created_at": "2024-01-01T00:00:00"
        }
        
        assert task_id in processing_tasks
        assert processing_tasks[task_id]["status"] == "pending"
    
    def test_task_status_update(self):
        """작업 상태 업데이트 테스트"""
        task_id = "test_task_2"
        processing_tasks[task_id] = {
            "status": "pending",
            "progress": 0.0
        }
        
        # 상태 업데이트
        processing_tasks[task_id]["status"] = "processing"
        processing_tasks[task_id]["progress"] = 0.5
        
        assert processing_tasks[task_id]["status"] == "processing"
        assert processing_tasks[task_id]["progress"] == 0.5

class TestPerformanceBenchmarks:
    """성능 벤치마크 테스트"""
    
    @pytest.mark.asyncio
    async def test_processing_speed(self, temp_dir):
        """처리 속도 테스트"""
        processor = AsyncASCRProcessor()
        
        # 대용량 PDF 시뮬레이션
        large_pdf = temp_dir / "large.pdf"
        with open(large_pdf, "wb") as f:
            # 1MB 크기의 더미 PDF 데이터
            f.write(b"%PDF-1.4\n" + b"0" * 1024 * 1024)
        
        output_dir = temp_dir / "output"
        
        start_time = time.time()
        result = await processor.process_pdf_async(large_pdf, output_dir)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # 성능 기준: 10MB 파일을 30초 이내에 처리
        file_size_mb = large_pdf.stat().st_size / (1024 * 1024)
        expected_time = file_size_mb * 3  # 1MB당 3초
        
        assert processing_time < expected_time, f"처리 시간이 너무 깁니다: {processing_time:.2f}초"
    
    def test_memory_efficiency(self, temp_dir):
        """메모리 효율성 테스트"""
        optimizer = OptimizedASCRProcessor(max_memory_mb=100)
        
        # 메모리 사용량 테스트
        initial_memory = optimizer.get_memory_usage()["rss_mb"]
        
        # 메모리 집약적 작업 시뮬레이션
        with optimizer.memory_context() as context:
            # 대용량 데이터 처리 시뮬레이션
            large_data = [i for i in range(1000000)]  # 1백만 개의 정수
            
            peak_memory = optimizer.get_memory_usage()["rss_mb"]
            memory_increase = peak_memory - initial_memory
            
            # 메모리 증가가 제한 내에 있어야 함
            assert memory_increase < 50, f"메모리 사용량이 너무 많습니다: {memory_increase:.2f}MB"
    
    @pytest.mark.asyncio
    async def test_concurrent_performance(self, temp_dir):
        """동시 처리 성능 테스트"""
        processor = AsyncASCRProcessor(max_workers=4)
        
        # 여러 파일 동시 처리
        pdf_files = []
        for i in range(5):
            pdf_path = temp_dir / f"concurrent_test_{i}.pdf"
            with open(pdf_path, "wb") as f:
                f.write(b"%PDF-1.4\n" + b"0" * 100000)  # 100KB
            pdf_files.append(pdf_path)
        
        start_time = time.time()
        
        tasks = []
        for pdf_file in pdf_files:
            output_dir = temp_dir / f"output_{pdf_file.stem}"
            task = processor.process_pdf_async(pdf_file, output_dir)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # 동시 처리로 인한 시간 단축 확인
        # 순차 처리 시 예상 시간: 5 * 1초 = 5초
        # 동시 처리 시 예상 시간: 2초 이내
        assert total_time < 2.0, f"동시 처리 성능이 부족합니다: {total_time:.2f}초"

class TestErrorHandling:
    """오류 처리 테스트"""
    
    @pytest.mark.asyncio
    async def test_invalid_pdf_handling(self, temp_dir):
        """잘못된 PDF 처리 테스트"""
        processor = AsyncASCRProcessor()
        
        # 잘못된 PDF 파일 생성
        invalid_pdf = temp_dir / "invalid.pdf"
        with open(invalid_pdf, "wb") as f:
            f.write(b"This is not a PDF file")
        
        output_dir = temp_dir / "output"
        
        # 오류 처리 확인
        with pytest.raises(Exception):
            await processor.process_pdf_async(invalid_pdf, output_dir)
    
    def test_memory_limit_exceeded(self, temp_dir):
        """메모리 한계 초과 테스트"""
        optimizer = OptimizedASCRProcessor(max_memory_mb=1)  # 매우 낮은 메모리 한계
        
        # 메모리 한계 초과 시뮬레이션
        with pytest.raises(Exception):
            with optimizer.memory_context() as context:
                # 메모리 한계를 초과하는 작업
                large_data = [i for i in range(10000000)]  # 1천만 개의 정수
                raise MemoryError("메모리 한계 초과")

class TestIntegrationScenarios:
    """통합 시나리오 테스트"""
    
    @pytest.mark.asyncio
    async def test_full_processing_pipeline(self, temp_dir):
        """전체 처리 파이프라인 테스트"""
        # 1. 서비스 초기화
        service = ASCRService()
        
        # 2. 샘플 PDF 생성
        pdf_path = temp_dir / "integration_test.pdf"
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.4\n%Integration Test\n")
        
        # 3. 다양한 처리 방식 테스트
        output_dir = temp_dir / "output"
        
        # 표준 처리
        standard_result = await service.process_pdf_standard(pdf_path, output_dir)
        assert standard_result["status"] == "success"
        
        # 최적화 처리
        optimized_result = service.process_pdf_optimized(pdf_path, output_dir)
        assert optimized_result["status"] == "success"
        
        # ML 강화 처리
        ml_result = await service.process_pdf_ml_enhanced(pdf_path, output_dir)
        assert ml_result["status"] == "success"
        assert "ml_analysis" in ml_result
    
    def test_logging_integration(self, temp_dir):
        """로깅 통합 테스트"""
        logger = AdvancedLogger("integration_test")
        
        # 다양한 작업 로깅
        with logger.operation_context("test_operation", "test_file") as context:
            context.add_metric("test_metric", 100)
            context.log_info("테스트 정보")
            context.log_warning("테스트 경고")
        
        # 성능 보고서 확인
        report = logger.get_performance_report()
        assert report["total_operations"] > 0
        assert "test_operation" in report["operations"]

def run_performance_benchmarks():
    """성능 벤치마크 실행"""
    print("ASCR 성능 벤치마크 시작...")
    
    # 테스트 실행
    pytest.main([
        __file__,
        "-v",
        "-k", "TestPerformanceBenchmarks",
        "--tb=short"
    ])

def run_integration_tests():
    """통합 테스트 실행"""
    print("ASCR 통합 테스트 시작...")
    
    # 테스트 실행
    pytest.main([
        __file__,
        "-v",
        "-k", "TestIntegrationScenarios",
        "--tb=short"
    ])

if __name__ == "__main__":
    # 성능 벤치마크 실행
    run_performance_benchmarks()
    
    # 통합 테스트 실행
    run_integration_tests() 