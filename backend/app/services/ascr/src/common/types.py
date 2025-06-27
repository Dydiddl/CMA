#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 공통 타입 정의

이 모듈은 ASCR 프로젝트에서 공통으로 사용되는 타입 정의들을 제공합니다.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from pathlib import Path
from datetime import datetime

# =============================================================================
# 기본 타입 별칭
# =============================================================================

# 파일 경로 타입
FilePath = Union[str, Path]

# JSON 데이터 타입
JSONData = Dict[str, Any]

# 페이지 번호 타입
PageNumber = int

# 부문 이름 타입
SectionName = str

# 장 제목 타입
ChapterTitle = str

# =============================================================================
# 목차 관련 타입
# =============================================================================

@dataclass
class TOCEntry:
    """목차 항목 데이터 클래스"""
    number: str
    title: str
    page: int
    level: int
    section: str = ""
    chapter: str = ""
    subsection: str = ""
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    type: str = "item"  # "chapter", "item", "other" 중 하나
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환 (JSON 직렬화용)"""
        return {
            "number": self.number,
            "title": self.title,
            "page": self.page,
            "level": self.level,
            "section": self.section,
            "chapter": self.chapter,
            "subsection": self.subsection,
            "parent": self.parent,
            "children": self.children,
            "type": self.type
        }

@dataclass
class TOCStructure:
    """목차 구조 데이터 클래스"""
    entries: List[TOCEntry]
    sections: Dict[str, Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        from dataclasses import asdict
        return {
            "entries": [asdict(entry) for entry in self.entries],
            "sections": self.sections,
            "metadata": self.metadata
        }

# =============================================================================
# PDF 관련 타입
# =============================================================================

@dataclass
class PDFInfo:
    """PDF 파일 정보"""
    filename: str
    total_pages: int
    file_size: int
    metadata: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class PageRange:
    """페이지 범위"""
    start_page: int
    end_page: int
    
    def __post_init__(self):
        if self.start_page > self.end_page:
            raise ValueError("시작 페이지가 끝 페이지보다 클 수 없습니다.")
    
    @property
    def page_count(self) -> int:
        """페이지 수 반환"""
        return self.end_page - self.start_page + 1

# =============================================================================
# 분할 관련 타입
# =============================================================================

@dataclass
class ChapterInfo:
    """장 정보"""
    title: str
    page: int
    start_page: Optional[int] = None
    end_page: Optional[int] = None
    source_page: Optional[int] = None
    section: str = ""

@dataclass
class SplitResult:
    """분할 결과"""
    success: bool
    output_path: Optional[Path] = None
    error_message: Optional[str] = None
    chapter_info: Optional[ChapterInfo] = None

@dataclass
class SectionChapters:
    """부문별 장 정보"""
    section_name: str
    chapters: List[ChapterInfo]
    start_page: Optional[int] = None
    end_page: Optional[int] = None

# =============================================================================
# 검증 관련 타입
# =============================================================================

@dataclass
class ValidationResult:
    """검증 결과"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SectionValidation:
    """부문 검증 정보"""
    section_name: str
    found: bool
    position: int = -1
    line_number: int = -1
    context: str = ""
    original_text: str = ""

# =============================================================================
# 설정 관련 타입
# =============================================================================

@dataclass
class ProcessingConfig:
    """처리 설정"""
    extraction_method: str = "auto"
    split_mode: str = "chapter"
    validation_mode: str = "basic"
    max_pages_per_file: int = 100
    supported_formats: List[str] = field(default_factory=lambda: ['json', 'csv', 'markdown'])
    log_level: str = "INFO"

@dataclass
class OutputConfig:
    """출력 설정"""
    output_dir: Path = Path("output")
    create_subdirectories: bool = True
    overwrite_existing: bool = False
    generate_reports: bool = True
    report_format: str = "markdown"

# =============================================================================
# 보고서 관련 타입
# =============================================================================

@dataclass
class ProcessingReport:
    """처리 결과 보고서"""
    processing_time: datetime
    input_file: str
    output_dir: str
    split_mode: str
    extraction_method: str
    toc_entries_count: int
    toc_json_path: Optional[str] = None
    mapping_path: Optional[str] = None
    success_count: int = 0
    error_count: int = 0

@dataclass
class SplitReport:
    """분할 결과 보고서"""
    pdf_file_path: Path
    json_file_path: Path
    output_dir: Path
    split_time: datetime
    chapters_by_section: Dict[str, List[ChapterInfo]]
    success_count: int
    error_count: int

# =============================================================================
# 로깅 관련 타입
# =============================================================================

@dataclass
class LogConfig:
    """로깅 설정"""
    name: str
    log_dir: Path = Path("logs")
    level: str = "INFO"
    enable_console: bool = True
    enable_file: bool = True
    enable_error_file: bool = True
    enable_daily_rotation: bool = True
    max_backup_count: int = 30

# =============================================================================
# 함수 시그니처 타입
# =============================================================================

# 파일 처리 함수 타입
FileProcessor = Callable[[Path], Any]

# 검증 함수 타입
Validator = Callable[[Any], ValidationResult]

# 변환 함수 타입
Converter = Callable[[Any, str], bool]

# 콜백 함수 타입
ProgressCallback = Callable[[int, int, str], None]

# =============================================================================
# 유니온 타입
# =============================================================================

# 설정 값 타입
ConfigValue = Union[str, int, float, bool, List[Any], Dict[str, Any]]

# 처리 결과 타입
ProcessingResult = Union[bool, str, Path, ValidationResult, SplitResult]

# 출력 형식 타입
OutputFormat = Union[str, Path, bytes] 