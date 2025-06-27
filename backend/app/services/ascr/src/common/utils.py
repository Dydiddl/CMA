#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 공통 유틸리티 함수

이 모듈은 ASCR 프로젝트에서 공통으로 사용되는 유틸리티 함수들을 제공합니다.
"""

import logging
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

# 분리된 모듈들 import
from .file_utils import (
    validate_pdf_file, get_file_hash, ensure_directory, get_safe_filename,
    format_file_size, get_current_timestamp, load_json_data, save_json_data,
    merge_dictionaries, create_section_directory, get_output_path, show_progress
)

from .text_utils import (
    clean_text, extract_page_number, determine_section, normalize_text,
    find_toc_page_range, validate_toc_structure, validate_section_name,
    is_valid_page_number, get_section_for_chapter, calculate_confidence_score,
    extract_chapter_info, performance_monitor, cache_result, batch_process,
    determine_section_with_confidence, validate_section_classification
)

# 공통 모듈 import
from .constants import (
    SECTION_MAPPING, SECTION_KEYWORDS, TOC_PATTERNS, 
    SUPPORTED_FORMATS, MAX_FILENAME_LENGTH,
    SUCCESS_MESSAGES, ERROR_MESSAGES, WARNING_MESSAGES
)
from .types import FilePath, JSONData, ChapterInfo, ValidationResult, SectionName, ChapterTitle
from .exceptions import FileValidationError, DataFormatError

def setup_logging_for_module(module_name: str, log_level: str = "INFO") -> logging.Logger:
    """모듈별 로깅 설정"""
    logger = logging.getLogger(module_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 핸들러가 없으면 추가
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# 편의 함수들 - 기존 함수들을 그대로 유지하되 새로운 모듈의 함수들을 사용
__all__ = [
    # 파일 처리 함수들
    'validate_pdf_file', 'get_file_hash', 'ensure_directory', 'get_safe_filename',
    'format_file_size', 'get_current_timestamp', 'load_json_data', 'save_json_data',
    'merge_dictionaries', 'create_section_directory', 'get_output_path', 'show_progress',
    
    # 텍스트 처리 함수들
    'clean_text', 'extract_page_number', 'determine_section', 'normalize_text',
    'find_toc_page_range', 'validate_toc_structure', 'validate_section_name',
    'is_valid_page_number', 'get_section_for_chapter', 'calculate_confidence_score',
    'extract_chapter_info', 'performance_monitor', 'cache_result', 'batch_process',
    'determine_section_with_confidence', 'validate_section_classification',
    
    # 로깅 함수
    'setup_logging_for_module'
] 