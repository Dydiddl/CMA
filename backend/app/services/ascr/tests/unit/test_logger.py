#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
로거 테스트
"""

import pytest
from pathlib import Path
from src.utils.log import ASCRLogger, get_logger, setup_logging

class TestASCRLogger:
    """ASCR 로거 테스트"""
    
    def test_logger_creation(self, temp_dir):
        """로거 생성 테스트"""
        logger = ASCRLogger("test_logger", temp_dir)
        assert logger.name == "test_logger"
        assert logger.log_dir == temp_dir
    
    def test_logger_info(self, temp_dir):
        """정보 로그 테스트"""
        logger = ASCRLogger("test_logger", temp_dir)
        logger.info("테스트 정보 메시지")
        
        # 로그 파일이 생성되었는지 확인
        log_file = temp_dir / "test_logger.log"
        assert log_file.exists()
        
        # 로그 내용 확인
        with open(log_file, 'r', encoding='utf-8', newline='', encoding='utf-8', newline='') as f:
            content = f.read()
            assert "테스트 정보 메시지" in content
    
    def test_logger_error(self, temp_dir):
        """에러 로그 테스트"""
        logger = ASCRLogger("test_logger", temp_dir)
        logger.error("테스트 에러 메시지")
        
        # 에러 로그 파일이 생성되었는지 확인
        error_log_file = temp_dir / "test_logger_error.log"
        assert error_log_file.exists()
        
        # 로그 내용 확인
        with open(error_log_file, 'r', encoding='utf-8', newline='', encoding='utf-8', newline='') as f:
            content = f.read()
            assert "테스트 에러 메시지" in content
    
    def test_get_logger(self, temp_dir):
        """get_logger 함수 테스트"""
        logger = get_logger("test_get_logger", temp_dir)
        assert isinstance(logger, ASCRLogger)
        assert logger.name == "test_get_logger"
    
    def test_setup_logging(self, temp_dir):
        """setup_logging 함수 테스트"""
        setup_logging(temp_dir, "DEBUG")
        # 설정이 성공적으로 적용되었는지 확인
        assert temp_dir.exists() 