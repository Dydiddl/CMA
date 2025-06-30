#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 로더 모듈 (PDF Loader)

이 모듈은 PDF 파일을 로드하고 기본 정보를 추출하는 기능을 제공합니다.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pypdf import PdfReader

# ASCR 커스텀 로깅 시스템 사용
from ..log import get_logger

# 공통 모듈 import
from src.common.constants import SUCCESS_MESSAGES, ERROR_MESSAGES
from src.common.utils import validate_pdf_file, ensure_directory
from src.common.exceptions import PDFLoadError, FileNotFoundError

# 로거 초기화
logger = get_logger("PDFLoader")

class PDFLoader:
    """PDF 로더 클래스"""
    
    def __init__(self, json_file_path: Path, pdf_file_path: Path, output_dir: Optional[Path] = None):
        """초기화"""
        self.json_file_path = json_file_path
        self.pdf_file_path = pdf_file_path
        self.output_dir = output_dir or Path("output")
        self.pdf_reader = None
        self.toc_data = None
        self.total_pages = 0
        
        # 출력 디렉토리 생성
        ensure_directory(self.output_dir)
    
    def load_pdf(self) -> bool:
        """PDF 파일 로드"""
        try:
            if not validate_pdf_file(self.pdf_file_path):
                return False
                
            self.pdf_reader = PdfReader(self.pdf_file_path)
            self.total_pages = len(self.pdf_reader.pages)
            print(SUCCESS_MESSAGES["pdf_load"].format(self.total_pages))
            logger.info(f"PDF 로드 성공: {self.total_pages}페이지")
            return True
        except Exception as e:
            print(ERROR_MESSAGES["pdf_load_failed"].format(e))
            logger.error(f"PDF 로드 실패: {e}")
            return False
    
    def load_json_data(self) -> bool:
        """JSON 파일 로드"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.toc_data = json.load(f)
            print(SUCCESS_MESSAGES["json_load"].format(self.json_file_path))
            logger.info(f"JSON 데이터 로드 성공: {self.json_file_path}")
            return True
        except Exception as e:
            print(ERROR_MESSAGES["json_load_failed"].format(e))
            logger.error(f"JSON 데이터 로드 실패: {e}")
            return False
    
    def get_pdf_reader(self) -> Optional[PdfReader]:
        """PDF 리더 반환"""
        if not self.pdf_reader:
            if not self.load_pdf():
                return None
        return self.pdf_reader
    
    def get_toc_data(self) -> Optional[Dict[str, Any]]:
        """목차 데이터 반환"""
        if not self.toc_data:
            if not self.load_json_data():
                return None
        return self.toc_data
    
    def get_total_pages(self) -> int:
        """총 페이지 수 반환"""
        if self.total_pages == 0:
            if not self.load_pdf():
                return 0
        return self.total_pages
    
    def validate_data(self) -> bool:
        """로드된 데이터 유효성 검증"""
        if not self.pdf_reader:
            print("❌ PDF가 로드되지 않았습니다")
            return False
        
        if not self.toc_data:
            print("❌ JSON 데이터가 로드되지 않았습니다")
            return False
        
        # 목차 데이터 구조 검증
        if 'entries' not in self.toc_data:
            print("❌ JSON 데이터에 'entries' 키가 없습니다")
            return False
        
        entries = self.toc_data.get('entries', [])
        if not isinstance(entries, list) or len(entries) == 0:
            print("❌ JSON 데이터에 유효한 entries가 없습니다")
            return False
        
        print("✅ 데이터 유효성 검증 통과")
        return True 