#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 예외 처리 시스템
"""

from typing import Optional, Any, Dict

class ASCRException(Exception):
    """ASCR 기본 예외 클래스"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message

class PDFProcessingError(ASCRException):
    """PDF 처리 중 발생하는 오류"""
    
    def __init__(self, message: str, pdf_path: Optional[str] = None, page_number: Optional[int] = None):
        details = {}
        if pdf_path:
            details['pdf_path'] = pdf_path
        if page_number is not None:
            details['page_number'] = page_number
        
        super().__init__(message, "PDF_PROCESSING_ERROR", details)

class ConfigurationError(ASCRException):
    """설정 관련 오류"""
    
    def __init__(self, message: str, config_file: Optional[str] = None, config_key: Optional[str] = None):
        details = {}
        if config_file:
            details['config_file'] = config_file
        if config_key:
            details['config_key'] = config_key
        
        super().__init__(message, "CONFIGURATION_ERROR", details)

class FileOperationError(ASCRException):
    """파일 작업 관련 오류"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, operation: Optional[str] = None):
        details = {}
        if file_path:
            details['file_path'] = file_path
        if operation:
            details['operation'] = operation
        
        super().__init__(message, "FILE_OPERATION_ERROR", details)

class ValidationError(ASCRException):
    """데이터 검증 오류"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Optional[Any] = None):
        details = {}
        if field:
            details['field'] = field
        if value is not None:
            details['value'] = value
        
        super().__init__(message, "VALIDATION_ERROR", details)

class OCRProcessingError(ASCRException):
    """OCR 처리 중 발생하는 오류"""
    
    def __init__(self, message: str, ocr_engine: Optional[str] = None, confidence: Optional[float] = None):
        details = {}
        if ocr_engine:
            details['ocr_engine'] = ocr_engine
        if confidence is not None:
            details['confidence'] = confidence
        
        super().__init__(message, "OCR_PROCESSING_ERROR", details)

class MemoryError(ASCRException):
    """메모리 부족 오류"""
    
    def __init__(self, message: str, required_memory: Optional[str] = None, available_memory: Optional[str] = None):
        details = {}
        if required_memory:
            details['required_memory'] = required_memory
        if available_memory:
            details['available_memory'] = available_memory
        
        super().__init__(message, "MEMORY_ERROR", details)

class TimeoutError(ASCRException):
    """작업 시간 초과 오류"""
    
    def __init__(self, message: str, timeout_seconds: Optional[float] = None, operation: Optional[str] = None):
        details = {}
        if timeout_seconds is not None:
            details['timeout_seconds'] = timeout_seconds
        if operation:
            details['operation'] = operation
        
        super().__init__(message, "TIMEOUT_ERROR", details)

def handle_exception(func):
    """예외를 처리하는 데코레이터"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ASCRException as e:
            # ASCR 예외는 그대로 재발생
            raise
        except Exception as e:
            # 일반 예외를 ASCR 예외로 변환
            raise ASCRException(f"예상치 못한 오류: {str(e)}", "UNEXPECTED_ERROR", {
                'original_exception': type(e).__name__,
                'function': func.__name__
            })
    return wrapper

def safe_execute(func, *args, **kwargs):
    """안전한 함수 실행을 위한 유틸리티"""
    try:
        return func(*args, **kwargs), None
    except Exception as e:
        return None, e

class ConfigError(Exception):
    """설정 관련 기본 예외 클래스"""
    pass

class ConfigFileNotFoundError(ConfigError):
    """설정 파일을 찾을 수 없을 때 발생하는 예외"""
    pass

class ConfigParseError(ConfigError):
    """설정 파일 파싱 오류 시 발생하는 예외"""
    pass

class ConfigValidationError(ConfigError):
    """설정 값 검증 실패 시 발생하는 예외"""
    pass

class ConfigKeyError(ConfigError):
    """설정 키가 존재하지 않을 때 발생하는 예외"""
    pass 