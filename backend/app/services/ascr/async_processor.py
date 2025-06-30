#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 비동기 처리 모듈
성능 최적화를 위한 비동기 처리 기능 구현
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiofiles
from pypdf import PdfReader, PdfWriter
import json

logger = logging.getLogger(__name__)

class AsyncASCRProcessor:
    """ASCR 비동기 처리 클래스"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.loop = asyncio.get_event_loop()
    
    async def process_pdf_async(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """PDF 비동기 처리 메인 함수"""
        try:
            logger.info(f"비동기 PDF 처리 시작: {pdf_path}")
            
            # 1. PDF 정보 수집
            pdf_info = await self._get_pdf_info_async(pdf_path)
            
            # 2. 텍스트 추출 (비동기)
            text_content = await self._extract_text_async(pdf_path)
            
            # 3. 목차 구조 분석 (비동기)
            toc_structure = await self._analyze_toc_structure_async(text_content)
            
            # 4. PDF 분할 (비동기)
            split_results = await self._split_pdf_async(pdf_path, toc_structure, output_dir)
            
            # 5. 결과 저장 (비동기)
            await self._save_results_async(output_dir, {
                "pdf_info": pdf_info,
                "toc_structure": toc_structure,
                "split_results": split_results
            })
            
            logger.info(f"비동기 PDF 처리 완료: {pdf_path}")
            return {
                "status": "success",
                "pdf_info": pdf_info,
                "toc_structure": toc_structure,
                "split_results": split_results
            }
            
        except Exception as e:
            logger.error(f"비동기 PDF 처리 실패: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _get_pdf_info_async(self, pdf_path: Path) -> Dict[str, Any]:
        """PDF 정보 비동기 수집"""
        def get_pdf_info():
            try:
                reader = PdfReader(pdf_path)
                return {
                    "total_pages": len(reader.pages),
                    "file_size": pdf_path.stat().st_size,
                    "file_name": pdf_path.name,
                    "creation_date": pdf_path.stat().st_ctime
                }
            except Exception as e:
                logger.error(f"PDF 정보 수집 실패: {e}")
                return {}
        
        return await self.loop.run_in_executor(self.thread_pool, get_pdf_info)
    
    async def _extract_text_async(self, pdf_path: Path) -> str:
        """PDF 텍스트 비동기 추출"""
        def extract_text():
            try:
                reader = PdfReader(pdf_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except Exception as e:
                logger.error(f"텍스트 추출 실패: {e}")
                return ""
        
        return await self.loop.run_in_executor(self.thread_pool, extract_text)
    
    async def _analyze_toc_structure_async(self, text_content: str) -> Dict[str, Any]:
        """목차 구조 비동기 분석"""
        def analyze_toc():
            try:
                # 목차 패턴 분석
                lines = text_content.split('\n')
                toc_structure = {
                    "sections": [],
                    "chapters": [],
                    "subsections": []
                }
                
                for i, line in enumerate(lines):
                    line = line.strip()
                    
                    # 부문 패턴 (예: "공통부문", "토목부문")
                    if "부문" in line and len(line) < 20:
                        toc_structure["sections"].append({
                            "title": line,
                            "line_number": i + 1,
                            "level": 1
                        })
                    
                    # 장 패턴 (예: "제1장", "제2장")
                    elif line.startswith("제") and "장" in line:
                        toc_structure["chapters"].append({
                            "title": line,
                            "line_number": i + 1,
                            "level": 2
                        })
                    
                    # 절 패턴 (예: "1-1", "2-1")
                    elif "-" in line and len(line.split("-")) == 2:
                        parts = line.split("-")
                        if parts[0].isdigit() and parts[1].isdigit():
                            toc_structure["subsections"].append({
                                "title": line,
                                "line_number": i + 1,
                                "level": 3
                            })
                
                return toc_structure
                
            except Exception as e:
                logger.error(f"목차 구조 분석 실패: {e}")
                return {"sections": [], "chapters": [], "subsections": []}
        
        return await self.loop.run_in_executor(self.thread_pool, analyze_toc)
    
    async def _split_pdf_async(self, pdf_path: Path, toc_structure: Dict, output_dir: Path) -> List[Dict[str, Any]]:
        """PDF 비동기 분할"""
        def split_pdf():
            try:
                reader = PdfReader(pdf_path)
                split_results = []
                
                # 부문별로 PDF 분할
                for section in toc_structure.get("sections", []):
                    section_name = section["title"]
                    section_file = output_dir / f"{section_name}.pdf"
                    
                    # 임시로 전체 PDF를 복사 (실제 분할 로직은 더 복잡)
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    with open(section_file, 'wb') as output_file:
                        writer.write(output_file)
                    
                    split_results.append({
                        "section": section_name,
                        "file_path": str(section_file),
                        "pages": len(reader.pages)
                    })
                
                return split_results
                
            except Exception as e:
                logger.error(f"PDF 분할 실패: {e}")
                return []
        
        return await self.loop.run_in_executor(self.thread_pool, split_pdf)
    
    async def _save_results_async(self, output_dir: Path, results: Dict[str, Any]):
        """결과 비동기 저장"""
        async def save_json():
            try:
                output_file = output_dir / "processing_results.json"
                async with aiofiles.open(output_file, 'w', encoding='utf-8') as f:
                    await f.write(json.dumps(results, ensure_ascii=False, indent=2))
                logger.info(f"결과 저장 완료: {output_file}")
            except Exception as e:
                logger.error(f"결과 저장 실패: {e}")
        
        await save_json()
    
    async def batch_process_pdfs(self, pdf_files: List[Path], output_dir: Path) -> List[Dict[str, Any]]:
        """여러 PDF 파일 배치 처리"""
        tasks = []
        for pdf_file in pdf_files:
            task = self.process_pdf_async(pdf_file, output_dir)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def close(self):
        """리소스 정리"""
        self.thread_pool.shutdown(wait=True)

# 사용 예시
async def main():
    """비동기 처리 예시"""
    processor = AsyncASCRProcessor(max_workers=4)
    
    try:
        # 단일 파일 처리
        pdf_path = Path("input/test.pdf")
        output_dir = Path("output")
        
        if pdf_path.exists():
            result = await processor.process_pdf_async(pdf_path, output_dir)
            print(f"처리 결과: {result}")
        
        # 배치 처리
        pdf_files = [Path("input/file1.pdf"), Path("input/file2.pdf")]
        results = await processor.batch_process_pdfs(pdf_files, output_dir)
        print(f"배치 처리 결과: {results}")
        
    finally:
        await processor.close()

if __name__ == "__main__":
    asyncio.run(main()) 