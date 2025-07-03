#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 예외 처리 모듈
"""

from typing import Optional, Dict, Any


class CMAException(Exception):
    """CMA 전용 예외 클래스"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class DatabaseConnectionError(CMAException):
    """데이터베이스 연결 오류"""
    
    def __init__(self, message: str = "데이터베이스 연결에 실패했습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "DB_CONNECTION_ERROR", details)


class DatabaseQueryError(CMAException):
    """데이터베이스 쿼리 오류"""
    
    def __init__(self, message: str = "데이터베이스 쿼리 실행에 실패했습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "DB_QUERY_ERROR", details)


class APICommunicationError(CMAException):
    """API 통신 오류"""
    
    def __init__(self, message: str = "API 서버와의 통신에 실패했습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "API_COMMUNICATION_ERROR", details)


class AuthenticationError(CMAException):
    """인증 오류"""
    
    def __init__(self, message: str = "인증에 실패했습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTH_ERROR", details)


class ConfigurationError(CMAException):
    """설정 오류"""
    
    def __init__(self, message: str = "설정 파일을 읽을 수 없습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "CONFIG_ERROR", details)


class FileProcessingError(CMAException):
    """파일 처리 오류"""
    
    def __init__(self, message: str = "파일 처리 중 오류가 발생했습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "FILE_PROCESSING_ERROR", details)


class GUIError(CMAException):
    """GUI 관련 오류"""
    
    def __init__(self, message: str = "GUI 초기화에 실패했습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "GUI_ERROR", details)


class ValidationError(CMAException):
    """데이터 검증 오류"""
    
    def __init__(self, message: str = "데이터 검증에 실패했습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class NetworkError(CMAException):
    """네트워크 오류"""
    
    def __init__(self, message: str = "네트워크 연결에 문제가 있습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "NETWORK_ERROR", details)


class ResourceError(CMAException):
    """리소스 오류"""
    
    def __init__(self, message: str = "필요한 리소스를 찾을 수 없습니다", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "RESOURCE_ERROR", details) 