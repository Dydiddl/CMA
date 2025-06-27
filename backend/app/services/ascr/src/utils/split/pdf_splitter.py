#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 분할 모듈 (PDF Splitter)

이 모듈은 PDF를 부문별, 장별로 분할하는 기능을 제공합니다.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pypdf import PdfWriter

# ASCR 커스텀 로깅 시스템 사용
from ..log import get_logger

# 공통 모듈 import
from src.common.utils import get_safe_filename, show_progress, ensure_directory
from src.common.exceptions import PDFSplitError

# 로거 초기화
logger = get_logger("PDFSplitter")

class PDFSplitter:
    """PDF 분할 클래스"""
    
    def __init__(self, pdf_reader, output_dir: Path):
        """초기화"""
        self.pdf_reader = pdf_reader
        self.output_dir = output_dir
        self.total_pages = len(pdf_reader.pages) if pdf_reader else 0
    
    def split_by_chapter(self, chapters_by_section: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """장별 분할"""
        try:
            success_count = 0
            error_count = 0
            
            print("=== 장별 PDF 분할 시작 ===")
            
            for section_name, chapters in chapters_by_section.items():
                if not chapters:
                    continue
                
                print(f"\n📁 {section_name} 처리 중...")
                
                # 부문별 디렉토리 생성
                section_dir = self.create_section_directory(section_name)
                
                for i, chapter in enumerate(chapters):
                    title = chapter['title']
                    start_page = chapter.get('start_page', 0)
                    end_page = chapter.get('end_page', 0)
                    
                    if start_page <= 0 or end_page <= 0:
                        print(f"  ⚠️ {title}: 유효하지 않은 페이지 범위")
                        error_count += 1
                        continue
                    
                    # 안전한 파일명 생성
                    safe_filename = get_safe_filename(title)
                    output_path = section_dir / f"{safe_filename}.pdf"
                    
                    print(f"  📄 {title} (p.{start_page}-{end_page})")
                    
                    # PDF 분할
                    if self.split_pdf_by_pages(start_page, end_page, output_path):
                        success_count += 1
                    else:
                        error_count += 1
                    
                    # 진행률 표시
                    show_progress(i + 1, len(chapters), f"{section_name} - {title}")
            
            # 분할 결과 보고서 생성
            self._generate_split_report(chapters_by_section, success_count, error_count)
            
            print(f"\n✅ 분할 완료: 성공 {success_count}개, 실패 {error_count}개")
            return {
                "success_count": success_count,
                "error_count": error_count,
                "total_processed": success_count + error_count
            }
            
        except Exception as e:
            logger.error(f"장별 분할 실패: {e}")
            print(f"❌ 장별 분할 실패: {e}")
            return {"success_count": 0, "error_count": 1, "total_processed": 1}
    
    def split_by_section(self, chapters_by_section: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """부문별 분할 (부문별 폴더 아래에 장별 개별 PDF 생성)"""
        try:
            success_count = 0
            error_count = 0
            
            print("=== 부문별 PDF 분할 시작 ===")
            
            for section_name, chapters in chapters_by_section.items():
                if not chapters:
                    continue
                
                print(f"\n📁 {section_name} 처리 중...")
                
                # 부문별 디렉토리 생성
                section_dir = self.create_section_directory(section_name)
                
                for i, chapter in enumerate(chapters):
                    title = chapter['title']
                    start_page = chapter.get('start_page', 0)
                    end_page = chapter.get('end_page', 0)
                    
                    if start_page <= 0 or end_page <= 0:
                        print(f"  ⚠️ {title}: 유효하지 않은 페이지 범위")
                        error_count += 1
                        continue
                    
                    # 안전한 파일명 생성
                    safe_filename = get_safe_filename(title)
                    output_path = section_dir / f"{safe_filename}.pdf"
                    
                    print(f"  📄 {title} (p.{start_page}-{end_page})")
                    
                    # PDF 분할
                    if self.split_pdf_by_pages(start_page, end_page, output_path):
                        success_count += 1
                    else:
                        error_count += 1
                    
                    # 진행률 표시
                    show_progress(i + 1, len(chapters), f"{section_name} - {title}")
            
            # 부문별 분할 결과 보고서 생성
            self._generate_section_report(chapters_by_section, success_count, error_count)
            
            print(f"\n✅ 부문별 분할 완료: 성공 {success_count}개, 실패 {error_count}개")
            return {
                "success_count": success_count,
                "error_count": error_count,
                "total_processed": success_count + error_count
            }
            
        except Exception as e:
            logger.error(f"부문별 분할 실패: {e}")
            print(f"❌ 부문별 분할 실패: {e}")
            return {"success_count": 0, "error_count": 1, "total_processed": 1}
    
    def split_pdf_by_pages(self, start_page: int, end_page: int, output_path: Path) -> bool:
        """지정된 페이지 범위로 PDF 분할"""
        try:
            if not self.pdf_reader:
                logger.error("PDF 리더가 초기화되지 않았습니다")
                return False
            
            # 페이지 범위 검증
            if start_page < 1 or end_page > self.total_pages or start_page > end_page:
                logger.error(f"유효하지 않은 페이지 범위: {start_page}-{end_page}")
                return False
            
            # PDF 분할
            writer = PdfWriter()
            
            # 0-based 인덱스로 변환
            for page_num in range(start_page - 1, end_page):
                if page_num < len(self.pdf_reader.pages):
                    page = self.pdf_reader.pages[page_num]
                    writer.add_page(page)
            
            # 출력 파일 저장
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            logger.info(f"PDF 분할 성공: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"PDF 분할 실패: {e}")
            return False
    
    def create_section_directory(self, section_name: str) -> Path:
        """부문별 디렉토리 생성"""
        section_dir = self.output_dir / get_safe_filename(section_name)
        ensure_directory(section_dir)
        return section_dir
    
    def _generate_split_report(self, chapters_by_section: Dict[str, List[Dict]], 
                              success_count: int, error_count: int):
        """분할 결과 보고서 생성"""
        try:
            report_path = self.output_dir / "split_report.txt"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=== PDF 분할 결과 보고서 ===\n")
                f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"총 페이지 수: {self.total_pages}\n")
                f.write(f"성공: {success_count}개\n")
                f.write(f"실패: {error_count}개\n\n")
                
                f.write("부문별 분할 결과:\n")
                for section_name, chapters in chapters_by_section.items():
                    if chapters:
                        f.write(f"\n📁 {section_name}:\n")
                        for chapter in chapters:
                            title = chapter['title']
                            start_page = chapter.get('start_page', 0)
                            end_page = chapter.get('end_page', 0)
                            f.write(f"  - {title} (p.{start_page}-{end_page})\n")
            
            print(f"📄 분할 보고서 생성: {report_path}")
            
        except Exception as e:
            logger.error(f"분할 보고서 생성 실패: {e}")
    
    def _generate_section_report(self, chapters_by_section: Dict[str, List[Dict]], 
                                success_count: int, error_count: int):
        """부문별 분할 결과 보고서 생성"""
        try:
            report_path = self.output_dir / "section_split_report.txt"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=== 부문별 PDF 분할 결과 보고서 ===\n")
                f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"총 페이지 수: {self.total_pages}\n")
                f.write(f"성공: {success_count}개\n")
                f.write(f"실패: {error_count}개\n\n")
                
                f.write("부문별 상세 결과:\n")
                for section_name, chapters in chapters_by_section.items():
                    if chapters:
                        f.write(f"\n📁 {section_name}:\n")
                        f.write(f"  장 수: {len(chapters)}개\n")
                        
                        # 페이지 범위 계산
                        pages = [ch.get('page', 0) for ch in chapters]
                        if pages:
                            f.write(f"  페이지 범위: {min(pages)}-{max(pages)}\n")
                        
                        for chapter in chapters:
                            title = chapter['title']
                            start_page = chapter.get('start_page', 0)
                            end_page = chapter.get('end_page', 0)
                            f.write(f"  - {title} (p.{start_page}-{end_page})\n")
            
            print(f"📄 부문별 분할 보고서 생성: {report_path}")
            
        except Exception as e:
            logger.error(f"부문별 분할 보고서 생성 실패: {e}") 