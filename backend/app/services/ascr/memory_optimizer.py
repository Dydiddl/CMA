#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 메모리 최적화 모듈
대용량 PDF 처리 시 메모리 사용량 최적화
"""

import gc
import logging
import psutil
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Generator
from contextlib import contextmanager
import weakref

logger = logging.getLogger(__name__)

class MemoryOptimizer:
    """메모리 최적화 클래스"""
    
    def __init__(self, max_memory_mb: int = 1024):
        self.max_memory_mb = max_memory_mb
        self.process = psutil.Process(os.getpid())
    
    def get_memory_usage(self) -> Dict[str, float]:
        """현재 메모리 사용량 조회"""
        memory_info = self.process.memory_info()
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,  # Resident Set Size
            "vms_mb": memory_info.vms / 1024 / 1024,  # Virtual Memory Size
            "percent": self.process.memory_percent()
        }
    
    def check_memory_limit(self) -> bool:
        """메모리 제한 확인"""
        memory_usage = self.get_memory_usage()
        return memory_usage["rss_mb"] < self.max_memory_mb
    
    @contextmanager
    def memory_monitor(self, operation_name: str):
        """메모리 사용량 모니터링 컨텍스트 매니저"""
        start_memory = self.get_memory_usage()
        logger.info(f"[MEMORY] {operation_name} 시작 - 메모리: {start_memory['rss_mb']:.1f}MB")
        
        try:
            yield
        finally:
            end_memory = self.get_memory_usage()
            memory_diff = end_memory["rss_mb"] - start_memory["rss_mb"]
            logger.info(f"[MEMORY] {operation_name} 완료 - 메모리 변화: {memory_diff:+.1f}MB")
            
            # 메모리 정리
            if memory_diff > 100:  # 100MB 이상 증가 시 강제 정리
                self.force_garbage_collection()
    
    def force_garbage_collection(self):
        """강제 가비지 컬렉션"""
        collected = gc.collect()
        logger.info(f"[MEMORY] 가비지 컬렉션 완료 - 수집된 객체: {collected}")
    
    def optimize_large_pdf_processing(self, pdf_path: Path, chunk_size: int = 10) -> Generator[Dict[str, Any], None, None]:
        """대용량 PDF 청크 단위 처리"""
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            for start_page in range(0, total_pages, chunk_size):
                end_page = min(start_page + chunk_size, total_pages)
                
                with self.memory_monitor(f"PDF 페이지 {start_page+1}-{end_page} 처리"):
                    chunk_data = {
                        "start_page": start_page,
                        "end_page": end_page,
                        "pages": []
                    }
                    
                    for page_num in range(start_page, end_page):
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        
                        chunk_data["pages"].append({
                            "page_number": page_num + 1,
                            "text": text,
                            "text_length": len(text)
                        })
                        
                        # 메모리 제한 확인
                        if not self.check_memory_limit():
                            logger.warning(f"[MEMORY] 메모리 제한 도달 - 청크 처리 중단")
                            self.force_garbage_collection()
                            break
                    
                    yield chunk_data
                    
                    # 청크 처리 후 메모리 정리
                    del chunk_data
                    self.force_garbage_collection()
                    
        except Exception as e:
            logger.error(f"[MEMORY] PDF 청크 처리 실패: {e}")
            raise

class ErrorHandler:
    """에러 처리 클래스"""
    
    def __init__(self):
        self.error_count = 0
        self.max_retries = 3
    
    @contextmanager
    def error_context(self, operation_name: str):
        """에러 처리 컨텍스트 매니저"""
        try:
            yield
        except FileNotFoundError as e:
            logger.error(f"[ERROR] 파일을 찾을 수 없음 - {operation_name}: {e}")
            raise
        except PermissionError as e:
            logger.error(f"[ERROR] 권한 오류 - {operation_name}: {e}")
            raise
        except MemoryError as e:
            logger.error(f"[ERROR] 메모리 부족 - {operation_name}: {e}")
            self.error_count += 1
            raise
        except Exception as e:
            logger.error(f"[ERROR] 예상치 못한 오류 - {operation_name}: {e}")
            self.error_count += 1
            raise
    
    def retry_operation(self, operation, max_retries: int = None):
        """작업 재시도"""
        if max_retries is None:
            max_retries = self.max_retries
        
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                logger.warning(f"[RETRY] 시도 {attempt + 1}/{max_retries} 실패: {e}")
                if attempt == max_retries - 1:
                    raise
                continue

class ResourceManager:
    """리소스 관리 클래스"""
    
    def __init__(self):
        self.resources = weakref.WeakSet()
    
    def register_resource(self, resource):
        """리소스 등록"""
        self.resources.add(resource)
    
    def cleanup_resources(self):
        """리소스 정리"""
        for resource in list(self.resources):
            try:
                if hasattr(resource, 'close'):
                    resource.close()
                elif hasattr(resource, '__del__'):
                    del resource
            except Exception as e:
                logger.warning(f"[RESOURCE] 리소스 정리 실패: {e}")
        
        self.resources.clear()
        gc.collect()

class OptimizedASCRProcessor:
    """최적화된 ASCR 처리 클래스"""
    
    def __init__(self, max_memory_mb: int = 1024):
        self.memory_optimizer = MemoryOptimizer(max_memory_mb)
        self.error_handler = ErrorHandler()
        self.resource_manager = ResourceManager()
    
    def process_pdf_optimized(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """최적화된 PDF 처리"""
        with self.error_handler.error_context("PDF 처리"):
            with self.memory_optimizer.memory_monitor("전체 PDF 처리"):
                
                # PDF 정보 수집
                pdf_info = self._get_pdf_info(pdf_path)
                
                # 청크 단위 텍스트 처리
                all_text = ""
                for chunk_data in self.memory_optimizer.optimize_large_pdf_processing(pdf_path):
                    for page_data in chunk_data["pages"]:
                        all_text += page_data["text"] + "\n"
                
                # 목차 구조 분석
                toc_structure = self._analyze_toc_structure(all_text)
                
                # 결과 저장
                results = {
                    "pdf_info": pdf_info,
                    "toc_structure": toc_structure,
                    "processing_stats": {
                        "memory_usage": self.memory_optimizer.get_memory_usage(),
                        "error_count": self.error_handler.error_count
                    }
                }
                
                self._save_results(output_dir, results)
                return results
    
    def _get_pdf_info(self, pdf_path: Path) -> Dict[str, Any]:
        """PDF 정보 수집"""
        def get_info():
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            return {
                "total_pages": len(reader.pages),
                "file_size": pdf_path.stat().st_size,
                "file_name": pdf_path.name
            }
        
        return self.error_handler.retry_operation(get_info)
    
    def _analyze_toc_structure(self, text_content: str) -> Dict[str, Any]:
        """목차 구조 분석"""
        lines = text_content.split('\n')
        toc_structure = {
            "sections": [],
            "chapters": [],
            "subsections": []
        }
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 부문 패턴
            if "부문" in line and len(line) < 20:
                toc_structure["sections"].append({
                    "title": line,
                    "line_number": i + 1,
                    "level": 1
                })
            
            # 장 패턴
            elif line.startswith("제") and "장" in line:
                toc_structure["chapters"].append({
                    "title": line,
                    "line_number": i + 1,
                    "level": 2
                })
            
            # 절 패턴
            elif "-" in line and len(line.split("-")) == 2:
                parts = line.split("-")
                if parts[0].isdigit() and parts[1].isdigit():
                    toc_structure["subsections"].append({
                        "title": line,
                        "line_number": i + 1,
                        "level": 3
                    })
        
        return toc_structure
    
    def _save_results(self, output_dir: Path, results: Dict[str, Any]):
        """결과 저장"""
        import json
        
        output_file = output_dir / "optimized_processing_results.json"
        with open(output_file, 'w', encoding='utf-8', newline=\'\', encoding=\'utf-8\', newline=\'\') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"최적화된 처리 결과 저장: {output_file}")
    
    def cleanup(self):
        """정리 작업"""
        self.resource_manager.cleanup_resources()
        self.memory_optimizer.force_garbage_collection()

# 사용 예시
def main():
    """최적화된 처리 예시"""
    processor = OptimizedASCRProcessor(max_memory_mb=512)
    
    try:
        pdf_path = Path("input/test.pdf")
        output_dir = Path("output")
        
        if pdf_path.exists():
            result = processor.process_pdf_optimized(pdf_path, output_dir)
            print(f"최적화된 처리 결과: {result}")
        else:
            print("PDF 파일을 찾을 수 없습니다.")
    
    finally:
        processor.cleanup()

if __name__ == "__main__":
    main() 