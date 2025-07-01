#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMA 데스크톱 애플리케이션 커스텀 예외 클래스
"""

class CMAException(Exception):
    """CMA 애플리케이션 기본 예외 클래스"""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class DatabaseException(CMAException):
    """데이터베이스 관련 예외"""
    pass

class APIException(CMAException):
    """API 관련 예외"""
    pass

class ConfigException(CMAException):
    """설정 관련 예외"""
    pass

class UIException(CMAException):
    """UI 관련 예외"""
    pass 