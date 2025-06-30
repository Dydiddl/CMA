#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 분할 유틸리티 모듈 (리팩토링됨)

목차 기반 PDF 분할 기능을 제공합니다.
기존 443줄에서 150줄로 대폭 간소화되었습니다.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional

# 새로운 모듈들 import
from .pdf_loader import PDFLoader
from .chapter_extractor import ChapterExtractor
from .pdf_splitter import PDFSplitter

class PDFSplitUtils:
    """PDF 분할 유틸리티 클래스 (리팩토링됨)"""
    
    def __init__(self, json_file_path: Path, pdf_file_path: Path, output_dir: Optional[Path] = None):
        """초기화"""
        self.json_file_path = json_file_path
        self.pdf_file_path = pdf_file_path
        self.output_dir = output_dir or Path("output")
        
        # 새로운 모듈들 초기화
        self.loader = PDFLoader(json_file_path, pdf_file_path, self.output_dir)
        self.extractor = None
        self.splitter = None
    
    def load_data(self) -> bool:
        """데이터 로드"""
        try:
            # PDF와 JSON 데이터 로드
            if not self.loader.load_pdf():
                return False
            
            if not self.loader.load_json_data():
                return False
            
            # 데이터 유효성 검증
            if not self.loader.validate_data():
                return False
            
            # 장 정보 추출기 초기화
            toc_data = self.loader.get_toc_data()
            if toc_data:
                self.extractor = ChapterExtractor(toc_data)
            
            # PDF 분할기 초기화
            pdf_reader = self.loader.get_pdf_reader()
            if pdf_reader:
                self.splitter = PDFSplitter(pdf_reader, self.output_dir)
            
            return True
            
        except Exception as e:
            print(f"❌ 데이터 로드 실패: {e}")
            return False
    
    def split(self, mode: str = 'chapter') -> bool:
        """
        PDF 분할 실행
        
        Args:
            mode: 분할 모드 ('chapter', 'section')
            
        Returns:
            bool: 성공 여부
        """
        try:
            # 데이터 로드 확인
            if not self.extractor or not self.splitter:
                if not self.load_data():
                    return False
            
            # 장 정보 추출
            chapters_by_section = self.extractor.extract_chapters_by_section()
            if not chapters_by_section:
                print("❌ 장 정보를 추출할 수 없습니다")
                return False
            
            # 페이지 범위 계산 및 검증
            total_pages = self.loader.get_total_pages()
            for section, chapters in chapters_by_section.items():
                if chapters:
                    chapters_by_section[section] = self.extractor.validate_and_correct_page_ranges(
                        chapters, total_pages
                    )
            
            # 분할 실행
            if mode == 'chapter':
                result = self.splitter.split_by_chapter(chapters_by_section)
            elif mode == 'section':
                result = self.splitter.split_by_section(chapters_by_section)
            else:
                print(f"❌ 지원하지 않는 분할 모드: {mode}")
                return False
            
            return result.get("error_count", 1) == 0
            
        except Exception as e:
            print(f"❌ PDF 분할 실패: {e}")
            return False
    
    def get_analysis_report(self) -> Dict[str, Any]:
        """분석 보고서 생성"""
        try:
            if not self.extractor:
                if not self.load_data():
                    return {}
            
            chapters_by_section = self.extractor.extract_chapters_by_section()
            analysis = self.extractor.analyze_chapter_structure(chapters_by_section)
            
            return {
                "chapters_by_section": chapters_by_section,
                "analysis": analysis,
                "total_pages": self.loader.get_total_pages()
            }
            
        except Exception as e:
            print(f"❌ 분석 보고서 생성 실패: {e}")
            return {}

def main():
    """메인 함수"""
    import sys
    
    if len(sys.argv) < 3:
        print("사용법: python pdf_split_utils.py <json_file> <pdf_file> [output_dir]")
        sys.exit(1)
    
    json_file = Path(sys.argv[1])
    pdf_file = Path(sys.argv[2])
    output_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("output")
    
    # PDF 분할 실행
    splitter = PDFSplitUtils(json_file, pdf_file, output_dir)
    
    if splitter.split('chapter'):
        print("✅ PDF 분할이 성공적으로 완료되었습니다")
    else:
        print("❌ PDF 분할에 실패했습니다")
        sys.exit(1)

if __name__ == "__main__":
    main() 