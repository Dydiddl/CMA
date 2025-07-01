#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
커스텀 예외 클래스 정의
"""

class CMAException(Exception):
    """CMA 시스템 기본 예외 클래스"""
    pass

class NotFoundException(CMAException):
    """리소스를 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, message: str = "리소스를 찾을 수 없습니다"):
        self.message = message
        super().__init__(self.message)

class ValidationException(CMAException):
    """데이터 검증 실패 시 발생하는 예외"""
    def __init__(self, message: str = "데이터 검증에 실패했습니다"):
        self.message = message
        super().__init__(self.message)

class DatabaseException(CMAException):
    """데이터베이스 관련 오류 시 발생하는 예외"""
    def __init__(self, message: str = "데이터베이스 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message)

class FileProcessingException(CMAException):
    """파일 처리 오류 시 발생하는 예외"""
    def __init__(self, message: str = "파일 처리 중 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message)

class AuthenticationException(CMAException):
    """인증 실패 시 발생하는 예외"""
    def __init__(self, message: str = "인증에 실패했습니다"):
        self.message = message
        super().__init__(self.message)

class AuthorizationException(CMAException):
    """권한 부족 시 발생하는 예외"""
    def __init__(self, message: str = "권한이 부족합니다"):
        self.message = message
        super().__init__(self.message)

class ConfigurationException(CMAException):
    """설정 오류 시 발생하는 예외"""
    def __init__(self, message: str = "설정 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message)

class PerformanceException(CMAException):
    """성능 관련 오류 시 발생하는 예외"""
    def __init__(self, message: str = "성능 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message) 