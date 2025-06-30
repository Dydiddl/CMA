#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
목차 추출 모듈 (TOC Extractor)

이 모듈은 PDF에서 목차를 추출하고 구조화하는 기능을 제공합니다.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# ASCR 커스텀 로깅 시스템 사용
from ..log import get_logger

# 분리된 모듈들 import
from .toc_pdf_extractor import TOCPDFExtractor
from .toc_structure_analyzer import TOCStructureAnalyzer
from .toc_mapping_generator import TOCMappingGenerator

# 공통 모듈 import
from src.common.types import TOCStructure
from src.common.exceptions import TOCExtractionError

# 로거 초기화
logger = get_logger("TOCExtractor")

class TOCExtractor:
    """목차 추출 통합 클래스"""
    
    def __init__(self):
        self.pdf_extractor = TOCPDFExtractor()
        self.structure_analyzer = TOCStructureAnalyzer()
        self.mapping_generator = TOCMappingGenerator()
    
    def extract_toc_pdf(self, pdf_path: Path, output_path: Optional[Path] = None, 
                       max_pages: int = 100, force_end_page: int = None) -> Optional[Path]:
        """
        PDF에서 목차 부분을 추출하여 별도 PDF로 저장
        """
        return self.pdf_extractor.extract_toc_pdf(pdf_path, output_path, max_pages, force_end_page)
    
    def extract_toc_structure(self, content: str, method: str = 'auto') -> TOCStructure:
        """
        텍스트에서 목차 구조 추출
        """
        return self.structure_analyzer.analyze_toc_structure(content, method)
    
    def generate_mapping_config(self, toc_structure: TOCStructure) -> Dict[str, Any]:
        """
        목차 구조를 기반으로 매핑 설정 생성
        """
        return self.mapping_generator.generate_mapping_config(toc_structure)
    
    def save_toc_structure(self, toc_structure: TOCStructure, 
                          output_path: Path, format: str = 'json') -> bool:
        """
        목차 구조를 파일로 저장
        """
        return self.mapping_generator.save_toc_structure(toc_structure, output_path, format)
    
    def validate_toc_structure(self, toc_structure) -> bool:
        """
        목차 구조 검증
        """
        return self.mapping_generator.validate_toc_structure(toc_structure)

# 편의 함수들
def extract_toc_from_pdf(pdf_path: Path, method: str = 'auto') -> Optional[TOCStructure]:
    """
    PDF에서 목차 구조 추출 (편의 함수)
    """
    try:
        extractor = TOCExtractor()
        
        # 1. PDF에서 목차 부분 추출
        toc_pdf_path = extractor.extract_toc_pdf(pdf_path)
        if not toc_pdf_path:
            logger.error("목차 PDF 추출 실패")
            return None
        
        # 2. 추출된 PDF에서 텍스트 읽기
        from pypdf import PdfReader
        reader = PdfReader(toc_pdf_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text() + "\n"
        
        # 3. 목차 구조 분석
        toc_structure = extractor.extract_toc_structure(content, method)
        
        return toc_structure
        
    except Exception as e:
        logger.error(f"목차 추출 실패: {e}")
        return None

def create_mapping_config_from_pdf(pdf_path: Path) -> Optional[Dict[str, Any]]:
    """
    PDF에서 매핑 설정 생성 (편의 함수)
    """
    try:
        toc_structure = extract_toc_from_pdf(pdf_path)
        if not toc_structure:
            return None
        
        extractor = TOCExtractor()
        mapping_config = extractor.generate_mapping_config(toc_structure)
        
        return mapping_config
        
    except Exception as e:
        logger.error(f"매핑 설정 생성 실패: {e}")
        return None 