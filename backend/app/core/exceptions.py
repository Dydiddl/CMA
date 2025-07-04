#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
커스텀 예외 클래스 모듈
"""

class CMAException(Exception):
    """CMA 기본 예외 클래스"""
    pass

class NotFoundException(CMAException):
    """리소스를 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, message: str = "리소스를 찾을 수 없습니다"):
        self.message = message
        super().__init__(self.message)

class ValidationException(CMAException):
    """데이터 검증 예외"""
    def __init__(self, message: str = "데이터 검증에 실패했습니다"):
        self.message = message
        super().__init__(self.message)

class DatabaseException(CMAException):
    """데이터베이스 관련 예외"""
    def __init__(self, message: str = "데이터베이스 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message)

class FileProcessingException(CMAException):
    """파일 처리 관련 예외"""
    def __init__(self, message: str = "파일 처리 중 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message)

class AuthenticationException(CMAException):
    """인증 관련 예외"""
    def __init__(self, message: str = "인증에 실패했습니다"):
        self.message = message
        super().__init__(self.message)

class AuthorizationException(CMAException):
    """권한 관련 예외"""
    def __init__(self, message: str = "권한이 부족합니다"):
        self.message = message
        super().__init__(self.message)

class ConfigurationException(CMAException):
    """설정 오류 시 발생하는 예외"""
    def __init__(self, message: str = "설정 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message)

class PerformanceException(CMAException):
    """성능 관련 예외"""
    def __init__(self, message: str = "성능 오류가 발생했습니다"):
        self.message = message
        super().__init__(self.message)

class ContractNotFoundException(CMAException):
    """계약을 찾을 수 없음 예외"""
    pass

class UserNotFoundException(CMAException):
    """사용자를 찾을 수 없음 예외"""
    pass

class FinancialRecordNotFoundException(CMAException):
    """재무 기록을 찾을 수 없음 예외"""
    pass

class LaborNotFoundException(CMAException):
    """노무를 찾을 수 없음 예외"""
    pass

class WorkTimeNotFoundException(CMAException):
    """작업 시간 기록을 찾을 수 없음 예외"""
    pass 