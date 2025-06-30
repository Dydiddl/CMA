#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 공통 예외 클래스

이 모듈은 ASCR 프로젝트에서 공통으로 사용되는 예외 클래스들을 정의합니다.
"""

from typing import Optional, Dict, Any

# =============================================================================
# 기본 ASCR 예외 클래스
# =============================================================================

class ASCRException(Exception):
    """ASCR 기본 예외 클래스"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        return f"ASCR 오류: {self.message}"

# =============================================================================
# 파일 처리 관련 예외
# =============================================================================

class FileNotFoundError(ASCRException):
    """파일을 찾을 수 없을 때 발생하는 예외"""
    
    def __init__(self, file_path: str, message: Optional[str] = None):
        if message is None:
            message = f"파일을 찾을 수 없습니다: {file_path}"
        super().__init__(message, {"file_path": file_path})

class FileValidationError(ASCRException):
    """파일 검증 실패 시 발생하는 예외"""
    
    def __init__(self, file_path: str, reason: str, message: Optional[str] = None):
        if message is None:
            message = f"파일 검증 실패: {file_path} - {reason}"
        super().__init__(message, {"file_path": file_path, "reason": reason})

class FileProcessingError(ASCRException):
    """파일 처리 중 오류 발생 시 예외"""
    
    def __init__(self, file_path: str, operation: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"파일 처리 오류: {file_path} - {operation} - {error}"
        super().__init__(message, {
            "file_path": file_path,
            "operation": operation,
            "error": error
        })

# =============================================================================
# PDF 처리 관련 예외
# =============================================================================

class PDFLoadError(ASCRException):
    """PDF 로드 실패 시 발생하는 예외"""
    
    def __init__(self, pdf_path: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"PDF 로드 실패: {pdf_path} - {error}"
        super().__init__(message, {"pdf_path": pdf_path, "error": error})

class PDFExtractionError(ASCRException):
    """PDF 추출 실패 시 발생하는 예외"""
    
    def __init__(self, pdf_path: str, extraction_type: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"PDF 추출 실패: {pdf_path} - {extraction_type} - {error}"
        super().__init__(message, {
            "pdf_path": pdf_path,
            "extraction_type": extraction_type,
            "error": error
        })

class PDFSplitError(ASCRException):
    """PDF 분할 실패 시 발생하는 예외"""
    
    def __init__(self, pdf_path: str, split_mode: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"PDF 분할 실패: {pdf_path} - {split_mode} - {error}"
        super().__init__(message, {
            "pdf_path": pdf_path,
            "split_mode": split_mode,
            "error": error
        })

# =============================================================================
# 목차 처리 관련 예외
# =============================================================================

class TOCExtractionError(ASCRException):
    """목차 추출 실패 시 발생하는 예외"""
    
    def __init__(self, source: str, method: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"목차 추출 실패: {source} - {method} - {error}"
        super().__init__(message, {
            "source": source,
            "method": method,
            "error": error
        })

class TOCValidationError(ASCRException):
    """목차 검증 실패 시 발생하는 예외"""
    
    def __init__(self, toc_data: Any, validation_rule: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"목차 검증 실패: {validation_rule} - {error}"
        super().__init__(message, {
            "toc_data": str(toc_data),
            "validation_rule": validation_rule,
            "error": error
        })

class TOCStructureError(ASCRException):
    """목차 구조 오류 시 발생하는 예외"""
    
    def __init__(self, structure_type: str, expected: str, actual: str, message: Optional[str] = None):
        if message is None:
            message = f"목차 구조 오류: {structure_type} - 예상: {expected}, 실제: {actual}"
        super().__init__(message, {
            "structure_type": structure_type,
            "expected": expected,
            "actual": actual
        })

# =============================================================================
# 설정 관련 예외
# =============================================================================

class ConfigurationError(ASCRException):
    """설정 관련 오류 시 발생하는 예외"""
    
    def __init__(self, config_key: str, error: str, config_file: Optional[str] = None, message: Optional[str] = None):
        if message is None:
            message = f"설정 오류: {config_key} - {error}"
            if config_file:
                message += f" (파일: {config_file})"
        super().__init__(message, {
            "config_key": config_key,
            "error": error,
            "config_file": config_file
        })

class ConfigFileNotFoundError(ConfigurationError):
    """설정 파일을 찾을 수 없을 때 발생하는 예외"""
    
    def __init__(self, config_file: str, message: Optional[str] = None):
        if message is None:
            message = f"설정 파일을 찾을 수 없습니다: {config_file}"
        super().__init__("", "", config_file, message)

class ConfigValidationError(ConfigurationError):
    """설정 검증 실패 시 발생하는 예외"""
    
    def __init__(self, config_key: str, validation_rule: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"설정 검증 실패: {config_key} - {validation_rule} - {error}"
        super().__init__(config_key, error, None, message)

# =============================================================================
# 검증 관련 예외
# =============================================================================

class ValidationError(ASCRException):
    """검증 실패 시 발생하는 예외"""
    
    def __init__(self, validation_type: str, target: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"검증 실패: {validation_type} - {target} - {error}"
        super().__init__(message, {
            "validation_type": validation_type,
            "target": target,
            "error": error
        })

class SectionValidationError(ValidationError):
    """부문 검증 실패 시 발생하는 예외"""
    
    def __init__(self, section_name: str, expected: str, actual: str, message: Optional[str] = None):
        if message is None:
            message = f"부문 검증 실패: {section_name} - 예상: {expected}, 실제: {actual}"
        super().__init__("section", section_name, f"예상: {expected}, 실제: {actual}", message)

class ContentValidationError(ValidationError):
    """내용 검증 실패 시 발생하는 예외"""
    
    def __init__(self, content_type: str, validation_rule: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"내용 검증 실패: {content_type} - {validation_rule} - {error}"
        super().__init__("content", content_type, error, message)

# =============================================================================
# 로깅 관련 예외
# =============================================================================

class LoggingError(ASCRException):
    """로깅 관련 오류 시 발생하는 예외"""
    
    def __init__(self, logger_name: str, operation: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"로깅 오류: {logger_name} - {operation} - {error}"
        super().__init__(message, {
            "logger_name": logger_name,
            "operation": operation,
            "error": error
        })

# =============================================================================
# 보고서 관련 예외
# =============================================================================

class ReportGenerationError(ASCRException):
    """보고서 생성 실패 시 발생하는 예외"""
    
    def __init__(self, report_type: str, output_path: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"보고서 생성 실패: {report_type} - {output_path} - {error}"
        super().__init__(message, {
            "report_type": report_type,
            "output_path": output_path,
            "error": error
        })

# =============================================================================
# 데이터 처리 관련 예외
# =============================================================================

class DataProcessingError(ASCRException):
    """데이터 처리 실패 시 발생하는 예외"""
    
    def __init__(self, data_type: str, operation: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"데이터 처리 오류: {data_type} - {operation} - {error}"
        super().__init__(message, {
            "data_type": data_type,
            "operation": operation,
            "error": error
        })

class DataFormatError(DataProcessingError):
    """데이터 형식 오류 시 발생하는 예외"""
    
    def __init__(self, data_type: str, expected_format: str, actual_format: str, message: Optional[str] = None):
        if message is None:
            message = f"데이터 형식 오류: {data_type} - 예상: {expected_format}, 실제: {actual_format}"
        super().__init__(data_type, "format_validation", f"예상: {expected_format}, 실제: {actual_format}", message)

class DataConversionError(DataProcessingError):
    """데이터 변환 실패 시 발생하는 예외"""
    
    def __init__(self, source_format: str, target_format: str, error: str, message: Optional[str] = None):
        if message is None:
            message = f"데이터 변환 실패: {source_format} → {target_format} - {error}"
        super().__init__("conversion", f"{source_format}→{target_format}", error, message)

# =============================================================================
# 유틸리티 함수
# =============================================================================

def handle_exception(exception: Exception, context: Optional[Dict[str, Any]] = None) -> str:
    """
    예외 처리 유틸리티 함수
    
    Args:
        exception: 발생한 예외
        context: 추가 컨텍스트 정보
        
    Returns:
        처리된 오류 메시지
    """
    if isinstance(exception, ASCRException):
        error_msg = str(exception)
        if context:
            error_msg += f" (컨텍스트: {context})"
        return error_msg
    else:
        error_msg = f"예상치 못한 오류: {type(exception).__name__} - {str(exception)}"
        if context:
            error_msg += f" (컨텍스트: {context})"
        return error_msg

def is_ascr_exception(exception: Exception) -> bool:
    """
    ASCR 예외인지 확인
    
    Args:
        exception: 확인할 예외
        
    Returns:
        ASCR 예외 여부
    """
    return isinstance(exception, ASCRException) 