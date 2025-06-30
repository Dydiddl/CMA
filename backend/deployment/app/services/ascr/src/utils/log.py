#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASCR 로깅 시스템
구조화된 로깅과 에러 추적을 제공합니다.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json
import traceback

class ASCRLogger:
    """ASCR 전용 로거 클래스"""
    
    def __init__(self, name: str = "ASCR", log_level: str = "INFO"):
        self.name = name
        self.log_level = getattr(logging, log_level.upper())
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """로거 설정"""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.log_level)
        
        # 중복 핸들러 방지
        if logger.handlers:
            return logger
            
        # 로그 포맷 설정
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 파일 핸들러
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 일반 로그 파일
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "ascr.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 에러 로그 파일
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "ascr_error.log",
            maxBytes=5*1024*1024,   # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
        
        return logger
    
    def info(self, message: str, **kwargs):
        """정보 로그"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """경고 로그"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, error: Optional[Exception] = None, **kwargs):
        """에러 로그"""
        if error:
            error_info = {
                'error_type': type(error).__name__,
                'error_message': str(error),
                'traceback': traceback.format_exc()
            }
            kwargs.update(error_info)
            self.logger.error(f"{message} - {error}", extra=kwargs)
        else:
            self.logger.error(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        """디버그 로그"""
        self.logger.debug(message, extra=kwargs)
    
    def critical(self, message: str, error: Optional[Exception] = None, **kwargs):
        """치명적 오류 로그"""
        if error:
            error_info = {
                'error_type': type(error).__name__,
                'error_message': str(error),
                'traceback': traceback.format_exc()
            }
            kwargs.update(error_info)
            self.logger.critical(f"{message} - {error}", extra=kwargs)
        else:
            self.logger.critical(message, extra=kwargs)

def get_logger(name: str = None) -> ASCRLogger:
    """로거 인스턴스 반환"""
    if name is None:
        name = "ASCR"
    return ASCRLogger(name)

def log_function_call(func_name: str, args: Dict[str, Any] = None, result: Any = None):
    """함수 호출 로깅 데코레이터용"""
    logger = get_logger()
    logger.info(f"함수 호출: {func_name}", 
                function_name=func_name,
                arguments=args,
                result=result)

def log_workflow_step(step_name: str, status: str = "started", details: Dict[str, Any] = None):
    """워크플로우 단계 로깅"""
    logger = get_logger("Workflow")
    logger.info(f"워크플로우 단계: {step_name} - {status}",
                step_name=step_name,
                status=status,
                details=details or {})

def log_file_operation(operation: str, file_path: str, success: bool, details: Dict[str, Any] = None):
    """파일 작업 로깅"""
    logger = get_logger("FileOps")
    level = logger.info if success else logger.error
    level(f"파일 작업: {operation} - {file_path}",
          operation=operation,
          file_path=file_path,
          success=success,
          details=details or {})

def log_performance(operation: str, duration: float, details: Dict[str, Any] = None):
    """성능 로깅"""
    logger = get_logger("Performance")
    logger.info(f"성능 측정: {operation} - {duration:.2f}초",
                operation=operation,
                duration=duration,
                details=details or {})

# 기존 호환성을 위한 함수들
def setup_logging(level: str = "INFO") -> logging.Logger:
    """기존 호환성을 위한 로깅 설정"""
    logger = get_logger()
    return logger.logger

def get_logger_legacy(name: str = None) -> logging.Logger:
    """기존 호환성을 위한 로거 반환"""
    logger = get_logger(name)
    return logger.logger 